from sklearn.feature_extraction.text import CountVectorizer
import logging
import  numpy as np
import tempfile
import os
class NGramFeatureExtractor:

    def __init__(self, n_gram_len=1, logs_dir = tempfile.mkdtemp()):
        """

        :param n_gram_len: the size of n-gram where each gram is a word
        """
        self.n_gram_len = n_gram_len
        self.logs_dir = logs_dir
        self.logger =logging.getLogger(__name__)

    def extract(self, text_vector):
        """
        Extracts  features.
        :rtype: vector
        :param text_vector: a vector of text blocks
        :return: returns a vector of features
        """
        vectorizer = CountVectorizer(analyzer="word", binary=True,
                                     ngram_range=(self.n_gram_len, self.n_gram_len))

        data_features = vectorizer.fit_transform(text_vector).toarray()
        logs_features_file = os.path.join(self.logs_dir, tempfile.mkstemp(suffix=".csv")[1])
        self.logger.info("Writing N Gram features  to log file %s", logs_features_file)
        np.savetxt(logs_features_file, np.array(vectorizer.get_feature_names()), fmt="%s")


        return data_features
