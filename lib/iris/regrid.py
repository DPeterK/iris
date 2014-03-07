# (C) British Crown Copyright 2010 - 2014, Met Office
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
Regridding and interpolation functionality.

"""

import iris
import iris.analysis.interpolate as iai
import iris.experimental.regrid as ier


class Interpolator(object):

    def __init__(self):
        pass


class Regridder(object):

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def regrid(self, src, grid):
        return iai.regrid(src, grid, mode=self.mode)


class LINEAR(object):

    def __init__(self, **kwargs):
        self._extrap = kwargs.pop('extrapolation_mode', 'linear')

        self.mode = 'linear'

    def interpolate(self, src, points):
        return iai.linear(src, points, extrapolation_mode=self._extrap)


class BILINEAR(Regridder):

    def __init__(self, **kwargs):
        self.mdtol = kwargs.pop('mdtol', None)
        self.weights = kwargs.pop('weights', None)

        self.mode = 'bilinear'

#     def regrid(self, src, grid):
#         return iris.analysis.regrid(src, grid, mode=self.mode)


class NEAREST(Regridder):

    def __init__(self, **kwargs):
        self.mdtol = kwargs.pop('mdtol', None)
        self.weights = kwargs.pop('weights', None)
        self._nd = kwargs.pop('nd', False)
        self._extract = kwargs.pop('extract', None)
        self.kw = kwargs

        self.mode = 'nearest'

#     def regrid(self, src, grid):
#         return iris.analysis.regrid(src, grid, mode=self.mode)
    
    def interpolate(self, src, points):
        if self._nd:
            result = iai._nearest_neighbour_indices_ndcoords(src,
                                                             points,
                                                             **self.kw)
        else:
            result = iai.nearest_neighbour_indices(src, points)
        if self._extract == 'cube':
            result = src[result]
        elif self._extract == 'data':
            result = iai.nearest_neighbour_data_value(src,
                                                      points,
                                                      indices=result)
        return result


class RECTILINEAR(object):

    def __init__(self, **kwargs):
        self.mode = kwargs.pop('mode', 'bilinear')
        self.weights = kwargs.pop('weights', None)
        self.kw = kwargs

    def regrid(self, src_cube, grid_cube):
        if self.mode == 'bilinear':
            result = ier.regrid_bilinear_rectilinear_src_and_grid(src_cube,
                                                                  grid_cube)
        elif self.mode == 'area_weighted':
            result = ier.regrid_area_weighted_rectilinear_src_and_grid(
                src_cube, grid_cube)
        elif self.mode == 'curvilinear':
            result = ier.regrid_weighted_curvilinear_to_rectilinear(
                src_cube, self.weights, grid_cube)
        else:
            msg = '{} is not a valid mode for rectilinear regridding.'
            raise ValueError(msg.format(self.mode))
        return result


def regrid(src_cube, grid_cube, regrid_method, **kwargs):
    regrid_func = regrid_method(**kwargs)
    return regrid_func.regrid(src_cube, grid_cube)


def interpolate(src_cube, sample_points, interpolate_method, **kwargs):
    interpolate_func = interpolate_method(**kwargs)
    return interpolate_func.interpolate(src_cube, sample_points)
