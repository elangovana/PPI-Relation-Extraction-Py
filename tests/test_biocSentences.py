import logging
from logging.config import fileConfig
from unittest import TestCase

import os
from ddt import ddt, data, unpack

from BiocSentences import BiocSentences
import bioc


@ddt
class TestBiocSentences(TestCase):

    def setUp(self):
        fileConfig(os.path.join(os.path.dirname(__file__), 'logger.ini'))

    @data(
        [["This is sentence 1 from passage 1", "This is sentence 2 from passage 1"]
            , ["This is sentence 1 from passage 2"]]
    )
    def test_convert_to_vec(self, bioc_doc_input):
        # Arrange
        expected_vec = []
        sut = BiocSentences()
        doc = bioc.BioCDocument()
        # construct a bioc doc object given the input array
        for p in bioc_doc_input:
            bioc_p = bioc.BioCPassage()
            doc.add_passage(bioc_p)
            for s in p:
                bioc_p.add_sentence(s)
                expected_vec.append(s)

        # Act
        actual = sut.convert_to_vec(doc)

        # Assert
        self.assertEqual(expected_vec, actual)
