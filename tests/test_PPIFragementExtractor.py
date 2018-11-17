from unittest import TestCase
from ddt import ddt, data, unpack

from PPIFragmentExtractor import PPIFragementExtractor


@ddt
class TestPPIFragementExtractor(TestCase):

    @data((["ProteinA interacts with ProteinB"], "ProteinA", "ProteinB",[], ["interacts with"])
        , (["ProteinB interacts with ProteinA"], "ProteinA", "ProteinB",[], ["interacts with"])
        , (["ProteinB interacts with ProteinA and does something else"], "ProteinA", "ProteinB",[], ["interacts with"])
        , (["ProteinB (ProteinB) interacts with ProteinA and does something else"], "ProteinA", "ProteinB",["ProteinA", "ProteinB"], ["() interacts with"])

          )
    @unpack
    def test_extract(self, sentence_vector, protein1, protein2, remove_words, expected_frags):
        # arrange
        sut = PPIFragementExtractor()

        # Act
        actual = sut.extract(sentence_vector, protein1, protein2, remove_words)

        # Assert
        self.assertEqual(expected_frags, actual)
