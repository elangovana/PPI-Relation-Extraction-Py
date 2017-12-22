from unittest import TestCase
import unittest
import os
from ddt import ddt, data, unpack

from PPIFragmentExtractor import PPIFragementExtractor

@ddt
class TestPPIFragementExtractor(TestCase):

    @data((["ProteinA interacts with ProteinB"], "ProteinA", "ProteinB", ["ProteinA interacts with ProteinB"])
        , (["ProteinB interacts with ProteinA"], "ProteinA", "ProteinB", ["ProteinB interacts with ProteinA"])
          )
    @unpack
    def test_extract(self, sentence_vector, protein1, protein2, expected_frags):
        # arrange
        sut = PPIFragementExtractor()

        # Act
        actual = sut.extract(sentence_vector, protein1, protein2)

        # Assert
        self.assertEquals(expected_frags, actual)
