



You can also convert realised data back into a lazy array::

    >>> cube.has_lazy_data()
    False
    >>> cube.data = cube.lazy_data()
    >>> cube.has_lazy_data()
    True

Note: the term "back into" is misleading; see https://github.com/SciTools/iris/pull/2583#discussion_r118980917
Note: realised data may not be the best terminology; see https://github.com/SciTools/iris/pull/2583#discussion_r118981051


Changing a cube's data
----------------------

There are several methods of modifying a cube's data array, each one subtly
different from the others.

Maths
^^^^^

You can use :ref:`cube maths <cube_maths>` to make in-place modifications to
each point in a cube's existing data array.  Provided you do not directly
reference the cube's data, the array will remain lazy::

    >>> cube = iris.load_cube(iris.sample_data_path('air_temp.pp'))
    >>> cube.has_lazy_data()
    True
    >>> cube *= 10
    >>> cube.has_lazy_data()
    True

Note: "each point" is bad terminology; see https://github.com/SciTools/iris/pull/2583#discussion_r118981932


Copy
^^^^

You can copy a cube and assign a completely new data array to the copy. All the
original cube's metadata will be the same as the new cube's metadata.  However,
the new cube's data array will not be lazy if you replace it with a real array
(but you can supply a lazy array and end up with lazy data; 
see https://github.com/SciTools/iris/pull/2583#discussion_r118982111 )::

    >>> import numpy as np
    >>> data = np.zeros((73, 96))
    >>> new_cube = cube.copy(data=data)
    >>> new_cube.has_lazy_data()
    False

Replace
^^^^^^^

This should probably have a good heap of docs with it: what does it do, why do
we need it, what are the unexpected behaviours, when should I (/should I not)
use it?

This does essentially the same thing as `cube.copy()`, except that it provides
a safe method of doing so for the specific edge case of a lazy masked integer
array::

    >>> values = np.zeros((73, 96), dtype=int)
    >>> data =np.ma.masked_values(values, 0)
    >>> print(data)
    [[-- -- -- ..., -- -- --]
     [-- -- -- ..., -- -- --]
     [-- -- -- ..., -- -- --]
     ...,
     [-- -- -- ..., -- -- --]
     [-- -- -- ..., -- -- --]
     [-- -- -- ..., -- -- --]]
    >>> new_cube = cube.replace(data=data)
    >>> new_cube.has_lazy_data()
    False
    >>> new_cube.data = new_cube.lazy_data()
    >>> new_cube.has_lazy_data()
    True

This method is necessary as Dask is currently unable to handle masked arrays.


Dask processing options
-----------------------

Dask applies some default values to certain aspects of the parallel processing
that it offers with Iris. It is possible to change these values and override
the defaults by using 'dask.set_options(option)' in your script.

You can use this as a global variable if you wish to use your chosen option for
the full length of the script, or you can use it with a context manager to
control the span of the option.

Here are some examples of the options that you may wish to change.

You can set the number of threads on which to work like this::

    >>> import dask
    >>> from multiprocessing.pool import ThreadPool
    >>> with dask.set_options(pool=ThreadPool(4)):
    ...     x.compute()

Multiple threads work well with heavy computation.


You can change the default option between threaded scheduler and
multiprocessing scheduler, for example::

    >>> with dask.set_options(get=dask.multiprocessing.get):
    ...     x.sum().compute()

Multiprocessing works well with strings, lists or custom Dask objects.


You can choose to run all processes in serial (which is currently the Iris
default)::

    >>> dask.set_options(get=dask.async.get_sync)

This option is particularly good for debugging scripts.


Chunks
------


Further reading
---------------

Dask offers much more fine control than is described in this user guide,
although a good understanding of the package would be required to properly
utilize it.

For example, it is possible to write callback functions to customize processing
options, of which there are many more than we have outlined.  Also, you may
wish to use some of the available Dask functionality regarding deferred
operations for your own scripts and objects.

For more information about these tools, how they work and what you can do with
them, please visit the following package documentation pages:

.. _Dask: http://dask.pydata.org/en/latest/
.. _Dask.distributed: http://distributed.readthedocs.io/en/latest/

`Dask`_
`Dask.distributed`_
