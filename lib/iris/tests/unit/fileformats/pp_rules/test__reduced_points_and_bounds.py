# (C) British Crown Copyright 2014 - 2015, Met Office
#
# This file is part of Iris.
#
# Iris is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Iris is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Iris.  If not, see <http://www.gnu.org/licenses/>.
"""
Unit tests for
:func:`iris.fileformats.pp_rules._reduce_points_and_bounds`.

"""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

# Import iris.tests first so that some things can be initialised before
# importing anything else.
import iris.tests as tests

import numpy as np

from iris.fileformats.pp_load_rules import _reduce_points_and_bounds


class Test(tests.IrisTest):
    def test_scalar(self):
        array = np.array(1)
        dims, result, bounds = _reduce_points_and_bounds(array)
        self.assertArrayEqual(result, array)
        self.assertEqual(dims, None)
        self.assertIsNone(bounds)

    def test_1d_nochange(self):
        array = np.array([1, 2, 3])
        dims, result, _ = _reduce_points_and_bounds(array)
        self.assertArrayEqual(result, array)
        self.assertEqual(dims, (0,))

    def test_1d_collapse(self):
        array = np.array([1, 1, 1])
        dims, result, _ = _reduce_points_and_bounds(array)
        self.assertArrayEqual(result, np.array(1))
        self.assertEqual(dims, None)

    def test_2d_nochange(self):
        array = np.array([[1, 2, 3], [4, 5, 6]])
        dims, result, _ = _reduce_points_and_bounds(array)
        self.assertArrayEqual(result, array)
        self.assertEqual(dims, (0, 1))

    def test_2d_collapse_dim0(self):
        array = np.array([[1, 2, 3], [1, 2, 3]])
        dims, result, _ = _reduce_points_and_bounds(array)
        self.assertArrayEqual(result, np.array([1, 2, 3]))
        self.assertEqual(dims, (1,))

    def test_2d_collapse_dim1(self):
        array = np.array([[1, 1, 1], [2, 2, 2]])
        dims, result, _ = _reduce_points_and_bounds(array)
        self.assertArrayEqual(result, np.array([1, 2]))
        self.assertEqual(dims, (0,))

    def test_2d_collapse_both(self):
        array = np.array([[3, 3, 3], [3, 3, 3]])
        dims, result, _ = _reduce_points_and_bounds(array)
        self.assertArrayEqual(result, np.array(3))
        self.assertEqual(dims, None)

    def test_3d(self):
        array = np.array([[[3, 3, 3], [4, 4, 4]], [[3, 3, 3], [4, 4, 4]]])
        dims, result, _ = _reduce_points_and_bounds(array)
        self.assertArrayEqual(result, np.array([3, 4]))
        self.assertEqual(dims, (1,))

    def test_bounds_collapse(self):
        points = np.array([1, 1, 1])
        bounds = np.array([[0, 2], [0, 2], [0, 2]])
        result_dims, result_pts, result_bds = \
            _reduce_points_and_bounds(points, (bounds[..., 0], bounds[..., 1]))
        self.assertArrayEqual(result_pts, np.array(1))
        self.assertArrayEqual(result_bds, np.array([0, 2]))
        self.assertEqual(result_dims, None)

    def test_bounds_no_collapse(self):
        points = np.array([1, 2, 3])
        bounds = np.array([[0, 2], [1, 3], [2, 4]])
        result_dims, result_pts, result_bds = \
            _reduce_points_and_bounds(points, (bounds[..., 0], bounds[..., 1]))
        self.assertArrayEqual(result_pts, points)
        self.assertArrayEqual(result_bds, bounds)
        self.assertEqual(result_dims, (0,))


if __name__ == "__main__":
    tests.main()
