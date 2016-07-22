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
E3-1245 v5 @ 3.5GHz, running Python 3.5 and Debian 16.04, but YMMV (and
will vary!)::

    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    python-blosc version: 1.3.4.dev0
    Blosc version: 1.10.0.dev ($Date:: 2016-07-20 #$)
    Compressors available: ['blosclz', 'lz4', 'lz4hc', 'snappy', 'zlib', 'zstd']
    Compressor library versions:
      BloscLZ: 1.0.5
      LZ4: 1.7.2
      Snappy: 1.1.1
      Zlib: 1.2.8
      Zstd: 0.7.4
    Python version: 3.5.2 |Continuum Analytics, Inc.| (default, Jul  2 2016, 17:53:06)
    [GCC 4.4.7 20120313 (Red Hat 4.4.7-1)]
    Platform: Linux-4.6.4-gentoo-x86_64 (#1 SMP Thu Jul 14 18:36:16 CEST 2016)
    Linux dist: debian stretch/sid
    Processor: x86_64
    Byte-ordering: little
    Detected cores: 8
    Number of threads to use by default: 4
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    Creating NumPy arrays with 10**8 int64/float64 elements:
      *** ctypes.memmove() *** Time for memcpy():	0.108 s	(6.87 GB/s)

    Times for compressing/decompressing with clevel=5 and 8 threads

    *** the arange linear distribution ***
      *** blosclz , noshuffle  ***  0.403 s (1.85 GB/s) / 0.106 s (7.06 GB/s)	Compr. ratio:   1.0x
      *** blosclz , shuffle    ***  0.070 s (10.62 GB/s) / 0.054 s (13.70 GB/s)	Compr. ratio:  57.1x
      *** blosclz , bitshuffle ***  0.135 s (5.50 GB/s) / 0.101 s (7.38 GB/s)	Compr. ratio:  74.0x
      *** lz4     , noshuffle  ***  0.388 s (1.92 GB/s) / 0.281 s (2.65 GB/s)	Compr. ratio:   2.0x
      *** lz4     , shuffle    ***  0.057 s (13.06 GB/s) / 0.065 s (11.42 GB/s)	Compr. ratio:  58.6x
      *** lz4     , bitshuffle ***  0.130 s (5.72 GB/s) / 0.106 s (7.06 GB/s)	Compr. ratio:  52.5x
      *** lz4hc   , noshuffle  ***  7.846 s (0.09 GB/s) / 0.242 s (3.08 GB/s)	Compr. ratio:   2.0x
      *** lz4hc   , shuffle    ***  0.120 s (6.21 GB/s) / 0.073 s (10.15 GB/s)	Compr. ratio: 137.2x
      *** lz4hc   , bitshuffle ***  1.729 s (0.43 GB/s) / 0.117 s (6.36 GB/s)	Compr. ratio: 208.9x
      *** snappy  , noshuffle  ***  0.399 s (1.87 GB/s) / 0.246 s (3.02 GB/s)	Compr. ratio:   2.0x
      *** snappy  , shuffle    ***  0.069 s (10.83 GB/s) / 0.105 s (7.10 GB/s)	Compr. ratio:  17.4x
      *** snappy  , bitshuffle ***  0.134 s (5.55 GB/s) / 0.159 s (4.67 GB/s)	Compr. ratio:  18.2x
      *** zlib    , noshuffle  ***  4.185 s (0.18 GB/s) / 0.549 s (1.36 GB/s)	Compr. ratio:   5.3x
      *** zlib    , shuffle    ***  0.675 s (1.10 GB/s) / 0.324 s (2.30 GB/s)	Compr. ratio: 237.3x
      *** zlib    , bitshuffle ***  0.713 s (1.05 GB/s) / 0.371 s (2.01 GB/s)	Compr. ratio: 305.4x
      *** zstd    , noshuffle  ***  4.134 s (0.18 GB/s) / 0.458 s (1.63 GB/s)	Compr. ratio:   7.8x
      *** zstd    , shuffle    ***  0.160 s (4.65 GB/s) / 0.078 s (9.58 GB/s)	Compr. ratio: 367.7x
      *** zstd    , bitshuffle ***  0.264 s (2.83 GB/s) / 0.121 s (6.15 GB/s)	Compr. ratio: 618.2x

    *** the linspace linear distribution ***
      *** blosclz , noshuffle  ***  0.426 s (1.75 GB/s) / 0.107 s (6.96 GB/s)	Compr. ratio:   1.0x
      *** blosclz , shuffle    ***  0.322 s (2.31 GB/s) / 0.075 s (9.96 GB/s)	Compr. ratio:   2.0x
      *** blosclz , bitshuffle ***  0.530 s (1.40 GB/s) / 0.135 s (5.52 GB/s)	Compr. ratio:   2.8x
      *** lz4     , noshuffle  ***  0.221 s (3.37 GB/s) / 0.105 s (7.07 GB/s)	Compr. ratio:   1.0x
      *** lz4     , shuffle    ***  0.196 s (3.80 GB/s) / 0.105 s (7.12 GB/s)	Compr. ratio:   3.2x
      *** lz4     , bitshuffle ***  0.252 s (2.96 GB/s) / 0.138 s (5.41 GB/s)	Compr. ratio:   4.9x
      *** lz4hc   , noshuffle  ***  2.797 s (0.27 GB/s) / 0.218 s (3.42 GB/s)	Compr. ratio:   1.2x
      *** lz4hc   , shuffle    ***  0.539 s (1.38 GB/s) / 0.073 s (10.25 GB/s)	Compr. ratio:  24.1x
      *** lz4hc   , bitshuffle ***  2.742 s (0.27 GB/s) / 0.118 s (6.34 GB/s)	Compr. ratio:  35.0x
      *** snappy  , noshuffle  ***  0.105 s (7.08 GB/s) / 0.105 s (7.10 GB/s)	Compr. ratio:   1.0x
      *** snappy  , shuffle    ***  0.235 s (3.17 GB/s) / 0.154 s (4.82 GB/s)	Compr. ratio:   4.2x
      *** snappy  , bitshuffle ***  0.327 s (2.28 GB/s) / 0.167 s (4.46 GB/s)	Compr. ratio:   6.1x
      *** zlib    , noshuffle  ***  5.358 s (0.14 GB/s) / 0.707 s (1.05 GB/s)	Compr. ratio:   1.6x
      *** zlib    , shuffle    ***  0.962 s (0.77 GB/s) / 0.292 s (2.55 GB/s)	Compr. ratio:  27.0x
      *** zlib    , bitshuffle ***  1.089 s (0.68 GB/s) / 0.342 s (2.18 GB/s)	Compr. ratio:  35.2x
      *** zstd    , noshuffle  ***  3.917 s (0.19 GB/s) / 0.453 s (1.64 GB/s)	Compr. ratio:   1.9x
      *** zstd    , shuffle    ***  0.410 s (1.82 GB/s) / 0.182 s (4.09 GB/s)	Compr. ratio:  40.7x
      *** zstd    , bitshuffle ***  0.556 s (1.34 GB/s) / 0.178 s (4.19 GB/s)	Compr. ratio:  48.7x

    *** the random distribution ***
      *** blosclz , noshuffle  ***  0.496 s (1.50 GB/s) / 0.105 s (7.10 GB/s)	Compr. ratio:   1.0x
      *** blosclz , shuffle    ***  0.184 s (4.05 GB/s) / 0.057 s (13.09 GB/s)	Compr. ratio:   3.9x
      *** blosclz , bitshuffle ***  0.177 s (4.20 GB/s) / 0.079 s (9.46 GB/s)	Compr. ratio:   6.1x
      *** lz4     , noshuffle  ***  0.366 s (2.04 GB/s) / 0.238 s (3.13 GB/s)	Compr. ratio:   2.1x
      *** lz4     , shuffle    ***  0.127 s (5.86 GB/s) / 0.083 s (8.94 GB/s)	Compr. ratio:   4.5x
      *** lz4     , bitshuffle ***  0.132 s (5.66 GB/s) / 0.107 s (6.95 GB/s)	Compr. ratio:   6.1x
      *** lz4hc   , noshuffle  ***  4.397 s (0.17 GB/s) / 0.117 s (6.36 GB/s)	Compr. ratio:   3.2x
      *** lz4hc   , shuffle    ***  3.185 s (0.23 GB/s) / 0.086 s (8.61 GB/s)	Compr. ratio:   5.4x
      *** lz4hc   , bitshuffle ***  0.414 s (1.80 GB/s) / 0.121 s (6.16 GB/s)	Compr. ratio:   6.2x
      *** snappy  , noshuffle  ***  0.428 s (1.74 GB/s) / 0.201 s (3.71 GB/s)	Compr. ratio:   2.2x
      *** snappy  , shuffle    ***  0.154 s (4.83 GB/s) / 0.124 s (6.02 GB/s)	Compr. ratio:   4.3x
      *** snappy  , bitshuffle ***  0.135 s (5.51 GB/s) / 0.132 s (5.66 GB/s)	Compr. ratio:   5.0x
      *** zlib    , noshuffle  ***  4.936 s (0.15 GB/s) / 0.441 s (1.69 GB/s)	Compr. ratio:   3.9x
      *** zlib    , shuffle    ***  2.916 s (0.26 GB/s) / 0.403 s (1.85 GB/s)	Compr. ratio:   6.1x
      *** zlib    , bitshuffle ***  1.088 s (0.68 GB/s) / 0.372 s (2.00 GB/s)	Compr. ratio:   6.3x
      *** zstd    , noshuffle  ***  5.572 s (0.13 GB/s) / 0.541 s (1.38 GB/s)	Compr. ratio:   4.2x
      *** zstd    , shuffle    ***  2.043 s (0.36 GB/s) / 0.127 s (5.87 GB/s)	Compr. ratio:   6.1x
      *** zstd    , bitshuffle ***  0.219 s (3.40 GB/s) / 0.126 s (5.93 GB/s)	Compr. ratio:   6.4x



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
<http://slides.zetatech.org/haenel-ep14-compress-me-stupid.pdf>`_ from the talk
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
