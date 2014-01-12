-----------------
Library Reference
-----------------

First level variables
=====================

.. py:attribute:: __version__

    The version of the carray package.

.. py:attribute:: blosclib_version

    The version of the Blosc C library.

.. py:attribute:: ncores

    The number of cores detected.


Public functions
================

.. automodule:: blosc
   :members: compress, compress_ptr, decompress, decompress_ptr, pack_array, unpack_array


Utilities
=========

.. automodule:: blosc
   :members: compressor_list, detect_number_of_cores, free_resources, set_nthreads, print_versions, test

