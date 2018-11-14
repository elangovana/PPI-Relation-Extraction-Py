from unittest import TestCase

import numpy as np
from ddt import ddt, data, unpack

from source.PostProcessingSelfRelation import PostProcessingSelfRelation


@ddt
class TestPostProcessingSelfRelation(TestCase):

    @data(([[0, 1, 2]], [0], 0, 1, [1])
        , ([[0, 1, 2], [1, 0, 0]], [0, 0],0, 1, [1, 0])

          )
    @unpack
    def test_process(self, metadata_x, y, value_to_match, value_to_set, expected_y):
        # Arrange
        sut = PostProcessingSelfRelation(col_index_self_rel=0, value_to_match=value_to_match, value_to_set=value_to_set)

        # Act
        actual = sut.process(None, y, metadata_x)

        # Assert
        self.assertEqual(np.array(expected_y).flatten().tolist(), np.array(actual).flatten().tolist())
