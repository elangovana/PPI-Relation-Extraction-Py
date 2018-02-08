import os
import tempfile

from BiocLoader import BiocLoader
from NGramExtractor import NGramExtractor
from Pipeline import Pipeline
import cPickle as pickle

from TransformerNGramFeatureExtractor import TransformerNGramFeatureExtractor
from os.path import basename

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

    # Run validation
    pipeline = Pipeline()
    result = pipeline.validate(data, training_settings_pickle)

    #Save results
    output_file = tempfile.mkstemp(prefix= basename(test_data_file), suffix=".xml")[1]
    loader.dump(result, filename=output_file)

