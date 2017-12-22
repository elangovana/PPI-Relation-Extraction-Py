from unittest import TestCase

from ddt import data, ddt

from ModelLogisticsRegresssion import ModelLogisticsRegression


@ddt
class TestModelLogisticsRegression(TestCase):


    @data
    def test_train(self):
        #Arrange
        sut = ModelLogisticsRegression()

        #Act
        sut.train()

        #Assert
