import logging


class BiocAnnotationSentences:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def convert_to_vec(self, biocDoc):
        result =[]
        for passage in biocDoc.passages:
            for sentence in passage.sentences:
                self.logger.debug("Adding bioc sentence %s", sentence)
                result.append(sentence)
        return result


