from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold


class ModelLogisticsRegression:

    def __init__(self):
        pass

    def train(self, matrix_x, vector_y):
        model = LogisticRegression()
        k_fold = KFold(n_splits=2)

        for k, (train, test) in enumerate(k_fold.split(matrix_x, vector_y)):
            model.fit(matrix_x[train], vector_y[train])
            print("[fold {0}] alpha: {1:.5f}, score: {2:.5f}".
                format(k, model.coef_, model.score(matrix_x[test], vector_y[test])))
