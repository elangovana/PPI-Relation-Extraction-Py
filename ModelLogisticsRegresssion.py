import tempfile

import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
import numpy as np
import logging
import os

from ModelScorer import ModelScorer


class ModelLogisticsRegression:

    def __init__(self, labels=None, positive_label=True, logs_dir=tempfile.mkdtemp()):
        if labels is None:
            labels = [True, False]

        self.labels = labels

        self.logger = logging.getLogger(__name__)
        self.positive_label = positive_label
        self.logs_dir = logs_dir
        self.model_scorer = ModelScorer(labels=self.labels, logs_dir=self.logs_dir, positive_label=self.positive_label)

    def train(self, matrix_x, vector_y, metadata_v=None, kfold_random_state=None, kfold_n_splits=3):
        class_weight = "balanced"
        model = LogisticRegression(class_weight=class_weight)
        self.logger.info("Class weight %s", class_weight)

        # Log some stats about the class
        unique, counts = np.unique(vector_y, return_counts=True)
        self.logger.info("Unique classes vs counts \n %s", np.asarray((unique, counts)).T)

        # Fit model
        model.fit(matrix_x, vector_y)

        # predict on the training set
        pred = model.predict(matrix_x)
        f_score, p_score, r_score = self.model_scorer.get_scores(vector_y, pred)
        self.logger.info("****Training set confusion")
        self.model_scorer.log_confusion_matrix(self.logger, vector_y, pred, self.labels)
        self.logger.info('Training data f-score %f, p-score %f, r-score %f ', f_score, p_score, r_score)

        # kfold cross validation
        score = self.model_scorer.evalute_kfold_score(matrix_x, model, vector_y, metadata_v, n_splits=kfold_n_splits,
                                                      random_stat=kfold_random_state)

        # Return
        return model, score
