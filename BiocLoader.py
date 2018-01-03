import bioc
import numpy as np
from BiocAnnotationGenes import BiocAnnotationGenes
from BiocRelation import BiocRelation
from BiocSentences import BiocSentences
from ModelLogisticsRegresssion import ModelLogisticsRegression
from NGramFeatureExtractor import NGramFeatureExtractor
from PPIFragmentExtractor import PPIFragementExtractor
from PreprocessorNormaliseGenes import PreprocessorNormaliseGenes
import os
import tempfile
import logging
import collections
import cPickle as pickle
import itertools



I_DOCID = 1
I_GENE1 = 2
I_GENE2 = 3
I_SENTENCES = 4
I_GENESINDOC = 5
I_BIOCDOC = 6
I_NORM_FREQUNCE = 7
I_FRAGMENTS = 8
I_SELFRELATION = 9


class BiocLoader:

    def __init__(self, model=None, logs_dir=tempfile.mkdtemp()):
        self.logs_dir = logs_dir
        self.model = model or ModelLogisticsRegression()
        self.sentence_extractor = BiocSentences().convert_to_vec
        self.logger = logging.getLogger(__name__)
        self.retrieve_gene_names_dict = BiocAnnotationGenes().get_gene_names_to_normalised_dict
        self.validate_relation = BiocRelation().is_valid
        self.preprocessor_replace_with_norm_genes = PreprocessorNormaliseGenes().normalise_gene_names_bulk
        self.preprocessor_ngram_feature_extractor = NGramFeatureExtractor().extract
        self.preprocessor_fragment_extractor = PPIFragementExtractor().extract

    def parse(self, filename, output_dir=tempfile.mkdtemp()):
        # Read file and do preliminary pre processing to form rows of records
        data_rows = []
        with open(filename, 'r') as fp:
            collection = bioc.load(fp)
            for doc in collection.documents:
                rows_x = self.convert_bioc_document_to_rows(doc)
                data_rows.extend(rows_x)
        #subset
        #data_rows =  data_rows[1:100]

        # Extract fragments
        for r in data_rows:
            fragments = self.preprocessor_fragment_extractor(r[I_SENTENCES], r[I_GENE1], r[I_GENE2], r[I_GENESINDOC])
            count_of_valid_fragments = sum(r[I_GENE1] in f and r[I_GENE2] in f for f in fragments)
            normalised_frequency = count_of_valid_fragments * 100 / (len(r[I_SENTENCES]))
            combined_fragments = "   \t ".join(fragments)
            r.append(normalised_frequency)
            r.append(combined_fragments)
            r.append(int(r[I_GENE1] == r[I_GENE2]))

        # Extract fragments
        v_ngram_features, n_gram_names = self.preprocessor_ngram_feature_extractor(np.array(data_rows)[:, I_FRAGMENTS])
        features = v_ngram_features
        feature_names = n_gram_names

        # Append features to ngrams
        # Self Relation
        new_feature = np.array(data_rows)[:, I_SELFRELATION]
        features = np.concatenate((features, new_feature.reshape(len(new_feature), 1)), axis=1)
        feature_names.append("SelfRelation")

        # Train model
        labels = np.array(self.get_labels(data_rows))
        trained_model = self.model.train(features, labels)

        # log formatted features to file
        logs_features_file = os.path.join(self.logs_dir,
                                          tempfile.mkstemp(prefix="data_formatted_features", suffix=".csv")[1])
        self.save_to_file(logs_features_file, (["uid", "docid", "gene1", "gene2"], feature_names, ["labels"]),
                          (np.array(data_rows)[:, 0:I_SENTENCES], features, labels))

        # persist trained model
        pickle_file_name = os.path.join(output_dir, tempfile.mkstemp(prefix="trained_model")[1])
        self.logger.info("Saving model to %s", pickle_file_name)
        with open(pickle_file_name, 'wb') as fd:
            pickle.dump(trained_model, fd)

    def save_to_file(self, logs_features_file, column_names, columnr_data_to_merge):
        c_names = []
        for c in column_names:
            c_names.extend(c)

        data = columnr_data_to_merge[0]

        for i in range(1, len(columnr_data_to_merge)):
            if isinstance(columnr_data_to_merge[i][0], collections.Sequence):
                w = len(columnr_data_to_merge[i][0])
            elif isinstance(columnr_data_to_merge[i][0], np.ndarray):
                w = columnr_data_to_merge[i].shape[1]
            else:
                w = 1

            data = np.concatenate((data, np.array(columnr_data_to_merge[i]).reshape(len(columnr_data_to_merge[i]), w)),
                                  axis=1)

        data = np.concatenate((np.array(c_names).reshape(1, len(c_names)), data), axis=0)

        self.logger.info("Writing features to log file %s", logs_features_file)

        np.savetxt(logs_features_file, data, delimiter='|', fmt="%s")

    def convert_bioc_document_to_rows(self, doc):
        result_x = []

        gene_to_norm_gene_dict = self.retrieve_gene_names_dict(doc)
        genes = gene_to_norm_gene_dict.values()
        gene_pairs = itertools.combinations_with_replacement(list(set(genes)), 2)

        # normalise gene names in sentences
        sentences = self.sentence_extractor(doc)
        normalised_sentences = self.preprocessor_replace_with_norm_genes(sentences, gene_to_norm_gene_dict)

        # extract fragments
        for gene_pair in gene_pairs:
            # construct unique id
            gene1 = gene_pair[0]
            gene2 = gene_pair[1]
            uid = "{}#{}#{}".format(doc.id, gene1, gene2)
            result_x.append([uid, doc.id, gene1, gene2, normalised_sentences, genes, doc])



        return result_x

    def get_labels(self, data_rows):
        labels = []
        for r in data_rows:
            labels.append(self.validate_relation(r[I_BIOCDOC], r[I_GENE1], r[I_GENE2]))
        return labels
