import bioc
import numpy as np
from BiocAnnotationGenes import BiocAnnotationGenes
from BiocRelation import BiocRelation
from BiocSentences import BiocSentences
from ModelLogisticsRegresssion import ModelLogisticsRegression
from PPIFragmentExtractor import PPIFragementExtractor
from PreprocessorNormaliseGenes import PreprocessorNormaliseGenes





class BiocLoader:

    def __init__(self, model=None):

        self.model = model or ModelLogisticsRegression()
        self.sentence_extractor = BiocSentences().convert_to_vec


    def parse(self, filename):
        result =[]
        with open(filename, 'r') as fp:
            collection = bioc.load(fp)
            for doc in collection.documents:
                result.extend( self._convert_doc_to_flat(doc))


        return  result
        #self.model.train(np.array(result)[:,0:3], np.array(result)[:,4]);

    def _convert_doc_to_flat(self, doc):
        result = []
        gene_to_norm_gene_dict = BiocAnnotationGenes().get_gene_names_to_normalised_dict(doc)
        relex = BiocRelation()
        gene_pairs = self._get_gene_pairs(set(gene_to_norm_gene_dict.values()))
        #normalise gene names in sentences
        s = PreprocessorNormaliseGenes().normalise_gene_names_bulk (self.sentence_extractor(doc), gene_to_norm_gene_dict )
        for gene_pair in gene_pairs:
            # construct unique id
            gene1 = gene_pair[0]
            gene2 = gene_pair[1]
            fragments = PPIFragementExtractor().extract(s, gene1, gene2 )


            uid = "{}#{}#{}".format(doc.id, gene1, gene2)
            result.append([uid, doc.id, gene1, gene2, fragments, relex.is_valid(doc, gene1, gene2)])

        return result

    def _get_gene_pairs(self, normalised_genes):
        result = []
        for gene1 in normalised_genes:
            for gene2 in normalised_genes:
                result.append((gene1, gene2))
        return result
