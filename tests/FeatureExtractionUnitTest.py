import unittest
import os
from ddt import ddt, data, unpack

from FeatureExtraction import FeatureExtraction

"""
Unit tests for FeatureExtraction class
"""


@ddt
class FeatureExtractionUnitTest(unittest.TestCase):

    @data(["This is a ngram", "This is also a n gram"])
    def test_should_extract(self, text_vector):
        """
        Should extract features
        :type text_vector: The text vector
        """

        #Arrange
        sut = FeatureExtraction(2)

        #Act
        sut.extract(text_vector)

