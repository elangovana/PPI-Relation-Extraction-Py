import bioc


class BiocLoader:

    def __init__(self):
        self.biocDocProcessors=[]

    def parse(self, filename):
        with open(filename, 'r') as fp:
            collection = bioc.load(fp)
            for doc in collection.documents:
                self._convert_doc_to_flat(doc)

    def _convert_doc_to_flat(self, doc):
        pass
