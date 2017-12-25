import bioc

from BiocAnnotationGenes import BiocAnnotationGenes
from BiocSentences import BiocSentences


class BiocLoader:

    def __init__(self):
        self.biocDocProcessors=[BiocSentences().convert_to_vec, BiocAnnotationGenes().get_gene_names]

    def parse(self, filename):
        with open(filename, 'r') as fp:
            collection = bioc.load(fp)
            for doc in collection.documents:
                self._convert_doc_to_flat(doc)

    def _convert_doc_to_flat(self, doc):
        result = [doc.id]
        for processor in self.biocDocProcessors:
            result.append(processor(doc))
        return result

