import re

"""
Extracts words between proteins in a passage. Preserves sentences.
"""


class PPIFragementExtractor:

    def __init__(self):
        pass

    def extract(self, sentence_vector, protein1, protein2):
        # Match all words between 2 proteins
        result = []
        for s in sentence_vector:
            self._fill_matching_word_frag(s, protein1, protein2, result)
            self._fill_matching_word_frag(s, protein2, protein1, result)
        return result

    def _fill_matching_word_frag(self, s, protein1, protein2, result):
        word_frag = self._match(s, protein1, protein2)
        if word_frag is not None:
            result.append(word_frag)

    def _match(self, sentence, protein1, protein2):
        regex_str = r"{}\s+[^.]*\s+{}";
        matching_words = re.search(regex_str.format(protein1, protein2), sentence)

        if matching_words:
            return matching_words.group(0);
        return None
