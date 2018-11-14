import re

"""
Extracts words between proteins in a passage. Preserves sentences.
"""


class PPIFragementExtractor:

    def __init__(self):
        pass

    def extract(self, sentence_vector, protein1, protein2, remove_words=[]):
        # Match all words between 2 proteins
        result = []
        for s in sentence_vector:
            #get all words between the 2 proteins
            self._fill_inbetween_word_frag(s, protein1, protein2, result, remove_words)
            self._fill_inbetween_word_frag(s, protein2, protein1, result, remove_words)

        return result

    def _fill_inbetween_word_frag(self, s, protein1, protein2, result, remove_words):
        """
        Fills the result array with all matches between the 2 proteins
        :param s: the sentence
        :param protein1:
        :param protein2:
        :param result:
        """
        word_frag = self._getWordFrag(s, protein1, protein2, remove_words)
        if word_frag is not None:
            result.append(word_frag)

    def _getWordFrag(self, sentence, protein1, protein2, remove_words):
        regex_str = r"{}\s+([^.]*)\s+{}";
        matching_words = re.search(regex_str.format(protein1, protein2), sentence)

        if matching_words:
            matching_frag = matching_words.group(1)
            for w in remove_words:
                matching_frag = matching_frag.replace(w,"")
            return  matching_frag
        return None
