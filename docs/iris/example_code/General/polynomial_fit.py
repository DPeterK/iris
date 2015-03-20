"""
Fitting a polynomial
====================

This example demonstrates adding a polynomial fit to a 1D plot of data from
an Iris cube.

"""

import matplotlib.pyplot as plt
import numpy as np

import iris
import iris.plot as iplt
import iris.quickplot as qplt


def main():
    fname = iris.sample_data_path('A1B_north_america.nc')
    cube = iris.load_cube(fname)

    # Extract a single time cross-section at a latitude and longitude point.
    location = next(cube.slices(['time']))

    # Calculate a polynomial fit to the data at this cross-section.
    x_points = location.coord('time').points
    y_points = location.data
    degree = 3

    p = np.polyfit(x_points, y_points, degree)
    f = np.poly1d(p)
    y_fitted = f(x_points)

    # Add the polynomial fit values to the cross-section to take
    #  full advantage of Iris plotting functionality.
    fit = iris.coords.AuxCoord(y_fitted, long_name='polynomial_fit_of_data',
                               units=location.units)
    location.add_aux_coord(fit, 0)

    qplt.plot(location.coord('time'), location, label='data')
    qplt.plot(location.coord('time'),
              location.coord('polynomial_fit_of_data'),
              'g-', label='polynomial fit')
    plt.legend(loc='best')
    plt.title('Trend of US air temperature over time')

    iplt.show()


if __name__ == '__main__':
    main()
