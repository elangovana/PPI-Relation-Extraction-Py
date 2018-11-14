import logging
import tempfile
from logging.config import fileConfig
from unittest import TestCase

import numpy as np
from ddt import ddt, data, unpack
from sklearn.linear_model import LogisticRegression
import os

from ModelScorer import ModelScorer


@ddt
class TestModelScorer(TestCase):

    @classmethod
    def setUpClass(cls):
        fileConfig(os.path.join(os.path.dirname(__file__), 'logger.ini'))

    @data((None, None, logging.DEBUG)
        , (True, None, logging.DEBUG)
        , (True, 42, logging.DEBUG)
        , (None, None, logging.INFO)
          )
    @unpack
    def test_evalute_kfold_score(self, metadata_v, random_state, log_level):
        # Arrange
        len = 1000
        sut = ModelScorer(labels=[0, 1], positive_label=1, logs_dir=tempfile.mkdtemp(prefix="test_evalute_kfold_score"))
        matrix_x = np.random.randint(low=10, high=100, size=(len, 2))
        vector_y = np.random.randint(low=0, high=2, size=(len, 1)).ravel()
        logging.getLogger().setLevel(log_level)

        model = LogisticRegression()
        if metadata_v:
            metadata_v = np.random.randint(low=10, high=100, size=(len, 2))

        # Act
        sut.evalute_kfold_score(matrix_x=matrix_x, model=model, vector_y=vector_y, metadata_v=metadata_v,
                                random_stat=random_state)
