import unittest
import os
from ddt import ddt, data, unpack
from logging.config import fileConfig
from NGramFeatureExtractor import NGramFeatureExtractor

"""
Unit tests for FeatureExtraction class
"""


@ddt
class TestNGramFeatureExtractor(unittest.TestCase):

    def setUp(self):
        fileConfig(os.path.join(os.path.dirname(__file__), 'logger.ini'))

    @data((["This is a ngram", "This is also a ngram"], 2, 4)
        , (["This is apple"], 3, 1)
        , (["Jack is a ngram"], 1, 3)
        , (["This"], 1, 1)
          # , (["This is apple. This is banna"], 3, 2) # Expect n-grams shouldn't span sentences
          )
    @unpack
    def test_should_extract_ngrams(self, text_vector, n_gram_size, expected_no_of_ngrams):
        """
        Should extract features
        :type text_vector: The text vector
        """

        # Arrange
        sut = NGramFeatureExtractor(n_gram_size)

        # Act
        actual = sut.extract(text_vector)

        # Assert
        actual_dim = len(actual.shape)
        self.assertEquals(actual_dim, 2, "Expecting a 2 dimensional array, instead found {}".format(actual_dim))
        self.assertEquals(actual.shape[1], expected_no_of_ngrams)
        self.assertEquals(actual.shape[0], len(text_vector))
