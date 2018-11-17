

class PreprocessorNormaliseGenes:

    def __init__(self):
        pass

    def Run(self):
        pass

    def normalise_gene_names(self, v_sentences, gene, normalised_gene):
        # get the gene names to replace
        # replace
        for i in range(0, len(v_sentences)):
            v_sentences[i] = v_sentences[i].replace(gene, normalised_gene)
        return v_sentences

    def normalise_gene_names_bulk(self, v_sentences, dict_gene_name_to_Id):
        # get the gene names to replace
        # replace
        for key, value in dict_gene_name_to_Id.items():
            v_sentences = self.normalise_gene_names(v_sentences, key, value)
        return v_sentences
