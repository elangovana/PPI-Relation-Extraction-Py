import bioc

NCBI_GENE = "NCBI GENE"

GENE = "Gene"


class BiocAnnotationGenes:
    def __init__(self):
        pass

    def get_gene_names_normalised(self, bioc_element):
        gene_type = NCBI_GENE
        if isinstance(bioc_element, bioc.BioCDocument):
            return self._get_gene_name_normalised_document(bioc_element, gene_type)
        else:
            return self._get_gene_name_normalised_passage(bioc_element, gene_type)

    def get_gene_names(self, bioc_element):
        if isinstance(bioc_element, bioc.BioCDocument):
            return self._get_gene_name_document(bioc_element)
        else:
            return self._get_gene_name_passage(bioc_element)

    def _get_gene_name_normalised_document(self, bioc_doc, gene_type=None):
        result = set()
        for passage in bioc_doc.passages:
            result = result.union(self._get_gene_name_normalised_passage(passage, gene_type))
        return result

    def _get_gene_name_normalised_passage(self, bioc_passage, gene_type=NCBI_GENE):
        result = set()
        for annotation in bioc_passage.annotations:
            if self.is_annotation_gene_name(annotation):
                result.add(annotation.infons[gene_type])
        return result

    @staticmethod
    def is_annotation_gene_name(annotation):
        return annotation.infons["type"] == GENE

    def _get_gene_name_document(self, bioc_doc):
        result = set()
        for passage in bioc_doc.passages:
            result = result.union(self._get_gene_name_passage(passage))
        return result

    def _get_gene_name_passage(self, bioc_passage):
        result = set()
        for annotation in bioc_passage.annotations:
            if self.is_annotation_gene_name(annotation):
                result.add(annotation.text)
        return result
