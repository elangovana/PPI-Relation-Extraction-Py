"""
This is the main pipeline class for relation extraction.
"""
import collections
import logging
import tempfile

import numpy as np
import os
import cPickle as pickle

from sklearn.model_selection import KFold

from BiocRelation import BiocRelation
from ModelLogisticsRegresssion import ModelLogisticsRegression
from ModelScorer import ModelScorer
from NGramFeatureExtractor import NGramFeatureExtractor
from PPIFragmentExtractor import PPIFragementExtractor
from PostProcessingSelfRelation import PostProcessingSelfRelation

I_RELATIONS = 1
I_GENE1 = 2
I_GENE2 = 3
I_SENTENCES = 4
I_GENESINDOC = 5
I_BIOCDOC = 6
I_NORM_FREQUNCE = 7
I_FRAGMENTS = 8
I_SELFRELATION = 9


class Pipeline:

    def __init__(self, model=None, logs_dir=tempfile.mkdtemp()):
        self.logs_dir = logs_dir
        self.logger = logging.getLogger(__name__)
        self.validate_relation = BiocRelation().is_valid
        self.preprocessor_ngram_feature_extractor = NGramFeatureExtractor().extract
        self.preprocessor_fragment_extractor = PPIFragementExtractor().extract

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
        # Extract fragments
        for r in data_rows:
            fragments = self.preprocessor_fragment_extractor(r[I_SENTENCES], r[I_GENE1], r[I_GENE2], r[I_GENESINDOC])
            count_of_valid_fragments = sum(r[I_GENE1] in f and r[I_GENE2] in f for f in fragments)
            normalised_frequency = count_of_valid_fragments * 100 / (len(r[I_SENTENCES]))
            combined_fragments = "   \t ".join(fragments)
            r.append(normalised_frequency)
            r.append(combined_fragments)
            r.append(int(r[I_GENE1] == r[I_GENE2]))

        # Test case by titling the number in favour of thumb print 0 to false, by removing some records
        #  remove_rec=[('21569203','28379874','2335')
        #  ,('18570893','801','4651')
        #  ,('15350535','5058','58480')
        #  ,('26342861','7474','11197')
        #  ,('26342861','11197','7476')
        #  ,('20547845','3146','7099')
        #  ,('20890284','10870','22914')
        #  ,('20181956','26986','57690')
        #  ,('18647389','9185','274')
        # ]
        #  data_rows = [r for r in data_rows if (r[I_DOCID], r[I_GENE1], r[I_GENE2]) not in remove_rec]

        # Extract ngram features
        v_ngram_features, n_gram_names = self.preprocessor_ngram_feature_extractor(np.array(data_rows)[:, I_FRAGMENTS])
        features = v_ngram_features
        feature_names = n_gram_names

        # Append features to ngrams
        # Self Relation
        new_feature = np.array(data_rows)[:, I_SELFRELATION]
        features = np.concatenate((features, new_feature.reshape(len(new_feature), 1)), axis=1)
        feature_names.append("SelfRelation")

        # Feature count
        feature_count = np.array([[np.sum(r)] for r in features])
        # new_feature = feature_count
        # features = np.concatenate((features, new_feature.reshape(len(new_feature), 1)), axis=1)
        # feature_names.append("feature_count")


#Normalised gene pair frequncy
        # new_feature = np.array(data_rows)[:, I_NORM_FREQUNCE]
        # features = np.concatenate((features, new_feature.reshape(len(new_feature), 1)), axis=1)
        # feature_names.append("normalised_frequency")

        # Append features to metadata (not used by model)
        # Self Relation
        metadata = np.array(data_rows)[:, 0:I_SENTENCES]
        metadata_feature_names = ["uid", "docid", "gene1", "gene2"]
        new_feature = np.array(data_rows)[:, I_SELFRELATION]
        metadata = np.concatenate((metadata, new_feature.reshape(len(new_feature), 1)), axis=1)
        metadata_feature_names.append("SelfRelation")
        #Feature count
        new_feature = feature_count
        metadata = np.concatenate((metadata, new_feature.reshape(len(new_feature), 1)), axis=1)
        metadata_feature_names.append("feature count")

        # Train model
        labels = np.array(self.get_labels(data_rows))
        distinct_labels = np.unique(labels)
        positive_label = True
        self.logger.info("Training model...")
        self.logger.info("Total number of features used %i. Feature names:\n%s", len(feature_names),
                         "\n".join(feature_names))
        random_state = 42
        kfold_splits = 3
        trained_model, holdout_f_score = self.model.train(features, labels, metadata_v=metadata,
                                                          kfold_random_state=random_state, kfold_n_splits=kfold_splits)
        predicted_on_train = trained_model.predict(features)

        # log formatted features to file
        logs_features_file = os.path.join(self.logs_dir,
                                          tempfile.mkstemp(prefix="data_formatted_features", suffix=".csv")[1])
        feature_thumbprint = np.array([["".join(np.array(r).astype(str))] for r in features])
        self.logger.info("Writing train features labels and predictions to log file %s", logs_features_file)
        self._save_to_file(logs_features_file,
                           (metadata_feature_names, ["labels"], ["Pred"], ["thumbprint"], feature_names),
                           (metadata, labels, np.array(predicted_on_train), feature_thumbprint, features))

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
            self.logger.info("Writing kth train features labels and predictions to log file %s", logs_features_file)
            self._save_to_file(logs_features_file,
                               (metadata_feature_names, ["labels"], ["Pred"], ["thumbprint"], feature_names),
                               (metadata[train], labels[train], np.array(pred_train), feature_thumbprint[train],
                                features[train]))

            logs_features_file = os.path.join(self.logs_dir,
                                              tempfile.mkstemp(prefix="data_formatted_features", suffix=".csv")[1])
            self.logger.info("Writing train features labels and predictions to log file %s", logs_features_file)
            self._save_to_file(logs_features_file,
                               (metadata_feature_names, ["labels"], ["Pred"], ["thumbprint"], feature_names),
                               (metadata[test], labels[test], np.array(post_processed_test), feature_thumbprint[test],
                                features[test]))

            f, p, r = model_scorer.get_scores(labels[test], post_processed_test)
            self.logger.info("Kth hold set f-score, after post processing %s", f)

        # persist trained model
        pickle_file_name = os.path.join(output_dir, tempfile.mkstemp(prefix="trained_model")[1])
        self.logger.info("Saving model to %s", pickle_file_name)
        with open(pickle_file_name, 'wb') as fd:
            pickle.dump(trained_model, fd)

    def get_labels(self, data_rows):
        labels = []
        for r in data_rows:
            labels.append(self.validate_relation(r[I_BIOCDOC], r[I_GENE1], r[I_GENE2]))
        return labels
