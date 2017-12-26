import bioc

NCBI_GENE = "NCBI GENE"

GENE = "Gene"

"""
A wrapper for BiocAnnotationGenes
"""


class BiocAnnotationGenes:
    def __init__(self):
        pass

    def get_gene_names_normalised(self, bioc_element):
        """
Returns NCBI gene ids from a document or a passage  by inspecting at the annotations
        :param bioc_element: A bioc document or a passage
        :return: a list of NCBI genes
        """
        gene_type = NCBI_GENE
        if isinstance(bioc_element, bioc.BioCDocument):
            return self._get_gene_name_normalised_document(bioc_element, gene_type)
        else:
            return self._get_gene_name_normalised_passage(bioc_element, gene_type)

    def get_gene_names(self, bioc_element):
        """
Returns the gene names from a document or a passage by inspecting at the annotations
        :param bioc_element: A bioc document or a passage
        :return: A list of gene names
        """
        if isinstance(bioc_element, bioc.BioCDocument):
            return self._get_gene_names_document(bioc_element)
        else:
            return self._get_gene_names_passage(bioc_element)

    def get_normalised_gene_name(self, doc, gene):
        """
Returns the normalised gene name given the normal gene name
        :param doc: bioc document
        :param gene: the unnormalised gene name
        :return: normalised gene name
        """
        for bioc_passage in doc.passages:
            for annotation in bioc_passage.annotations:
                if self.is_annotation_gene(annotation) and annotation.text == gene:
                    return annotation.infons[NCBI_GENE]
        return None


    @staticmethod
    def is_annotation_gene(annotation):
        return annotation.infons["type"] == GENE

    def get_gene_names_to_normalised_dict(self, doc):
        """
Returns a dictionary of gene to normalised id by parsing the annotations in the bioc doc
        :param doc:Bioc Document
        :return: Returns a dictionary of gene to normalised id by parsing the annotations in the bioc doc
        """
        result = {}
        gene_names = self.get_gene_names(doc)
        for g in gene_names:
            result[g] = self.get_normalised_gene_name(doc, g)
        return  result


    def _get_gene_name_normalised_document(self, bioc_doc,  gene_type=None):
        result = set()
        for passage in bioc_doc.passages:
            result = result.union(self._get_gene_name_normalised_passage(passage, gene_type))
        return result

    def _get_gene_name_normalised_passage(self, bioc_passage, gene_type=NCBI_GENE):
        result = set()
        for annotation in bioc_passage.annotations:
            if self.is_annotation_gene(annotation):
                result.add(annotation.infons[gene_type])
        return result

    def _get_gene_names_document(self, bioc_doc):
        result = set()
        for passage in bioc_doc.passages:
            result = result.union(self._get_gene_names_passage(passage))
        return result

    def _get_gene_names_passage(self, bioc_passage):
        result = set()
        for annotation in bioc_passage.annotations:
            if self.is_annotation_gene(annotation):
                result.add(annotation.text)
        return result

    def _get_normalised_gene_name_document(self, bioc_element, gene):
        pass
