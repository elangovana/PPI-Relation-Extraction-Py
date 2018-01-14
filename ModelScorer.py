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

    def log_confusion_matrix(self, logger, actual, pred, labels, log_level=logging.DEBUG):
        logger.log(log_level, "-------------------------------")
        s = "\t\t"
        for l in labels:
            s = "{}\t\t|{} Pred".format(s, l)
        logger.log(log_level, "|%s|", s)
        cm = sklearn.metrics.confusion_matrix(actual, pred, labels)
        i = 0
        for r in cm:
            s = ""
            for c in r:
                s = "{}\t\t|{}".format(s, c)
            logger.log(log_level, "|%s Actual\t%s|", labels[i], s)
            i = i + 1
        logger.log(log_level, "---------------------------------")

    def evalute_kfold_score(self, matrix_x, model, vector_y, metadata_v=None, n_splits=3, random_stat=None):
        # Initialise
        k_fold = KFold(n_splits=n_splits, shuffle=True, random_state=random_stat)
        k_fold_fscores = []
        k_fold_pscores = []
        k_fold_rscores = []

        for train, test in k_fold.split(matrix_x):
            # fit
            self.logger.debug("****Training set splits for each k fold")
            model.fit(matrix_x[train], vector_y[train])
            self.log_confusion_matrix(self.logger, vector_y[train], model.predict(matrix_x[train]), self.labels)

            # predict the hold out set
            actual = vector_y[test]
            pred = model.predict(matrix_x[test])
            f_score, p_score, r_score = self.get_scores(actual, pred)

            # log
            self.logger.debug("-----Confusion matrix for the hold out set-----")
            self.log_confusion_matrix(self.logger, actual, pred, self.labels)
            self.logger.debug('KFold  score %f, precision  %f, recall %f', f_score, p_score, r_score)
            # log holdout predictions
            logfile = os.path.join(self.logs_dir,
                                   tempfile.mkstemp(prefix="debug_kfold_holdout_", suffix=".csv")[1])
            self.logger.debug('Logging feature and metadata for kth holdout set into file %s', logfile)
            metadata_test =  metadata_v[test] if metadata_v is not None else None
            self._log_kfold_predictions_csv(logfile, matrix_x[test],metadata_test, pred,  actual)

            # save scores
            k_fold_fscores.append(f_score)
            k_fold_pscores.append(p_score)
            k_fold_rscores.append(r_score)

        # return average score
        mean_fscore = np.mean(k_fold_fscores)
        mean_pscore = np.mean(k_fold_pscores)
        mean_rscore = np.mean(k_fold_rscores)
        self.logger.info('KFold mean f-score %f, p-score %f, r-score %f ', mean_fscore, mean_pscore,
                         mean_rscore)
        return mean_fscore, mean_pscore, mean_rscore

    @staticmethod
    def _log_kfold_predictions_csv(logfile, matrix_x, metadata_v, pred, actual):
        # log the files only for debug or above
        if not logging.getLogger().isEnabledFor(logging.DEBUG):
            return

        data = np.concatenate((
            np.array(actual).reshape(len(actual), 1),
            np.array(pred).reshape(len(pred), 1)), axis=1)
        #, matrix_x
        if metadata_v is not None:
            data = np.concatenate((metadata_v, data), axis=1 )

        np.savetxt(logfile, data, delimiter='|', fmt="%s")

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
