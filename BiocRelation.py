from bioc import BioCDocument, BioCRelation


class BiocRelation(object):
    def is_valid(self, doc, gene1, gene2):
        for rel in doc.relations:
            if set([rel.infons["Gene1"], rel.infons["Gene2"]]) == set([gene1, gene2]):
                return True
        return False
