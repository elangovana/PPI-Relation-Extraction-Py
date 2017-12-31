import bioc
import numpy as np
from BiocAnnotationGenes import BiocAnnotationGenes
from BiocRelation import BiocRelation
from BiocSentences import BiocSentences
from ModelLogisticsRegresssion import ModelLogisticsRegression
from NGramFeatureExtractor import NGramFeatureExtractor
from PPIFragmentExtractor import PPIFragementExtractor
from PreprocessorNormaliseGenes import PreprocessorNormaliseGenes


class BiocLoader:

    def __init__(self, model=None):

        self.model = model or ModelLogisticsRegression()
        self.sentence_extractor = BiocSentences().convert_to_vec

    def parse(self, filename):
        result = []
        with open(filename, 'r') as fp:
            collection = bioc.load(fp)
            for doc in collection.documents:
                result.extend(self._convert_doc_to_flat(doc))

        # return result
        v_ngram_features = NGramFeatureExtractor().extract(np.array(result)[:, 4])
        freq_v = np.array(result)[:, 5].astype(int)
        print(v_ngram_features.shape)
        print( np.array(freq_v).T.shape)
        # add the frequency feature
        features =v_ngram_features# np.concatenate((v_ngram_features, freq_v.reshape(len(freq_v),1)), axis=1)
        # i = 0
        # for row in v_ngram_features:
        #
        #     rown = np.concatenate([row, [freq_v[i]]])
        #     #print(rown)
        #     np.append(rown)
        #
        #     #   features[i].append( lastColumn)
        #     # Now add the new column to the current row
        #     i = i + 1


        # v_ngram_features[:, -1] = freq_v#np.array( np.array(result)[:, 5]).reshape((len(np.array(result)[:, 5]), 1))
        self.model.train(features, np.array(result)[:, 6]);

    def _convert_doc_to_flat(self, doc):
        result = []
        gene_to_norm_gene_dict = BiocAnnotationGenes().get_gene_names_to_normalised_dict(doc)
        relex = BiocRelation()
        gene_pairs = self._get_gene_pairs(set(gene_to_norm_gene_dict.values()))
        # normalise gene names in sentences
        normalised_sentences = PreprocessorNormaliseGenes().normalise_gene_names_bulk(self.sentence_extractor(doc),
                                                                                      gene_to_norm_gene_dict)
        for gene_pair in gene_pairs:
            # construct unique id
            gene1 = gene_pair[0]
            gene2 = gene_pair[1]
            fragments = PPIFragementExtractor().extract(normalised_sentences, gene1, gene2)
            count_of_valid_fragments = sum(gene1 in f and gene2 in f for f in fragments)
            normalised_freqeuncy = (count_of_valid_fragments) * 100 / (len(normalised_sentences))
            combined_fragments = " nline nline ".join(fragments)
            uid = "{}#{}#{}".format(doc.id, gene1, gene2)
            result.append([uid, doc.id, gene1, gene2, combined_fragments, normalised_freqeuncy,
                           relex.is_valid(doc, gene1, gene2)])

        return result

    def _get_gene_pairs(self, normalised_genes):
        result = []
        for gene1 in normalised_genes:
            for gene2 in normalised_genes:
                if  gene1 != gene2:
                    result.append((gene1, gene2))
        return result
