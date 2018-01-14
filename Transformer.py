import logging


class Transformer:
    def __init__(self):
        self.key_metadata = "metadata"
        self.key_metadata_names ="metadata_names"
        self.key_feature_names ="feature_names"
        self.key_feature ="feature"
        self.logger = logging.getLogger(__name__)


    def extract(self, data_rows):
        pass

