import logging
from unittest import TestCase
import numpy
from ddt import data, ddt
import numpy as np
from ModelLogisticsRegresssion import ModelLogisticsRegression
from logging.config import fileConfig
import os

@ddt
class TestModelLogisticsRegression(TestCase):

    def setUp(self):
        fileConfig(os.path.join(os.path.dirname( __file__), 'logger.ini'))
        self.logger = logging.getLogger(__name__)


    def test_train(self):
        # Arrange
        self.logger.debug("Running test to arrange")
        sut = ModelLogisticsRegression()
        mn, mx = 1, 50
        data_x = np.transpose([range(mn, mx), range(mn, mx)])
        data_y = data_x[:, 1] > (mx - mn) / 2

        # Act
        actual_model, actual_score = sut.train(data_x, data_y)

        # Assert
        self.assertIsNotNone(actual_model)
        self.assertTrue(0 <= actual_score <= 1.0,
                        "The actual score must be between one and zero, but is {}".format(actual_score))
