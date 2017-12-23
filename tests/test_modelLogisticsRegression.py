from unittest import TestCase
import numpy
from ddt import data, ddt
import numpy as np
from ModelLogisticsRegresssion import ModelLogisticsRegression


@ddt
class TestModelLogisticsRegression(TestCase):

    def test_train(self):
        # Arrange
        sut = ModelLogisticsRegression()
        data_x = np.transpose([range(1, 50), range(1, 50)])
        data_y = np.remainder(data_x[:, 1], 2)

        # Act
        sut.train(data_x, data_y)

        # Assert
