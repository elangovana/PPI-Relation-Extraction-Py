from unittest import TestCase

from bioc import BioCDocument, BioCAnnotation, BioCPassage
from ddt import data, ddt, unpack

from BiocAnnotationGenes import BiocAnnotationGenes


@ddt
class TestBiocAnnotationGenes(TestCase):

    @data(
        ([{"type": "Gene", "NCBI GENE": "8183"}, {"type": "Non-Gene", "NCBI GENE": "81833"}]
         , ["8183"]
         )
        , ([{"type": "Gene", "NCBI GENE": "8183"}]
           , ["8183"]
           )
        , ([{"type": "Gene", "NCBI GENE": "8183"}, {"type": "Gene", "NCBI GENE": "81834"}]
           , ["8183", "81834"])
    )
    @unpack
    def test_should_get_gene_names_normalised(self, list_dict, expected_genes):
        # Arrange
        sut = BiocAnnotationGenes()
        bioc_doc = BioCDocument()
        bioc_passage = BioCPassage()
        bioc_doc.add_passage(bioc_passage)

        for dict in list_dict:
            annotation = BioCAnnotation()
            annotation.infons = dict
            bioc_passage.add_annotation(annotation)

        # act
        actual = sut.get_gene_names_normalised(bioc_doc)

        # assert
        self.assertEqual(set(expected_genes), actual)

    @data(([{"type": "Gene", "NCBI GENE": "8183", "text": "klk3"}]
           , ["klk3"]
           )
          )
    @unpack
    def test_should_get_gene_names(self, list_dict, expected_genes):
        # Arrange
        sut = BiocAnnotationGenes()
        bioc_doc = BioCDocument()
        bioc_passage = BioCPassage()
        bioc_doc.add_passage(bioc_passage)

        for dict in list_dict:
            annotation = BioCAnnotation()
            annotation.text = dict["text"]
            annotation.infons = dict
            bioc_passage.add_annotation(annotation)

        # act
        actual = sut.get_gene_names(bioc_doc)

        # assert
        self.assertEqual(set(expected_genes), actual)
