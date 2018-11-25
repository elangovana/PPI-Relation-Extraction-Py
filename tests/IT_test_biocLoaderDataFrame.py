from io import StringIO
from logging.config import fileConfig
from unittest import TestCase

from BiocLoaderDataFrame import BiocLoaderDataFrame
import os
from ddt import ddt, data


@ddt
class TestBiocLoaderDataFrame(TestCase):

    def setUp(self):
        fileConfig(os.path.join(os.path.dirname(__file__), 'logger.ini'))

    @data(  # ("data/training_gold_sentences.xml")
        ("data/training_gnorm_with_relation.xml")
    )
    def test_parse(self, bioc_file):
        # Arrange
        sut = BiocLoaderDataFrame()
        bioc_file_abs_path = os.path.join(os.path.dirname(__file__), bioc_file)

        # Act
        actual = sut.parse(bioc_file_abs_path)

        self.assertIsNotNone(actual)

    @data(  # ("data/training_gold_sentences.xml")
        ("data/training_gnorm_with_relation.xml")
    )
    def test_dump(self, bioc_file):
        # Arrange
        sut = BiocLoaderDataFrame()
        bioc_file_abs_path = os.path.join(os.path.dirname(__file__), bioc_file)
        out_handle= StringIO()

        # Act
        dataframe = sut.parse(bioc_file_abs_path)
        sut.dump(dataframe, out_handle)





