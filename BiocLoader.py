import bioc

from BiocSentences import BiocSentences


class BiocLoader:

    def __init__(self):
        self.biocDocProcessors=[BiocSentences()]

    def parse(self, filename):
        with open(filename, 'r') as fp:
            collection = bioc.load(fp)
            for doc in collection.documents:
                self._convert_doc_to_flat(doc)

    def _convert_doc_to_flat(self, doc):
        return [doc.id, ]
