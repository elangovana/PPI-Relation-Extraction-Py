from unittest import TestCase

from bioc import BioCDocument, BioCRelation
from ddt import ddt, unpack, data

from BiocRelation import BiocRelation


@ddt
class TestBiocRelation(TestCase):

    @data(([{"Gene1":"1", "Gene2":"2"}], "1","2", True)
          )
    @unpack
    def test_is_valid(self, relations_infons, gene1, gene2, expected):
        #arrange
        sut = BiocRelation()
        doc = BioCDocument()

        for dict in relations_infons:
            relation = BioCRelation()
            relation.infons = dict
            doc.add_relation(relation)


        #Act
        actual = sut.is_valid(doc, gene1, gene2)
        
        #Assert
        self.assertEqual(expected, actual)
