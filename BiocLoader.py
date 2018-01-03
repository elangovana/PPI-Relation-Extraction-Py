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


class BiocLoader:

    def __init__(self, model=None, logs_dir=tempfile.mkdtemp()):
        self.logs_dir = logs_dir
        self.model = model or ModelLogisticsRegression()
        self.sentence_extractor = BiocSentences().convert_to_vec
        self.logger = logging.getLogger(__name__)
        self.genenames_normaliser = BiocAnnotationGenes().get_gene_names_to_normalised_dict
        self.validate_relation = BiocRelation().is_valid

    def parse(self, filename, output_dir=tempfile.mkdtemp()):
        data_rows = []
        labels = []
        with open(filename, 'r') as fp:
            collection = bioc.load(fp)
            for doc in collection.documents:
                rows_x, rows_y = self.convert_bioc_document_to_rows(doc)
                data_rows.extend(rows_x)
                labels.extend(rows_y)

        # return result
        v_ngram_features, n_gram_names = NGramFeatureExtractor().extract(np.array(data_rows)[:, 4])
        # freq_v = np.array(data_rows)[:, 5].astype(int)

        # add the frequency feature
        # features = np.concatenate((v_ngram_features, freq_v.reshape(len(freq_v),1)), axis=1)
        features = v_ngram_features
        logs_features_file = os.path.join(self.logs_dir,
                                          tempfile.mkstemp(prefix="data_formatted_features", suffix=".csv")[1])
        self.save_to_file(logs_features_file, (["uid", "docid", "gene1", "gene2"], n_gram_names, ["label"]),
                          (np.array(data_rows)[:, 0:4], features, labels))
        trained_model = self.model.train(features, np.array(labels));

        # persist trained model
        with open(os.path.join(output_dir, tempfile.mkstemp(prefix="trained_model")), 'wb') as fd:
            pickle.dump(trained_model, fd)

    def save_to_file(self, logs_features_file, column_names, columnr_data_to_merge):
        c_names = []
        for c in column_names:
            c_names.extend(c)

        data = columnr_data_to_merge[0]

        for i in range(1, len(columnr_data_to_merge)):
            print(columnr_data_to_merge[i][0:5])
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
        result_y = []

        gene_to_norm_gene_dict = self.genenames_normaliser(doc)
        genes = gene_to_norm_gene_dict.values()
        gene_pairs = itertools.combinations(list(set(genes)), 2)

        # normalise gene names in sentences
        normalised_sentences = PreprocessorNormaliseGenes().normalise_gene_names_bulk(self.sentence_extractor(doc),
                                                                                      gene_to_norm_gene_dict)
        # extract fragments
        for gene_pair in gene_pairs:
            # construct unique id
            gene1 = gene_pair[0]
            gene2 = gene_pair[1]
            fragments = PPIFragementExtractor().extract(normalised_sentences, gene1, gene2, genes)
            count_of_valid_fragments = sum(gene1 in f and gene2 in f for f in fragments)
            normalised_freqeuncy = (count_of_valid_fragments) * 100 / (len(normalised_sentences))
            combined_fragments = "   \t ".join(fragments)
            uid = "{}#{}#{}".format(doc.id, gene1, gene2)
            result_x.append([uid, doc.id, gene1, gene2, combined_fragments, normalised_freqeuncy])
            result_y.append(self.validate_relation(doc, gene1, gene2))

        return result_x, result_y
