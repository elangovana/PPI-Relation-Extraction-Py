from sklearn.feature_extraction.text import CountVectorizer


class FeatureExtraction:

    def __init__(self, n_gram_len=3):
        """

        :param n_gram_len: the size of n-gram where each gram is a word
        """
        self.n_gram_len = n_gram_len

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

        return (data_features)
