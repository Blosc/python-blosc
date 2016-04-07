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
.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/FrancescAlted/python-blosc
        :target: https://ci.appveyor.com/project/FrancescAlted/python-blosc/branch/master
.. |pypi| image:: https://pypip.in/d/blosc/badge.png
        :target: https://pypi.python.org/pypi/blosc
.. |version| image:: https://pypip.in/v/blosc/badge.png
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
Python 2.6, 2.7 and 3.1, 3.2, 3.3 or higher versions.

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
(including the LZ4 and Zlib libraries).

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

Just to wet you appetite, here are the results for an Intel E3-1240 v3 @
3.40GHz, running Python 2.7 and Gentoo Base System release 2.2, but YMMV
(and will vary!)::

    Creating NumPy arrays with 10**8 int64/float64 elements:
      *** ctypes.memmove() *** Time for memcpy():   0.295 s (2.53 GB/s)

    Times for compressing/decompressing with clevel=5 and 8 threads

    *** the arange linear distribution ***
      *** blosclz , noshuffle  ***  0.455 s (1.64 GB/s) / 0.087 s (8.58 GB/s)       Compr. ratio:   1.0x
      *** blosclz , shuffle    ***  0.108 s (6.93 GB/s) / 0.075 s (10.00 GB/s)      Compr. ratio:  57.1x
      *** blosclz , bitshuffle ***  0.120 s (6.19 GB/s) / 0.107 s (6.97 GB/s)       Compr. ratio:  74.0x
      *** lz4     , noshuffle  ***  0.342 s (2.18 GB/s) / 0.212 s (3.52 GB/s)       Compr. ratio:   2.0x
      *** lz4     , shuffle    ***  0.078 s (9.54 GB/s) / 0.093 s (8.02 GB/s)       Compr. ratio:  58.6x
      *** lz4     , bitshuffle ***  0.116 s (6.41 GB/s) / 0.135 s (5.53 GB/s)       Compr. ratio:  52.5x
      *** lz4hc   , noshuffle  ***  8.142 s (0.09 GB/s) / 0.212 s (3.52 GB/s)       Compr. ratio:   2.0x
      *** lz4hc   , shuffle    ***  0.140 s (5.33 GB/s) / 0.092 s (8.06 GB/s)       Compr. ratio: 137.2x
      *** lz4hc   , bitshuffle ***  1.572 s (0.47 GB/s) / 0.142 s (5.25 GB/s)       Compr. ratio: 208.9x
      *** snappy  , noshuffle  ***  0.381 s (1.95 GB/s) / 0.244 s (3.06 GB/s)       Compr. ratio:   2.0x
      *** snappy  , shuffle    ***  0.073 s (10.25 GB/s) / 0.136 s (5.48 GB/s)      Compr. ratio:  17.4x
      *** snappy  , bitshuffle ***  0.126 s (5.92 GB/s) / 0.177 s (4.22 GB/s)       Compr. ratio:  18.2x
      *** zlib    , noshuffle  ***  5.298 s (0.14 GB/s) / 0.401 s (1.86 GB/s)       Compr. ratio:   5.3x
      *** zlib    , shuffle    ***  0.974 s (0.76 GB/s) / 0.393 s (1.90 GB/s)       Compr. ratio: 237.3x
      *** zlib    , bitshuffle ***  1.026 s (0.73 GB/s) / 0.444 s (1.68 GB/s)       Compr. ratio: 305.4x

    *** the linspace linear distribution ***
      *** blosclz , noshuffle  ***  0.434 s (1.72 GB/s) / 0.088 s (8.45 GB/s)       Compr. ratio:   1.0x
      *** blosclz , shuffle    ***  0.298 s (2.50 GB/s) / 0.090 s (8.32 GB/s)       Compr. ratio:   2.0x
      *** blosclz , bitshuffle ***  0.476 s (1.56 GB/s) / 0.166 s (4.50 GB/s)       Compr. ratio:   2.8x
      *** lz4     , noshuffle  ***  0.219 s (3.41 GB/s) / 0.088 s (8.45 GB/s)       Compr. ratio:   1.0x
      *** lz4     , shuffle    ***  0.190 s (3.92 GB/s) / 0.112 s (6.63 GB/s)       Compr. ratio:   3.2x
      *** lz4     , bitshuffle ***  0.248 s (3.00 GB/s) / 0.149 s (5.00 GB/s)       Compr. ratio:   4.9x
      *** lz4hc   , noshuffle  ***  2.797 s (0.27 GB/s) / 0.211 s (3.53 GB/s)       Compr. ratio:   1.2x
      *** lz4hc   , shuffle    ***  0.528 s (1.41 GB/s) / 0.085 s (8.78 GB/s)       Compr. ratio:  24.1x
      *** lz4hc   , bitshuffle ***  2.918 s (0.26 GB/s) / 0.131 s (5.71 GB/s)       Compr. ratio:  35.0x
      *** snappy  , noshuffle  ***  0.088 s (8.49 GB/s) / 0.087 s (8.61 GB/s)       Compr. ratio:   1.0x
      *** snappy  , shuffle    ***  0.235 s (3.16 GB/s) / 0.176 s (4.24 GB/s)       Compr. ratio:   4.2x
      *** snappy  , bitshuffle ***  0.317 s (2.35 GB/s) / 0.198 s (3.76 GB/s)       Compr. ratio:   6.1x
      *** zlib    , noshuffle  ***  6.569 s (0.11 GB/s) / 0.718 s (1.04 GB/s)       Compr. ratio:   1.6x
      *** zlib    , shuffle    ***  1.313 s (0.57 GB/s) / 0.339 s (2.20 GB/s)       Compr. ratio:  27.0x
      *** zlib    , bitshuffle ***  1.348 s (0.55 GB/s) / 0.380 s (1.96 GB/s)       Compr. ratio:  35.2x

    *** the random distribution ***
      *** blosclz , noshuffle  ***  0.517 s (1.44 GB/s) / 0.087 s (8.60 GB/s)       Compr. ratio:   1.0x
      *** blosclz , shuffle    ***  0.212 s (3.52 GB/s) / 0.070 s (10.62 GB/s)      Compr. ratio:   3.9x
      *** blosclz , bitshuffle ***  0.181 s (4.13 GB/s) / 0.104 s (7.16 GB/s)       Compr. ratio:   6.1x
      *** lz4     , noshuffle  ***  0.373 s (2.00 GB/s) / 0.149 s (5.00 GB/s)       Compr. ratio:   2.1x
      *** lz4     , shuffle    ***  0.135 s (5.52 GB/s) / 0.101 s (7.36 GB/s)       Compr. ratio:   4.5x
      *** lz4     , bitshuffle ***  0.129 s (5.77 GB/s) / 0.138 s (5.39 GB/s)       Compr. ratio:   6.1x
      *** lz4hc   , noshuffle  ***  4.684 s (0.16 GB/s) / 0.101 s (7.36 GB/s)       Compr. ratio:   3.2x
      *** lz4hc   , shuffle    ***  3.223 s (0.23 GB/s) / 0.101 s (7.37 GB/s)       Compr. ratio:   5.4x
      *** lz4hc   , bitshuffle ***  0.429 s (1.74 GB/s) / 0.139 s (5.36 GB/s)       Compr. ratio:   6.2x
      *** snappy  , noshuffle  ***  0.461 s (1.62 GB/s) / 0.257 s (2.90 GB/s)       Compr. ratio:   2.2x
      *** snappy  , shuffle    ***  0.166 s (4.49 GB/s) / 0.160 s (4.66 GB/s)       Compr. ratio:   4.3x
      *** snappy  , bitshuffle ***  0.136 s (5.48 GB/s) / 0.167 s (4.45 GB/s)       Compr. ratio:   5.0x
      *** zlib    , noshuffle  ***  5.383 s (0.14 GB/s) / 0.499 s (1.49 GB/s)       Compr. ratio:   3.9x
      *** zlib    , shuffle    ***  2.903 s (0.26 GB/s) / 0.408 s (1.83 GB/s)       Compr. ratio:   6.1x
      *** zlib    , bitshuffle ***  1.403 s (0.53 GB/s) / 0.433 s (1.72 GB/s)

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
