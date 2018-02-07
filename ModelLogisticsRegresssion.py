import tempfile

import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
import numpy as np
import logging
import os

from ModelScorer import ModelScorer


class ModelLogisticsRegression:

    def __init__(self, labels=None, positive_label=True, logs_dir=None, scorer=None):
        self.labels = labels or [True, False]
        self.logger = logging.getLogger(__name__)
        self.positive_label = positive_label
        self.logs_dir = logs_dir or tempfile.mkdtemp()
        self.model_scorer = scorer or ModelScorer(labels=self.labels, logs_dir=self.logs_dir,
                                                  positive_label=self.positive_label)

    def train(self, matrix_x, vector_y, metadata_v=None, kfold_random_state=None, kfold_n_splits=3):
        model = self.construct_model()

        # Log some stats about the class
        unique, counts = np.unique(vector_y, return_counts=True)
        self.logger.info("Unique classes vs counts \n %s", np.asarray((unique, counts)).T)

        # Fit model
        model.fit(matrix_x, vector_y)
        self.logger.info(model.coef_)

        # predict on the training set
        pred = model.predict(matrix_x)
        f_score, p_score, r_score = self.model_scorer.get_scores(vector_y, pred)
        self.logger.info("****Training set confusion")
        self.model_scorer.log_confusion_matrix(self.logger, vector_y, pred, self.labels)
        self.logger.info('Training data f-score %f, p-score %f, r-score %f ', f_score, p_score, r_score)

        # evaluate k fold score
        scores = self.model_scorer.evalute_kfold_score(matrix_x, self.construct_model(), vector_y, metadata_v,
                                                      n_splits=kfold_n_splits,
                                                      random_stat=kfold_random_state)
        # Return
        return model, scores

    def construct_model(self):
        class_weight = "balanced"
        self.logger.debug("Constructing logistic regression with class weight %s", class_weight)
        return LogisticRegression(class_weight=class_weight, max_iter=200)
