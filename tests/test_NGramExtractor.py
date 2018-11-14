import unittest
import os

import numpy as np
from ddt import ddt, data, unpack
from logging.config import fileConfig
from source.NGramExtractor import NGramExtractor

"""
Unit tests for FeatureExtraction class
"""


@ddt
class TestNGramExtractor(unittest.TestCase):

    def setUp(self):
        fileConfig(os.path.join(os.path.dirname(__file__), 'logger.ini'))

    @data((["This is a ngram ", "This is also a ngram"], 2, None, 4)
        , (["This is apple"], 3, None, 1)
        , (["This is stemming"], 3, None, 1)
        , (["Jack is a ngram"], 1, None, 3)
        , (["This"], 1, None, 1)
        , (["This"], 1, ["Noterm"], 1)
          # , (["This is apple. This is banna"], 3, 2) # Expect n-grams shouldn't span sentences
          )
    @unpack
    def test_should_extract__correct_number_of_ngrams(self, text_vector, n_gram_size, vocabulary,
                                                      expected_no_of_ngrams):
        """
        Should extract features
        :type text_vector: The text vector
        """

        # Arrange
        sut = NGramExtractor(n_gram_size, vocabulary=vocabulary, stop_words=None)

        # Act
        actual, feature_names = sut.extract(text_vector)

        # Assert
        actual_dim = len(actual.shape)
        self.assertEquals(actual_dim, 2, "Expecting a 2 dimensional array, instead found {}".format(actual_dim))
        self.assertEquals(actual.shape[1], expected_no_of_ngrams)
        self.assertEquals(actual.shape[0], len(text_vector))

    @data((["This is apple"], 3, None, [[1]])
        , (["This is stemming"], 3, None, [[1]])
        , (["Jack is a ngram", "ngram"], 1, None, [[1, 1, 1, ], [0, 0, 1]])
        , (["This"], 1, None, [[1]])
        , (["This is non existent"], 1, ["Noterm"], [[0]])
        , (["This is non stemming"], 1, ["stem", "this"], [[1, 1]])
          # , (["This is apple. This is banna"], 3, 2) # Expect n-grams shouldn't span sentences
          )
    @unpack
    def test_should_extract_ngrams_vector(self, text_vector, n_gram_size, vocabulary, expected_ngrams_vector):
        """
        Should extract features
        :type text_vector: The text vector
        """

        # Arrange
        sut = NGramExtractor(n_gram_size, vocabulary=vocabulary,stop_words=None)

        # Act
        actual, feature_names = sut.extract(text_vector)

        # Assert
        actual_dim = len(actual.shape)
        self.assertEquals(actual_dim, 2, "Expecting a 2 dimensional array, instead found {}".format(actual_dim))
        self.assertEqual(actual.flatten().tolist(), np.array(expected_ngrams_vector).flatten().tolist())
