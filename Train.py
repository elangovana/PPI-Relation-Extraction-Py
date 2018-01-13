import os

from BiocLoader import BiocLoader
from NGramFeatureExtractor import NGramFeatureExtractor
from Pipeline import Pipeline
import cPickle as pickle

def run(training_data_file, output_dir):
    # Parse data
    loader = BiocLoader()
    data = loader.parse(training_data_file)

    # Run Train
    pipeline = Pipeline()
    pipeline.run_model(data_rows=data, output_dir=output_dir)


def validate(training_settings_pickle, test_data_file, output_dir):
    # Parse data
    loader = BiocLoader()
    data = loader.parse(test_data_file)

    #training settings
    training_settings = pickle.load(open(training_settings_pickle, "rb"))
    trained_model = training_settings["model"]

    n_grams = training_settings["n-grams"]

    # Run Train
    pipeline = Pipeline(preprocessor_ngram_feature_extractor=NGramFeatureExtractor(vocabulary=n_grams))

    pipeline.validate(data, trained_model)
