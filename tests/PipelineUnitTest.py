import unittest
import os
from ddt import ddt, data, unpack

"""
Unit tests for Pipeline class
"""


@ddt
class PipelineUnitTest(unittest.TestCase):

    @data("data/smallTrainingData.xml")
    def test_should_train(self, train_file_path):
        """
        Should train data
        :type train_file_path: The training file
        """
        train_file_abs_path = os.path.join(os.path.dirname(__file__), train_file_path)
        self.assertEquals(os.path.exists(train_file_abs_path), True,
                          "The file {} does not exist".format(train_file_abs_path))
