import unittest
import os
from ddt import ddt, data, unpack

from FeatureExtraction import FeatureExtraction

"""
Unit tests for FeatureExtraction class
"""


@ddt
class FeatureExtractionUnitTest(unittest.TestCase):

    @data((["This is a ngram", "This is also a ngram"], 2, 4)
          ,(["This is apple"], 3, 1)
          ,(["Jack is a ngram"],1, 3)
        , (["This"], 1, 1)
          )
    @unpack
    def test_should_extract(self, text_vector, n_gram, expected_columns):
        """
        Should extract features
        :type text_vector: The text vector
        """

        #Arrange
        sut = FeatureExtraction(n_gram)

        #Act
        actual = sut.extract(text_vector)
        print(actual)

        #Assert
        actual_dim = len(actual.shape)
        self.assertEquals(actual_dim, 2, "Expecting a 2 dimensional array, instead found {}".format(actual_dim))
        self.assertEquals(actual.shape[1], expected_columns)
        self.assertEquals(actual.shape[0], len(text_vector))



