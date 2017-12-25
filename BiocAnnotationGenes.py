import bioc

GENE = "Gene"


class BiocAnnotationGenes:
    def __init__(self):
        pass

    def get_gene_names(self, bioc_element):
        if isinstance(bioc_element , bioc.BioCDocument):
            return self._get_gene_name_document(bioc_element)
        else:
            return self._get_gene_name_passage(bioc_element)

    def _get_gene_name_document(self, bioc_doc):
        result = []
        for passage in bioc_doc.passages:
            result.append(self._get_gene_name_passage(passage))
        return result

    def _get_gene_name_passage(self, bioc_passage):
        result = []
        for annotation in bioc_passage.annotations:
            if self.is_annotation_gene_name(annotation):
               result.append(annotation.infons["NCBI Gene"])
        return result

    @staticmethod
    def is_annotation_gene_name( annotation) :
        return annotation.infons["type"] == GENE

