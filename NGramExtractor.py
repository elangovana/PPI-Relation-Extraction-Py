import nltk as nltk
from sklearn.feature_extraction.text import CountVectorizer
import logging
import numpy as np
import tempfile
import os


class NGramExtractor(CountVectorizer):

    def __init__(self, n_gram_len=1, vocabulary=None, logs_dir=tempfile.mkdtemp(), stop_words='english'):
        """

        :param n_gram_len: the size of n-gram where each gram is a word
        """
        super(NGramExtractor, self).__init__(analyzer="word", binary=True,
                                             ngram_range=(n_gram_len, n_gram_len), vocabulary=vocabulary, max_features = 5, stop_words=stop_words)
        self.n_gram_len = n_gram_len
        self.logs_dir = logs_dir
        self.logger = logging.getLogger(__name__)


    def build_analyzer(self):
        analyzer = super(NGramExtractor, self).build_analyzer()
        return lambda doc: ([nltk.stem.SnowballStemmer('english').stem(w) for w in analyzer(doc)])

    def extract(self, text_vector):
        """
        Extracts  features.
        :rtype: vector
        :param text_vector: a vector of text blocks
        :return: returns a vector of features
        """
        vectorizer = self

        data_features = vectorizer.fit_transform(text_vector).toarray()
        logs_features_file = os.path.join(self.logs_dir, tempfile.mkstemp(suffix=".csv")[1])
        self.logger.info("Writing N Gram features  to log file %s", logs_features_file)
        np.savetxt(logs_features_file, np.array(vectorizer.get_feature_names()), fmt="%s")



        return data_features, vectorizer.get_feature_names()


