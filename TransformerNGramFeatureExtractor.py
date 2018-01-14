import logging

import numpy as np

from BiocLoader import I_SENTENCES, I_GENE1, I_GENE2, I_GENESINDOC, I_ID, I_DOC_ID
from NGramExtractor import NGramExtractor
from PPIFragmentExtractor import PPIFragementExtractor
from Transformer import Transformer


class TransformerNGramFeatureExtractor(Transformer):

    def __init__(self, n_grams=None, ngram_extractor=None):
        self.key_n_grams = "n_grams"
        self.key_self_relation = "Self--Relation"
        self.key_frequncy = "frequnce"
        self.meta_field_name_id = "uid"
        self.meta_field_name_doc_id = "docid"
        self.meta_field_name_gene1 = "gene1"
        self.meta_field_name_gene2 = "gene2"
        self.preprocessor_ngram_feature_extractor = ngram_extractor or NGramExtractor(
            vocabulary=n_grams).extract
        self.preprocessor_fragment_extractor = PPIFragementExtractor().extract
        self.logger = logging.getLogger(__name__)
        Transformer.__init__(self)

    def extract(self, data_rows):
        tmp_stage1_transformed_data_rows = []
        Feature_NORM_FREQ = "normalised_frequncey"
        Feature_Fragments = "Feature fragments"
        Feature_IsSelfRelation = "isselfrelation"
        indics = {Feature_NORM_FREQ: 0, Feature_Fragments: 1, Feature_IsSelfRelation: 2}

        metadata = np.array(data_rows)[:, [I_ID, I_DOC_ID, I_GENE1, I_GENE2]]
        metadata_feature_names = [self.meta_field_name_id, self.meta_field_name_doc_id, self.meta_field_name_gene1,
                                  self.meta_field_name_gene2]

        for r in data_rows:
            fragments = self.preprocessor_fragment_extractor(r[I_SENTENCES], r[I_GENE1], r[I_GENE2], r[I_GENESINDOC])
            count_of_valid_fragments = len(fragments)
            normalised_frequency = (count_of_valid_fragments * 100) / (len(r[I_SENTENCES]))
            combined_fragments = "   \t ".join(fragments)

            tmp_stage1_transformed_data_rows.append(
                [normalised_frequency, combined_fragments, int(r[I_GENE1] == r[I_GENE2])])

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
        v_ngram_features, n_gram_names = self.preprocessor_ngram_feature_extractor(
            np.array(tmp_stage1_transformed_data_rows)[:, indics[Feature_Fragments]])

        features = v_ngram_features
        feature_names = []
        feature_names.extend(n_gram_names)

        # Append features to ngrams
        # Self Relation
        new_feature = (np.array(tmp_stage1_transformed_data_rows)[:, indics[Feature_IsSelfRelation]].astype(int))
        features = np.concatenate((features, new_feature.reshape(len(new_feature), 1)), axis=1)
        feature_names.append(self.key_self_relation)

        # Feature count
        feature_count = np.array([[np.sum(r)] for r in features])
        # new_feature = feature_count
        # features = np.concatenate((features, new_feature.reshape(len(new_feature), 1)), axis=1)
        # feature_names.append("feature_count")

        # Normalised gene pair frequncy

        new_feature = np.array(tmp_stage1_transformed_data_rows)[:, indics[Feature_NORM_FREQ]].astype(int)
        features = np.concatenate((features, new_feature.reshape(len(new_feature), 1)), axis=1)
        feature_names.append("normalised_frequency")

        # Append features to metadata (not used by model)
        # Self Relation
        new_feature = np.array(tmp_stage1_transformed_data_rows)[:, indics[Feature_IsSelfRelation]]
        metadata = np.concatenate((metadata, new_feature.reshape(len(new_feature), 1)), axis=1)
        metadata_feature_names.append("SelfRelation")

        new_metadata_feature = np.array([["".join(np.array(r).astype(str))] for r in v_ngram_features])
        metadata = np.concatenate((metadata, new_metadata_feature.reshape(len(new_metadata_feature), 1)), axis=1)
        metadata_feature_names.append("tumbpint")


        # Feature count
        new_feature = feature_count
        metadata = np.concatenate((metadata, new_feature.reshape(len(new_feature), 1)), axis=1)
        metadata_feature_names.append("feature count")

        self.logger.info("Total number of features used %s. Feature names:\n %s",
                         len(feature_names),
                         "\n".join(feature_names))

        return ({self.key_metadata_names: metadata_feature_names, self.key_metadata: metadata,
                 self.key_feature_names: feature_names, self.key_feature: features, self.key_n_grams: n_gram_names,
                 self.key_self_relation: self.key_self_relation})

    def convert_bioc_ready(self, metadata, metadata_names, y):
        result = []
        i_id = metadata_names.index(self.meta_field_name_id)
        i_docId = metadata_names.index(self.meta_field_name_doc_id)
        i_gene1 = metadata_names.index(self.meta_field_name_gene1)
        i_gene2 = metadata_names.index(self.meta_field_name_gene2)

        i = 0
        for m in metadata:
            result.append([m[i_id], m[i_docId], m[i_gene1], m[i_gene2], y[i]])
            i = i + 1

        return result
