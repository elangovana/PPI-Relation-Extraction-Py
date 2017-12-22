import unittest
import os
from ddt import ddt, data, unpack

from NGramFeatureExtraction import NGramFeatureExtraction

"""
Unit tests for FeatureExtraction class
"""


@ddt
class TestNGramFeatureExtraction(unittest.TestCase):

    @data((["This is a ngram", "This is also a ngram"], 2, 4)
        , (["This is apple"], 3, 1)
        , (["Jack is a ngram"], 1, 3)
        , (["This"], 1, 1)
          )
    @unpack
    def test_should_extract_ngrams(self, text_vector, n_gram, expected_no_columns):
        """
        Should extract features
        :type text_vector: The text vector
        """

        # Arrange
        sut = NGramFeatureExtraction(n_gram)

        # Act
        actual = sut.extract(text_vector)

        # Assert
        actual_dim = len(actual.shape)
        self.assertEquals(actual_dim, 2, "Expecting a 2 dimensional array, instead found {}".format(actual_dim))
        self.assertEquals(actual.shape[1], expected_no_columns)
        self.assertEquals(actual.shape[0], len(text_vector))
