import bioc
from bioc import BioCCollection, BioCDocument

from BiocAnnotationGenes import BiocAnnotationGenes
from BiocRelation import BiocRelation
from BiocSentences import BiocSentences
from PreprocessorNormaliseGenes import PreprocessorNormaliseGenes

import tempfile
import logging
import itertools

I_ID = 0
I_DOC_ID = 1
I_GENE1 = 2
I_GENE2 = 3
I_SENTENCES = 4
I_GENESINDOC = 5
I_RELATIONS = 6


class BiocLoader:

    def __init__(self, logs_dir=tempfile.mkdtemp()):
        self.logs_dir = logs_dir
        self.logger = logging.getLogger(__name__)

        self.sentence_extractor = BiocSentences().convert_to_vec
        self.retrieve_gene_names_dict = BiocAnnotationGenes().get_gene_names_to_normalised_dict
        self.retrieve_relations = BiocRelation().get_relations
        self.preprocessor_replace_with_norm_genes = PreprocessorNormaliseGenes().normalise_gene_names_bulk

    def parse(self, filename, output_dir=tempfile.mkdtemp()):
        # Read file and do preliminary pre processing to form rows of records
        data_rows = []
        with open(filename, 'r') as fp:
            collection = bioc.load(fp)
            for doc in collection.documents:
                rows_x = self.convert_bioc_document_to_rows(doc)
                data_rows.extend(rows_x)

        # subset
        # data_rows =  data_rows[1:100]
        return data_rows

    def convert_bioc_document_to_rows(self, doc):
        result_x = []

        gene_to_norm_gene_dict = self.retrieve_gene_names_dict(doc)
        genes = gene_to_norm_gene_dict.values()

        gene_pairs = list(itertools.combinations_with_replacement(list(set(genes)), 2))

        # # Add gene pairs not picked by annotation, but are present in relations
        # relations = self.retrieve_relations(doc)
        # for r in relations:
        #     r=list(r)
        #     gene1 = r[0]
        #     if len(r) ==2:
        #         gene2 = r[1]
        #     else:
        #         gene2 = gene1
        #
        #     gene_pairs.append([gene1, gene2])

        # normalise gene names in sentences
        sentences = self.sentence_extractor(doc)
        normalised_sentences = self.preprocessor_replace_with_norm_genes(sentences, gene_to_norm_gene_dict)

        # extract fragments
        for gene_pair in gene_pairs:
            # construct unique id
            gene1 = gene_pair[0]
            gene2 = gene_pair[1]
            uid = "{}#{}#{}".format(doc.id, gene1, gene2)
            result_x.append([uid, doc.id, gene1, gene2, normalised_sentences, genes, self.retrieve_relations(doc)])

        return result_x

    def dump(self, data_rows, filename=tempfile.mkstemp(prefix="PredictedFile", suffix=".xml")[1]):
        # Read file and do preliminary pre processing to form rows of records
        dic = {}
        for d in data_rows:
            i_relation = I_GENE2 + 1
            # Only bother with true relations
            if not d[i_relation]:
                continue

            # construct dictionary
            docid = d[I_DOC_ID]
            if not dic.has_key(docid):
                dic[docid] = {"relations": []}

            dic[docid]["relations"].append((d[I_GENE1], d[I_GENE2]))

        biocrelation_wrapper = BiocRelation()
        with open(filename, 'w') as fp:
            collection = BioCCollection()
            for docid in dic.keys():
                collection.add_document(biocrelation_wrapper.get_bioc_relations(docid, dic[docid]["relations"]))

            self.logger.info("Writing input to %s", filename)
            bioc.dump(collection, fp)
