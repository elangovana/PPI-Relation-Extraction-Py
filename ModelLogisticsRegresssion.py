import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
import numpy as np
import logging


class ModelLogisticsRegression:

    def __init__(self, labels = [True, False], positive_label=True):
        self.n_splits = 3
        self.logger = logging.getLogger(__name__)
        self.labels = labels
        self.positive_label = positive_label

    def train(self, matrix_x, vector_y):
        class_weight = None #"balanced"
        model = LogisticRegression(class_weight=class_weight)
        self.logger.info("Class weight %s",class_weight)

        #model = LogisticRegression()

        #Log some stats about the class
        unique, counts = np.unique(vector_y, return_counts=True)
        self.logger.info("Unique classes vs counts \n %s", np.asarray((unique, counts)).T)

        model.fit(matrix_x, vector_y)

        # predict on the training set
        pred = model.predict(matrix_x)
        f_score, p_score, r_score = self.get_scores(vector_y, pred)
        self.logger.info("****Training set confusion")
        self._log_confusion_matrix(vector_y, pred, self.labels)
        self.logger.info('Training data f-score %f, p-score %f, r-score %f ', f_score, p_score, r_score)
        # kfold cross validation
        score = self.evalute_kfold_score(matrix_x, model, vector_y)
        return model, score

    def evalute_kfold_score(self, matrix_x, model, vector_y):
        k_fold = KFold(n_splits=self.n_splits, shuffle=True, random_state=42)
        k_fold_fscores = []
        k_fold_pscores = []
        k_fold_rscores = []

        for train, test in k_fold.split(matrix_x):
            self.logger.info("****Training set splits for each k fold")
            model.fit(matrix_x[train], vector_y[train])
            self._log_confusion_matrix(vector_y[train], model.predict(matrix_x[train]), self.labels)

            # predict the hold out set
            actual = vector_y[test]
            pred = model.predict(matrix_x[test])
            f_score, p_score, r_score = self.get_scores(actual, pred)
            self.logger.info("-----Confusion matrx for the hold out set-----")
            self._log_confusion_matrix(actual, pred, self.labels)
            self.logger.info('KFold  score %f, precision  %f, recall %f', f_score, p_score, r_score)

            k_fold_fscores.append(f_score)
            k_fold_pscores.append(p_score)
            k_fold_rscores.append(r_score)
        # return average score
        mean_score = np.mean(k_fold_fscores)
        self.logger.info('KFold mean f-score %f, p-score %f, r-score %f ', mean_score, p_score, r_score)
        return mean_score

    def get_scores(self, actual, pred):
        """
Computes F-score (harmonic mean), Precision and Recall
        :param actual: The actual result, the labels are passed in the constructor
        :param pred: The predicted
        :return: returns f_score, p_score, r_score
        """
        p_score = sklearn.metrics.precision_score(actual, pred, self.labels, pos_label=self.positive_label)
        r_score = sklearn.metrics.recall_score(actual, pred, self.labels, pos_label=self.positive_label)
        f_score = sklearn.metrics.f1_score(actual, pred, self.labels, pos_label=self.positive_label)
        return f_score, p_score, r_score

    def _log_confusion_matrix(self, actual, pred, labels):
        self.logger.info("-------------------------------")
        s = "\t\t"
        for l in labels:
            s = "{}\t\t|{} Pred".format(s, l)
        self.logger.info("|%s|", s)
        cm = sklearn.metrics.confusion_matrix(actual, pred, labels)
        i = 0
        for r in cm:
            s = ""
            for c in r:
                s = "{}\t\t|{}".format(s, c)
            self.logger.info("|%s Actual\t%s|", labels[i], s)
            i = i + 1
        self.logger.info("---------------------------------")
