python-blosc: a Python wrapper for the extremely fast Blosc compression library
===============================================================================

:Author: Francesc Alted
:Author: Valentin Hänel
:Contact: faltet@gmail.com
:Contact: valentin@haenel.co
:URL: https://github.com/Blosc/python-blosc
:URL: http://python-blosc.blosc.org
:Travis CI: |travis|
:Appveyor: |appveyor|
:PyPi: |version| |pypi|

.. |travis| image:: https://travis-ci.org/Blosc/python-blosc.png?branch=master
        :target: https://travis-ci.org/Blosc/python-blosc
.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/dexdkko8omge6o3s/branch/master?svg=true
        :target: https://ci.appveyor.com/project/FrancescAlted/python-blosc/branch/master
.. |pypi| image:: https://img.shields.io/pypi/dm/blosc.png
        :target: https://pypi.python.org/pypi/blosc
.. |version| image:: https://img.shields.io/pypi/v/blosc.png
        :target: https://pypi.python.org/pypi/blosc


What it is
==========

Blosc (http://blosc.org) is a high performance compressor optimized for
binary data.  It has been designed to transmit data to the processor
cache faster than the traditional, non-compressed, direct memory fetch
approach via a memcpy() OS call.

Blosc works well for compressing numerical arrays that contains data
with relatively low entropy, like sparse data, time series, grids with
regular-spaced values, etc.

python-blosc a Python package that wraps Blosc.  python-blosc supports
Python 2.6, 2.7 and 3.4 or higher versions.

Building
========

There are different ways to compile python-blosc, depending if you want
to link with an already installed Blosc library or not.

Compiling with an installed Blosc library (recommended)
-------------------------------------------------------

Python and Blosc-powered extensions have a difficult relationship when
compiled using GCC, so this is why using an external C-Blosc library is
recommended for maximum performance (for details, see
https://github.com/Blosc/python-blosc/issues/110).

Go to https://github.com/Blosc/c-blosc/releases and download and install
the C-Blosc library.  Then, you can tell python-blosc where is the
C-Blosc library in a couple of ways:

Using an environment variable:

.. code-block:: console

    $ BLOSC_DIR=/usr/local     (or "set BLOSC_DIR=\blosc" on Win)
    $ export BLOSC_DIR         (not needed on Win)
    $ python setup.py build_ext --inplace
 
Using a flag:

.. code-block:: console

    $ python setup.py build_ext --inplace --blosc=/usr/local

Compiling without an installed Blosc library
--------------------------------------------

*Warning:* This way of compiling is discouraged for performance reasons.
See the previous section.

python-blosc also comes with the Blosc sources with it so, assuming that
you have a C++ compiler installed, do:

.. code-block:: console

    $ python setup.py build_ext --inplace

That's all.  You can proceed with testing section now.

Note: The requirement for the C++ compiler is just for the Snappy
dependency.  The rest of the other components of Blosc are pure C
(including the LZ4, Zstd and Zlib libraries).

Testing
=======

After compiling, you can quickly check that the package is sane by
running the doctests in ``blosc/test.py``:

.. code-block:: console

    $ PYTHONPATH=.   (or "set PYTHONPATH=." on Win)
    $ export PYTHONPATH=.  (not needed on Win)
    $ python blosc/test.py  (add -v for verbose mode)

Or alternatively, you can use the third-party ``nosetests`` script:

.. code-block:: console

    $ nosetests --with-doctest (add -v for verbose mode)

Once installed, you can re-run the tests at any time with:

.. code-block:: console

    $ python -c "import blosc; blosc.test()"

Benchmarking
============

If curious, you may want to run a small benchmark that compares a plain
NumPy array copy against compression through different compressors in
your Blosc build:

.. code-block:: console

  $ PYTHONPATH=. python bench/compress_ptr.py

Just to whet your appetite, here are the results for an Intel Xeon
E5-2695 v3 @ 2.30GHz, running Python 3.5, CentOS 7, but YMMV (and
will vary!)::

  -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
  python-blosc version: 1.5.1.dev0
  Blosc version: 1.11.2 ($Date:: 2017-01-27 #$)
  Compressors available: ['blosclz', 'lz4', 'lz4hc', 'snappy', 'zlib', 'zstd']
  Compressor library versions:
    BloscLZ: 1.0.5
    LZ4: 1.7.5
    Snappy: 1.1.1
    Zlib: 1.2.7
    Zstd: 1.1.2
  Python version: 3.5.2 |Continuum Analytics, Inc.| (default, Jul  2 2016, 17:53:06) 
  [GCC 4.4.7 20120313 (Red Hat 4.4.7-1)]
  Platform: Linux-3.10.0-327.18.2.el7.x86_64-x86_64 (#1 SMP Thu May 12 11:03:55 UTC 2016)
  Linux dist: CentOS Linux 7.2.1511
  Processor: x86_64
  Byte-ordering: little
  Detected cores: 56
  Number of threads to use by default: 4
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
  Creating NumPy arrays with 10**8 int64/float64 elements:
    *** ctypes.memmove() *** Time for memcpy():	0.276 s	(2.70 GB/s)

  Times for compressing/decompressing with clevel=5 and 24 threads

  *** the arange linear distribution ***
    *** blosclz , noshuffle  ***  0.382 s (1.95 GB/s) / 0.300 s (2.48 GB/s)	Compr. ratio:   1.0x
    *** blosclz , shuffle    ***  0.042 s (17.77 GB/s) / 0.027 s (27.18 GB/s)	Compr. ratio:  57.1x
    *** blosclz , bitshuffle ***  0.094 s (7.94 GB/s) / 0.041 s (18.28 GB/s)	Compr. ratio:  74.0x
    *** lz4     , noshuffle  ***  0.156 s (4.79 GB/s) / 0.052 s (14.30 GB/s)	Compr. ratio:   2.0x
    *** lz4     , shuffle    ***  0.033 s (22.58 GB/s) / 0.034 s (22.03 GB/s)	Compr. ratio:  68.6x
    *** lz4     , bitshuffle ***  0.059 s (12.63 GB/s) / 0.053 s (14.18 GB/s)	Compr. ratio:  33.1x
    *** lz4hc   , noshuffle  ***  0.443 s (1.68 GB/s) / 0.070 s (10.62 GB/s)	Compr. ratio:   2.0x
    *** lz4hc   , shuffle    ***  0.102 s (7.31 GB/s) / 0.029 s (25.42 GB/s)	Compr. ratio:  97.5x
    *** lz4hc   , bitshuffle ***  0.206 s (3.62 GB/s) / 0.038 s (19.85 GB/s)	Compr. ratio: 180.5x
    *** snappy  , noshuffle  ***  0.154 s (4.84 GB/s) / 0.056 s (13.28 GB/s)	Compr. ratio:   2.0x
    *** snappy  , shuffle    ***  0.044 s (16.89 GB/s) / 0.047 s (15.95 GB/s)	Compr. ratio:  17.4x
    *** snappy  , bitshuffle ***  0.064 s (11.58 GB/s) / 0.061 s (12.26 GB/s)	Compr. ratio:  18.2x
    *** zlib    , noshuffle  ***  1.172 s (0.64 GB/s) / 0.135 s (5.50 GB/s)	Compr. ratio:   5.3x
    *** zlib    , shuffle    ***  0.260 s (2.86 GB/s) / 0.086 s (8.67 GB/s)	Compr. ratio: 120.8x
    *** zlib    , bitshuffle ***  0.262 s (2.84 GB/s) / 0.094 s (7.96 GB/s)	Compr. ratio: 260.1x
    *** zstd    , noshuffle  ***  0.973 s (0.77 GB/s) / 0.093 s (8.00 GB/s)	Compr. ratio:   7.8x
    *** zstd    , shuffle    ***  0.093 s (7.97 GB/s) / 0.023 s (32.71 GB/s)	Compr. ratio: 156.7x
    *** zstd    , bitshuffle ***  0.115 s (6.46 GB/s) / 0.029 s (25.60 GB/s)	Compr. ratio: 320.6x

  *** the linspace linear distribution ***
    *** blosclz , noshuffle  ***  0.341 s (2.19 GB/s) / 0.291 s (2.56 GB/s)	Compr. ratio:   1.0x
    *** blosclz , shuffle    ***  0.132 s (5.65 GB/s) / 0.023 s (33.10 GB/s)	Compr. ratio:   2.0x
    *** blosclz , bitshuffle ***  0.166 s (4.50 GB/s) / 0.036 s (20.89 GB/s)	Compr. ratio:   2.8x
    *** lz4     , noshuffle  ***  0.142 s (5.26 GB/s) / 0.028 s (27.07 GB/s)	Compr. ratio:   1.0x
    *** lz4     , shuffle    ***  0.093 s (8.01 GB/s) / 0.030 s (24.87 GB/s)	Compr. ratio:   3.4x
    *** lz4     , bitshuffle ***  0.102 s (7.31 GB/s) / 0.039 s (19.13 GB/s)	Compr. ratio:   5.3x
    *** lz4hc   , noshuffle  ***  0.700 s (1.06 GB/s) / 0.044 s (16.77 GB/s)	Compr. ratio:   1.1x
    *** lz4hc   , shuffle    ***  0.203 s (3.67 GB/s) / 0.021 s (36.22 GB/s)	Compr. ratio:   8.6x
    *** lz4hc   , bitshuffle ***  0.342 s (2.18 GB/s) / 0.028 s (26.50 GB/s)	Compr. ratio:  14.2x
    *** snappy  , noshuffle  ***  0.271 s (2.75 GB/s) / 0.274 s (2.72 GB/s)	Compr. ratio:   1.0x
    *** snappy  , shuffle    ***  0.099 s (7.54 GB/s) / 0.042 s (17.55 GB/s)	Compr. ratio:   4.2x
    *** snappy  , bitshuffle ***  0.127 s (5.86 GB/s) / 0.043 s (17.20 GB/s)	Compr. ratio:   6.1x
    *** zlib    , noshuffle  ***  1.525 s (0.49 GB/s) / 0.158 s (4.70 GB/s)	Compr. ratio:   1.6x
    *** zlib    , shuffle    ***  0.346 s (2.15 GB/s) / 0.098 s (7.59 GB/s)	Compr. ratio:  10.7x
    *** zlib    , bitshuffle ***  0.420 s (1.78 GB/s) / 0.104 s (7.20 GB/s)	Compr. ratio:  18.0x
    *** zstd    , noshuffle  ***  1.061 s (0.70 GB/s) / 0.096 s (7.79 GB/s)	Compr. ratio:   1.9x
    *** zstd    , shuffle    ***  0.203 s (3.68 GB/s) / 0.052 s (14.21 GB/s)	Compr. ratio:  14.2x
    *** zstd    , bitshuffle ***  0.251 s (2.97 GB/s) / 0.047 s (15.84 GB/s)	Compr. ratio:  22.2x

  *** the random distribution ***
    *** blosclz , noshuffle  ***  0.340 s (2.19 GB/s) / 0.285 s (2.61 GB/s)	Compr. ratio:   1.0x
    *** blosclz , shuffle    ***  0.091 s (8.21 GB/s) / 0.017 s (44.29 GB/s)	Compr. ratio:   3.9x
    *** blosclz , bitshuffle ***  0.080 s (9.27 GB/s) / 0.029 s (26.12 GB/s)	Compr. ratio:   6.1x
    *** lz4     , noshuffle  ***  0.150 s (4.95 GB/s) / 0.027 s (28.05 GB/s)	Compr. ratio:   2.4x
    *** lz4     , shuffle    ***  0.068 s (11.02 GB/s) / 0.029 s (26.03 GB/s)	Compr. ratio:   4.5x
    *** lz4     , bitshuffle ***  0.063 s (11.87 GB/s) / 0.054 s (13.70 GB/s)	Compr. ratio:   6.2x
    *** lz4hc   , noshuffle  ***  0.645 s (1.15 GB/s) / 0.019 s (39.22 GB/s)	Compr. ratio:   3.5x
    *** lz4hc   , shuffle    ***  0.257 s (2.90 GB/s) / 0.022 s (34.62 GB/s)	Compr. ratio:   5.1x
    *** lz4hc   , bitshuffle ***  0.128 s (5.80 GB/s) / 0.029 s (25.52 GB/s)	Compr. ratio:   6.2x
    *** snappy  , noshuffle  ***  0.164 s (4.54 GB/s) / 0.048 s (15.46 GB/s)	Compr. ratio:   2.2x
    *** snappy  , shuffle    ***  0.082 s (9.09 GB/s) / 0.043 s (17.39 GB/s)	Compr. ratio:   4.3x
    *** snappy  , bitshuffle ***  0.071 s (10.48 GB/s) / 0.046 s (16.08 GB/s)	Compr. ratio:   5.0x
    *** zlib    , noshuffle  ***  1.223 s (0.61 GB/s) / 0.093 s (7.97 GB/s)	Compr. ratio:   4.0x
    *** zlib    , shuffle    ***  0.636 s (1.17 GB/s) / 0.126 s (5.89 GB/s)	Compr. ratio:   5.5x
    *** zlib    , bitshuffle ***  0.327 s (2.28 GB/s) / 0.109 s (6.81 GB/s)	Compr. ratio:   6.2x
    *** zstd    , noshuffle  ***  1.432 s (0.52 GB/s) / 0.103 s (7.27 GB/s)	Compr. ratio:   4.2x
    *** zstd    , shuffle    ***  0.388 s (1.92 GB/s) / 0.031 s (23.71 GB/s)	Compr. ratio:   5.9x
    *** zstd    , bitshuffle ***  0.127 s (5.86 GB/s) / 0.033 s (22.77 GB/s)	Compr. ratio:   6.4x


In case you find your own results interesting, please report them back
to the authors!

Installing
==========

Install it as a typical Python package:

.. code-block:: console

    $ python setup.py install

Documentation
=============

The Sphinx based documentation is here:

http://python-blosc.blosc.org

Also, some examples are available on python-blosc wiki page:

http://github.com/blosc/python-blosc/wiki

Lastly, here is the `recording
<https://www.youtube.com/watch?v=rilU44j_wUU&list=PLNkWzv63CorW83NY3U93gUar645jTXpJF&index=15>`_
and the `slides
<http://www.blosc.org/docs/haenel-ep14-compress-me-stupid.pdf>`_ from the talk
"Compress me stupid" at the EuroPython 2014.

Mailing list
============

Discussion about this module is welcome in the Blosc list:

blosc@googlegroups.com

http://groups.google.es/group/blosc

----

  **Enjoy data!**


.. Local Variables:
.. mode: rst
.. coding: utf-8
.. fill-column: 72
.. End:
