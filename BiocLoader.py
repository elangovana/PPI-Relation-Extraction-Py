import bioc
import numpy as np
from BiocAnnotationGenes import BiocAnnotationGenes
from BiocRelation import BiocRelation
from BiocSentences import BiocSentences
from ModelLogisticsRegresssion import ModelLogisticsRegression


class BiocLoader:

    def __init__(self, model=None):
        self.biocDocProcessors = [BiocSentences().convert_to_vec, BiocAnnotationGenes().get_gene_names_normalised]
        self.model = model or ModelLogisticsRegression()
        self.sentence_extractor = BiocSentences().convert_to_vec

    def parse(self, filename):
        result =[]
        with open(filename, 'r') as fp:
            collection = bioc.load(fp)
            for doc in collection.documents:
                result.extend( self._convert_doc_to_flat(doc))


        self.model.train(np.array(result)[:,0:3], np.array(result)[:,4]);

    def _convert_doc_to_flat(self, doc):
        result = []
        normalised_genes = BiocAnnotationGenes().get_gene_names_normalised(doc)
        relex = BiocRelation()
        gene_pairs = self._get_gene_pairs(normalised_genes)
        #normalise gene names in sentences
        normalise_gene_names(self.sentence_extractor(doc),  )
        for gene_pair in gene_pairs:
            # construct unique id
            gene1 = gene_pair[0]
            gene2 = gene_pair[1]
            uid = "{}#{}#{}".format(doc.id, gene1, gene2)
            result.append([uid, doc.id, gene1, gene2, self.sentence_extractor(doc), relex.is_valid(doc, gene1, gene2)])

        return result

    def _get_gene_pairs(self, normalised_genes):
        result = []
        for gene1 in normalised_genes:
            for gene2 in normalised_genes:
                result.append((gene1, gene2))
        return result
