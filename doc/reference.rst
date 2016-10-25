-----------------
Library Reference
-----------------

First level variables
=====================

.. py:attribute:: __version__

    The version of the blosc package.

.. py:attribute:: blosclib_version

    The version of the Blosc C library.

.. py:attribute:: clib_versions

    A map for the versions of the compression libraries included in C library.

.. py:attribute:: cnames

    The list of compressors included in C library.

.. py:attribute:: cname2clib

    A map between compressor names and its libraries (or formats).

.. py:attribute:: ncores

    The number of cores detected.


Public functions
================
.. automodule:: blosc
   :members: compress, compress_ptr, decompress, decompress_ptr, pack_array, unpack_array, clib_info, compressor_list, detect_number_of_cores, free_resources, get_clib, set_nthreads, set_blocksize, set_releasegil, print_versions, test

:mod:`blosc`

:func:`blosc.set_releasegil`

   