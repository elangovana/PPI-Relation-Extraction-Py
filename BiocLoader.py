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

class BiocLoader:

    def __init__(self, model=None, logs_dir = tempfile.mkdtemp()):
        self.logs_dir = logs_dir
        self.model = model or ModelLogisticsRegression()
        self.sentence_extractor = BiocSentences().convert_to_vec
        self.logger = logging.getLogger(__name__)

    def parse(self, filename):
        data_rows = []
        labels = []
        with open(filename, 'r') as fp:
            collection = bioc.load(fp)
            for doc in collection.documents:
                rows_x, rows_y = self._convert_doc_to_flat(doc)
                data_rows.extend(rows_x)
                labels.extend(rows_y)

        # return result
        v_ngram_features = NGramFeatureExtractor().extract(np.array(data_rows)[:, 4])
        freq_v = np.array(data_rows)[:, 5].astype(int)

        # add the frequency feature
        # features = np.concatenate((v_ngram_features, freq_v.reshape(len(freq_v),1)), axis=1)
        features = v_ngram_features
        logs_features_file = os.path.join(self.logs_dir, tempfile.mkstemp(suffix=".csv")[1])
        self.logger.info("Writing features to log file %s", logs_features_file)
        np.savetxt(logs_features_file, features, delimiter='|')
        self.model.train(features, np.array( labels));


    def _convert_doc_to_flat(self, doc):
        result_x = []
        result_y = []
        gene_to_norm_gene_dict = BiocAnnotationGenes().get_gene_names_to_normalised_dict(doc)
        relex = BiocRelation()
        genes = gene_to_norm_gene_dict.values()
        gene_pairs = self._get_gene_pairs(set(genes))
        # normalise gene names in sentences
        normalised_sentences = PreprocessorNormaliseGenes().normalise_gene_names_bulk(self.sentence_extractor(doc),
                                                                                      gene_to_norm_gene_dict)
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
            result_y.append(relex.is_valid(doc, gene1, gene2))

        return result_x, result_y

    def _get_gene_pairs(self, normalised_genes):
        result = []

        genes_list = list(normalised_genes)
        for i in range(0, len(genes_list)):
            for j in range(i+1, len(genes_list)):
                gene1= genes_list[i]
                gene2= genes_list[j]
                result.append((gene1, gene2))
        return result
