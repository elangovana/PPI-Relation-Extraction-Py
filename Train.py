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


    # training settings
    training_settings = pickle.load(open(training_settings_pickle, "rb"))
    trained_model = training_settings["model"]

    n_grams = training_settings["n-grams"]

    # Run Train
    pipeline = Pipeline(feature_extractor=TransformerNGramFeatureExtractor(
        ngram_extractor=NGramExtractor(vocabulary=n_grams).extract))

    result = pipeline.validate(data, trained_model)

    loader.dump(result)

