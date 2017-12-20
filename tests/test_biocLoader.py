from unittest import TestCase

from BiocLoader import BiocLoader
import os
from ddt import ddt, data, unpack

@ddt
class TestBiocLoader(TestCase):

    @data(("data/smallTrainingData.xml"))
    def test_parse(self, bioc_file):
        # Arrange
        sut = BiocLoader()
        bioc_file_abs_path=os.path.join(os.path.dirname(__file__), bioc_file)

        #Act
        sut.parse(bioc_file_abs_path)
