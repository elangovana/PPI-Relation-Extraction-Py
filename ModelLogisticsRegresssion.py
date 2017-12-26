import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
import numpy as np
import logging


class ModelLogisticsRegression:

    def __init__(self):
        self.n_splits = 5
        self.logger = logging.getLogger(__name__)

    def train(self, matrix_x, vector_y):
        model = LogisticRegression()
        score = self.evalute_kfold_score(matrix_x, model, vector_y)
        model.fit(matrix_x, vector_y)
        return model, score

    def evalute_kfold_score(self, matrix_x, model, vector_y):
        k_fold = KFold(n_splits=self.n_splits, shuffle=True)
        k_fold_scores = []
        for train, test in k_fold.split(matrix_x, vector_y):
            model.fit(matrix_x[train], vector_y[train])
            pred = model.predict(matrix_x[test])

            p_score = sklearn.metrics.precision_score( vector_y[test], pred, labels=['True', 'False'], pos_label='True')
            r_score = sklearn.metrics.recall_score( vector_y[test], pred, labels=['True', 'False'], pos_label='True')
            f_score = sklearn.metrics.f1_score( vector_y[test], pred, labels=['True', 'False'], pos_label='True')
            print(sklearn.metrics.confusion_matrix(vector_y[test], pred))
            self.logger.info('KFold  score %f, precision  %f, recall %f', f_score, p_score, r_score)

            k_fold_scores.append(f_score)

        # return average score
        mean_score = np.mean(k_fold_scores)
        self.logger.info('KFold mean score %f', mean_score)
        return mean_score
