from unittest import TestCase
import unittest
import os
from ddt import ddt, data, unpack

from PPIFragmentExtractor import PPIFragementExtractor


@ddt
class TestPPIFragementExtractor(TestCase):

    @data((["ProteinA interacts with ProteinB"], "ProteinA", "ProteinB", ["interacts with"])
        , (["ProteinB interacts with ProteinA"], "ProteinA", "ProteinB", ["interacts with"])
        , (["ProteinB interacts with ProteinA and does something else"], "ProteinA", "ProteinB", ["interacts with"])
          )
    @unpack
    def test_extract(self, sentence_vector, protein1, protein2, expected_frags):
        # arrange
        sut = PPIFragementExtractor()

        # Act
        actual = sut.extract(sentence_vector, protein1, protein2)

        # Assert
        self.assertEquals(expected_frags, actual)
