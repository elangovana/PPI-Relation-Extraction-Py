from unittest import TestCase

from bioc import BioCDocument, BioCAnnotation, BioCPassage
from ddt import data, ddt

from BiocAnnotationGenes import BiocAnnotationGenes

@ddt
class TestBiocAnnotationGenes(TestCase):

    @data({"type":"Gene", "NCBI Gene":"Key3"})
    def test_should_get_gene_names(self, dict):
        # Arrange
        sut = BiocAnnotationGenes()
        bioc_doc = BioCDocument()
        bioc_passage = BioCPassage()
        annotation = BioCAnnotation()
        annotation.infons = dict
        bioc_passage.add_annotation(annotation)
        bioc_doc.add_passage(bioc_passage)

        #act
        actual = sut.get_gene_names(bioc_doc)

        #assert
        self.assertEqual( 1, len(actual))
