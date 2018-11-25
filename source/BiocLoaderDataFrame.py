import logging
import tempfile

import pandas as pd
from bioc import BioCCollection

from BiocLoader import BiocLoader, I_DOC_ID, I_GENE1, I_GENE2, I_SENTENCES, I_ID, I_RELATIONS
from BiocRelation import BiocRelation
import bioc

class BiocLoaderDataFrame:

    def __init__(self, logs_dir=None):
        self.bioc_loader = BiocLoader()
        self.validate_relation = BiocRelation().is_valid
        self.logger = logging.getLogger(__name__)

    def parse(self, filename, output_dir=tempfile.mkdtemp()):
        data_rows = self.bioc_loader.parse(filename)

        formatted_data_rows = []
        for r in data_rows:
            formatted_data_rows.append([
                str(r[I_ID]),
                str(r[I_DOC_ID]),
                str(r[I_GENE1]),
                str(r[I_GENE2]),
                ". ".join(r[I_SENTENCES]),
                self.validate_relation(r[I_RELATIONS], r[I_GENE1], r[I_GENE2])])

        dataframe = pd.DataFrame(formatted_data_rows,
                                 columns=["id", "docid", "participant1", "participant2", "abstract", "isValid"])
        return dataframe

    def dump(self, dataframe, handle):
        # Read file and do preliminary pre processing to form rows of records
        dic = {}

        for i, d in dataframe.iterrows():
            if not d["isValid"]: continue

            i_relation = I_GENE2 + 1
            # Only bother with true relations
            if not d[i_relation]:
                continue

            # construct dictionary
            docid = d["docid"]
            if docid not in dic:
                dic[docid] = {"relations": []}

            dic[docid]["relations"].append((d["participant1"], d["participant2"]))

        biocrelation_wrapper = BiocRelation()

        collection = BioCCollection()
        for docid in dic.keys():
            collection.add_document(biocrelation_wrapper.get_bioc_relations(docid, dic[docid]["relations"]))

        self.logger.info("Writing input to handle")
        bioc.dump(collection, handle)
