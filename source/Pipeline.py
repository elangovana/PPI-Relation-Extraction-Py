"""
This is the main pipeline class for relation extraction.
"""
import collections
import logging
import tempfile

import numpy as np
import os
import pickle

from sklearn.model_selection import KFold

from source.BiocLoader import I_GENE1, I_GENE2, I_RELATIONS
from source.BiocRelation import BiocRelation
from source.ModelLogisticsRegresssion import ModelLogisticsRegression
from source.ModelScorer import ModelScorer
from source.PostProcessingSelfRelation import PostProcessingSelfRelation
from source.TransformerNGramFeatureExtractor import TransformerNGramFeatureExtractor


class Pipeline:

    def __init__(self, model=None, logs_dir=tempfile.mkdtemp(), feature_extractor=TransformerNGramFeatureExtractor()):
        self.logs_dir = logs_dir
        self.logger = logging.getLogger(__name__)
        self.validate_relation = BiocRelation().is_valid
        self.feature_extractor = feature_extractor
        self.model = model or ModelLogisticsRegression()

    def _save_to_file(self, logs_features_file, column_names, columnr_data_to_merge):
        c_names = []
        for c in column_names:
            c_names.extend(c)

        data = columnr_data_to_merge[0]

        for i in range(1, len(columnr_data_to_merge)):

            if isinstance(columnr_data_to_merge[i][0], np.ndarray):
                w = columnr_data_to_merge[i].shape[1]

            elif isinstance(columnr_data_to_merge[i][0], collections.Sequence):
                w = len(columnr_data_to_merge[i][0])
            else:
                w = 1

            data = np.concatenate((data, np.array(columnr_data_to_merge[i]).reshape(len(columnr_data_to_merge[i]), w)),
                                  axis=1)

        data = np.concatenate((np.array(c_names).reshape(1, len(c_names)), data), axis=0)

        np.savetxt(logs_features_file, data, delimiter='|', fmt="%s")

    def run_model(self, data_rows, output_dir):

        result = self.feature_extractor.extract(data_rows)
        metadata_names = result[self.feature_extractor.key_metadata_names]
        feature_names = result[self.feature_extractor.key_feature_names]
        features = result[self.feature_extractor.key_feature]
        metadata = result[self.feature_extractor.key_metadata]

        self.logger.debug("Total number of features used %s. Feature names:\n %s",
                          len(feature_names),
                          "\n".join(feature_names))
        # labels
        labels = np.array(self.get_labels(data_rows))
        distinct_labels = np.unique(labels)
        positive_label = True

        # Train model
        random_state = 42
        kfold_splits = 5
        trained_model, holdout_f_score = self.model.train(features, labels, metadata_v=metadata,
                                                          kfold_random_state=random_state, kfold_n_splits=kfold_splits)
        predicted_on_train = trained_model.predict(features)

        # persist trained model
        pickle_file_name = os.path.join(output_dir, tempfile.mkstemp(prefix="trained_model")[1])
        self.logger.info("Saving model to %s", pickle_file_name)
        with open(pickle_file_name, 'wb') as fd:
            pickle.dump({"model": trained_model, "feature_extractor": self.feature_extractor}, fd)

        # log formatted features to file
        logs_features_file = os.path.join(self.logs_dir,
                                          tempfile.mkstemp(prefix="data_formatted_features", suffix=".csv")[1])

        self.logger.info("Writing train features labels and predictions to log file %s", logs_features_file)
        self._save_to_file(logs_features_file,
                           (metadata_names, ["labels"], ["Pred"], feature_names),
                           (metadata, labels, np.array(predicted_on_train), features))

        # post processing
        model_scorer = ModelScorer(labels=distinct_labels, positive_label=positive_label,
                                   logs_dir=tempfile.gettempdir())
        col_self_rel_index = 4
        post_processor = PostProcessingSelfRelation(col_self_rel_index, value_to_match=True, value_to_set=False)
        k_fold = KFold(n_splits=kfold_splits, shuffle=True, random_state=random_state)
        for train, test in k_fold.split(features):
            trained_model.fit(features[train], labels[train])
            pred_train = trained_model.predict(features[train])
            pred_test = trained_model.predict(features[test])
            post_processed_test = post_processor.process(None, pred_test, metadata[test])
            # Save test set
            logs_features_file = os.path.join(self.logs_dir,
                                              tempfile.mkstemp(prefix="data_formatted_features", suffix=".csv")[1])
            self.logger.debug("Writing kth train features labels and predictions to log file %s", logs_features_file)
            self._save_to_file(logs_features_file,
                               (metadata_names, ["labels"], ["Pred"], feature_names),
                               (metadata[train], labels[train], np.array(pred_train),
                                features[train]))

            logs_features_file = os.path.join(self.logs_dir,
                                              tempfile.mkstemp(prefix="data_formatted_features", suffix=".csv")[1])
            self.logger.debug("Writing train features labels and predictions to log file %s", logs_features_file)
            self._save_to_file(logs_features_file,
                               (metadata_names, ["labels"], ["Pred"], feature_names),
                               (metadata[test], labels[test], np.array(post_processed_test),

                                features[test]))

            f, p, r = model_scorer.get_scores(labels[test], post_processed_test)
            self.logger.info("Kth hold set f-score, after post processing %s", f)

        return pickle_file_name

    def validate(self, data_rows, training_settings_pickle):

        # training settings
        training_settings = pickle.load(open(training_settings_pickle, "rb"))
        trained_model = training_settings["model"]
        feature_extractor = training_settings["feature_extractor"]

        self.logger.info("Data rows %s", np.array(data_rows).shape)
        result = feature_extractor.extract(data_rows)

        metadata_names = result[self.feature_extractor.key_metadata_names]
        feature_names = result[self.feature_extractor.key_feature_names]
        features = result[self.feature_extractor.key_feature]
        metadata = result[self.feature_extractor.key_metadata]

        self.logger.info("features %s", np.array(features).shape)

        predicted = trained_model.predict(features)

        labels = np.array(self.get_labels(data_rows))
        distinct_labels = np.unique(labels)
        positive_label = True
        # Log some stats about the class
        unique, counts = np.unique(labels, return_counts=True)
        self.logger.info("Unique classes vs counts in validation set\n %s", np.asarray((unique, counts)).T)

        model_scorer = ModelScorer(labels=distinct_labels, positive_label=positive_label,
                                   logs_dir=tempfile.gettempdir())
        f, p, r = model_scorer.get_scores(labels, predicted)
        self.logger.info("Validation set score f = %s, p= %s, r = %s", f, p, r)

        post_processor = PostProcessingSelfRelation(4, value_to_match=True, value_to_set=False)
        post_processed_pred = post_processor.process(None, predicted, metadata)

        f, p, r = model_scorer.get_scores(labels, post_processed_pred)
        self.logger.info("Validation post_processed_pred set score f = %s, p= %s, r = %s", f, p, r)

        # writeback to biocformat
        data_rows_result = self.feature_extractor.convert_bioc_ready(metadata, metadata_names, predicted)
        return data_rows_result

    def get_labels(self, data_rows):
        labels = []
        for r in data_rows:
            labels.append(self.validate_relation(r[I_RELATIONS], r[I_GENE1], r[I_GENE2]))
        return labels
