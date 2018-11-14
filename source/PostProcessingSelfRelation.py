class PostProcessingSelfRelation:

    def __init__(self, col_index_self_rel, value_to_match, value_to_set):
        """

        :param value_to_match: The value to match, the true condition for self relation
        :param value_to_set:  The value to set, when the condition is true
        :param col_index_self_rel: Index of the sel relationship in the metadata
        """
        self.value_to_match = value_to_match
        self.value_to_set = value_to_set
        self.col_index_self_rel = col_index_self_rel

    def process(self, matrix_x, y, metadata_v=None):
        for i in range(0, len(metadata_v)):
            if metadata_v[i][self.col_index_self_rel] == self.value_to_match:
                y[i] = self.value_to_set
        return y
