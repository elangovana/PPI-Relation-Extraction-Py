import os

from BiocLoader import BiocLoader
from NGramExtractor import NGramExtractor
from Pipeline import Pipeline
import cPickle as pickle

from TransformerNGramFeatureExtractor import TransformerNGramFeatureExtractor


def run(training_data_file, output_dir):
    # Parse data
    loader = BiocLoader()
    data = loader.parse(training_data_file)

    # Run Train
    pipeline = Pipeline()
    return pipeline.run_model(data_rows=data, output_dir=output_dir)


def validate(training_settings_pickle, test_data_file, output_dir):
    # Parse data
    loader = BiocLoader()
    data = loader.parse(test_data_file)


    # Run Train
    pipeline = Pipeline()

    result = pipeline.validate(data, training_settings_pickle)

    loader.dump(result)

