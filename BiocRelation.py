from bioc import BioCDocument, BioCRelation


class BiocRelation(object):
    def is_valid(self, doc, gene1, gene2):
        if isinstance(doc, BioCDocument):
            return self._is_valid_given_biocdoc(doc, gene1, gene2)
        else:
            return self._is_valid_given_relations(doc, gene1, gene2)

    def _is_valid_given_biocdoc(self, doc, gene1, gene2):
        list_of_relations = self.get_relations(doc)
        return self._is_valid_given_relations(list_of_relations, gene1, gene2)

    def _is_valid_given_relations(self, list_of_relations, gene1, gene2):
        for rel in list_of_relations:
            if rel == {gene1, gene2}:
                return True
        return False

    def get_relations(self, doc):

        # <relation id="5618#7534">
        #     <infon key="Gene1">5618</infon>
        #     <infon key="Gene2">7534</infon>
        #     <infon key="relation">PPIm</infon>
        # </relation>

        result = []
        for rel in doc.relations:
            if rel.infons["relation"] == "PPIm":
                result.append({rel.infons["Gene1"], rel.infons["Gene2"]})
        return result

    def get_bioc_relations(self, docid, relations):

        # <relation id="5618#7534">
        #     <infon key="Gene1">5618</infon>
        #     <infon key="Gene2">7534</infon>
        #     <infon key="relation">PPIm</infon>
        # </relation>

        biocDoc=BioCDocument()
        biocDoc.id = docid
        biocDoc.relations=[]

        for rel in relations:
            bioc_rel = BioCRelation()
            rel_list = list(rel)
            infon = {}
            infon["relation"] = "PPIm"
            infon["Gene1"] = rel_list[0]

            infon["Gene2"] = rel_list[0]
            if len(rel_list) == 2:
                infon["Gene2"] = rel_list[1]

            bioc_rel.id="{}#{}".format(infon["Gene1"], infon["Gene2"])
            bioc_rel.infons=infon
            biocDoc.relations.append(bioc_rel)

        return biocDoc
