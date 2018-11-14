from logging.config import fileConfig
from unittest import TestCase

from source.BiocLoader import BiocLoader
import os
from ddt import ddt, data


@ddt
class TestBiocLoader(TestCase):

    def setUp(self):
        fileConfig(os.path.join(os.path.dirname(__file__), 'logger.ini'))

    @data(  # ("data/training_gold_sentences.xml")
        ("data/training_gnorm_with_relation.xml")
    )
    def test_parse(self, bioc_file):
        # Arrange
        sut = BiocLoader()
        bioc_file_abs_path = os.path.join(os.path.dirname(__file__), bioc_file)

        # Act
        actual = sut.parse(bioc_file_abs_path)

        self.assertIsNotNone(actual)



    def test_dump(self):
        # Arrange
        sut = BiocLoader()
        data_rows = [["Doc1#Gene1A#Gene2A", "DocId1", "Gene1A", "Gene2A", True],["Doc2#Gene2B#Gene2B", "DocId2", "Gene1B", "Gene2B", True] ]

        # Act
        actual = sut.dump(data_rows)

