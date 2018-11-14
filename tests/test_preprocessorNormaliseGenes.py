from unittest import TestCase

from ddt import data, unpack, ddt

from PreprocessorNormaliseGenes import PreprocessorNormaliseGenes


@ddt
class TestPreprocessorNormaliseGenes(TestCase):

    @data(
        [["This is sentence 1 with gene1 from passage 1"]
            , "gene1", "normgene1", ["This is sentence 1 with normgene1 from passage 1"]]
    )
    @unpack
    def test_normalise_gene_names(self, v_sentences, gene, norm_gene, expected_v_sentences):
        # Arrange
        sut = PreprocessorNormaliseGenes()

        # Act
        actual = sut.normalise_gene_names(v_sentences, gene, norm_gene)

        # Assert
        self.assertEqual(expected_v_sentences, actual)

    @data(
        (["This is sentence 1 with gene1 from passage 1"]
         , {"gene1": "normgene1"},
         ["This is sentence 1 with normgene1 from passage 1"])

        , (["This is sentence 1 with gene1 from passage 1", "This is sentence 1 with gene1 from passage 2"]
           , {"gene1": "normgene1"},
           ["This is sentence 1 with normgene1 from passage 1", "This is sentence 1 with normgene1 from passage 2"])
    )
    @unpack
    def test_normalise_gene_names_bulk(self, v_sentences, dict, expected_v_sentences):
        # Arrange
        sut = PreprocessorNormaliseGenes()

        # Act
        actual = sut.normalise_gene_names_bulk(v_sentences, dict)

        # Assert
        self.assertEqual(expected_v_sentences, actual)
