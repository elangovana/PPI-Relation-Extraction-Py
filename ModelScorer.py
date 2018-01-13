import logging
import os
import tempfile

import numpy as np
import sklearn
from sklearn.model_selection import KFold


class ModelScorer:

    def __init__(self, labels, positive_label, logs_dir):
        self.logs_dir = logs_dir
        self.positive_label = positive_label
        self.labels = labels
        self.logger = logging.getLogger(__name__)

    def log_confusion_matrix(self, logger, actual, pred, labels):
        logger.info("-------------------------------")
        s = "\t\t"
        for l in labels:
            s = "{}\t\t|{} Pred".format(s, l)
        logger.info("|%s|", s)
        cm = sklearn.metrics.confusion_matrix(actual, pred, labels)
        i = 0
        for r in cm:
            s = ""
            for c in r:
                s = "{}\t\t|{}".format(s, c)
            logger.info("|%s Actual\t%s|", labels[i], s)
            i = i + 1
        logger.info("---------------------------------")

    def evalute_kfold_score(self, matrix_x, model, vector_y, metadata_v=None, n_splits=3, random_stat=None):
        # Initialise
        k_fold = KFold(n_splits=n_splits, shuffle=True, random_state=random_stat)
        k_fold_fscores = []
        k_fold_pscores = []
        k_fold_rscores = []

        for train, test in k_fold.split(matrix_x):
            # fit
            self.logger.info("****Training set splits for each k fold")
            model.fit(matrix_x[train], vector_y[train])
            self.log_confusion_matrix(self.logger, vector_y[train], model.predict(matrix_x[train]), self.labels)

            # predict the hold out set
            actual = vector_y[test]
            pred = model.predict(matrix_x[test])
            f_score, p_score, r_score = self.get_scores(actual, pred)

            # log
            self.logger.info("-----Confusion matrx for the hold out set-----")
            self.log_confusion_matrix(self.logger, actual, pred, self.labels)
            self.logger.info('KFold  score %f, precision  %f, recall %f', f_score, p_score, r_score)
            # log holdout pred
            logfile = os.path.join(self.logs_dir,
                                   tempfile.mkstemp(prefix="debug_kfold_holdout_", suffix=".csv")[1])
            self.logger.info('Logging feature and metadata for kth holdout set into file %s', logfile)

            # TODO cleanup
            if metadata_v is not None:
                np.savetxt(logfile, np.concatenate((metadata_v[test],
                                                    np.array(vector_y[test]).reshape(len(vector_y[test]), 1),
                                                    np.array(pred).reshape(len(pred), 1), matrix_x[test]), axis=1),
                           delimiter='|', fmt="%s")
            else:
                np.savetxt(logfile, np.concatenate((
                    np.array(vector_y[test]).reshape(len(vector_y[test]), 1),
                    np.array(pred).reshape(len(pred), 1), matrix_x[test]), axis=1),
                           delimiter='|', fmt="%s")

            # save scores
            k_fold_fscores.append(f_score)
            k_fold_pscores.append(p_score)
            k_fold_rscores.append(r_score)

        # return average score
        mean_score = np.mean(k_fold_fscores)
        self.logger.info('KFold mean f-score %f, p-score %f, r-score %f ', mean_score, np.mean(k_fold_pscores),
                         np.mean(k_fold_rscores))
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

        self.log_confusion_matrix(self.logger, actual, pred, self.labels)
        return f_score, p_score, r_score
