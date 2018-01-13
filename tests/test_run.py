import tempfile
from logging.config import fileConfig
from unittest import TestCase

import os
from ddt import data, ddt

import Train


@ddt
class TestRun(TestCase):

    def setUp(self):
        fileConfig(os.path.join(os.path.dirname(__file__), 'logger.ini'))

    @data(  # ("data/training_gold_sentences.xml")
        "data/training_gnorm_with_relation.xml"
    )
    def test_run(self, train_data_file):
        # arrange
        sut = Train.run
        train_file_abs_path = os.path.join(os.path.dirname(__file__), train_data_file)

        #assert
        sut(train_file_abs_path, output_dir=tempfile.mkdtemp(prefix="Train_test_run_"))

