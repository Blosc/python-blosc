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

Just to whet your appetite, here are the results for an Intel E3-1240 v3
@ 3.40GHz, running Python 2.7 and Gentoo Base System release 2.2, but
YMMV (and will vary!)::

    Creating NumPy arrays with 10**8 int64/float64 elements:
      *** ctypes.memmove() *** Time for memcpy():	0.269 s	(2.76 GB/s)

    Times for compressing/decompressing with clevel=5 and 8 threads

    *** the arange linear distribution ***
      *** blosclz , noshuffle  ***  0.560 s (1.33 GB/s) / 0.255 s (2.92 GB/s)	Compr. ratio:   1.0x
      *** blosclz , shuffle    ***  0.090 s (8.26 GB/s) / 0.066 s (11.22 GB/s)	Compr. ratio:  57.1x
      *** blosclz , bitshuffle ***  0.121 s (6.18 GB/s) / 0.111 s (6.69 GB/s)	Compr. ratio:  74.0x
      *** lz4     , noshuffle  ***  0.351 s (2.12 GB/s) / 0.208 s (3.58 GB/s)	Compr. ratio:   2.0x
      *** lz4     , shuffle    ***  0.063 s (11.76 GB/s) / 0.088 s (8.42 GB/s)	Compr. ratio:  58.6x
      *** lz4     , bitshuffle ***  0.115 s (6.47 GB/s) / 0.132 s (5.63 GB/s)	Compr. ratio:  52.5x
      *** lz4hc   , noshuffle  ***  8.607 s (0.09 GB/s) / 0.208 s (3.57 GB/s)	Compr. ratio:   2.0x
      *** lz4hc   , shuffle    ***  0.136 s (5.47 GB/s) / 0.088 s (8.44 GB/s)	Compr. ratio: 137.2x
      *** lz4hc   , bitshuffle ***  2.130 s (0.35 GB/s) / 0.136 s (5.50 GB/s)	Compr. ratio: 208.9x
      *** snappy  , noshuffle  ***  0.433 s (1.72 GB/s) / 0.241 s (3.09 GB/s)	Compr. ratio:   2.0x
      *** snappy  , shuffle    ***  0.071 s (10.47 GB/s) / 0.131 s (5.68 GB/s)	Compr. ratio:  17.4x
      *** snappy  , bitshuffle ***  0.129 s (5.78 GB/s) / 0.175 s (4.25 GB/s)	Compr. ratio:  18.2x
      *** zlib    , noshuffle  ***  5.295 s (0.14 GB/s) / 0.398 s (1.87 GB/s)	Compr. ratio:   5.3x
      *** zlib    , shuffle    ***  0.971 s (0.77 GB/s) / 0.391 s (1.91 GB/s)	Compr. ratio: 237.3x
      *** zlib    , bitshuffle ***  1.023 s (0.73 GB/s) / 0.445 s (1.67 GB/s)	Compr. ratio: 305.4x

    *** the linspace linear distribution ***
      *** blosclz , noshuffle  ***  0.446 s (1.67 GB/s) / 0.256 s (2.91 GB/s)	Compr. ratio:   1.0x
      *** blosclz , shuffle    ***  0.304 s (2.45 GB/s) / 0.089 s (8.36 GB/s)	Compr. ratio:   2.0x
      *** blosclz , bitshuffle ***  0.487 s (1.53 GB/s) / 0.174 s (4.29 GB/s)	Compr. ratio:   2.8x
      *** lz4     , noshuffle  ***  0.203 s (3.66 GB/s) / 0.255 s (2.92 GB/s)	Compr. ratio:   1.0x
      *** lz4     , shuffle    ***  0.188 s (3.95 GB/s) / 0.108 s (6.93 GB/s)	Compr. ratio:   3.2x
      *** lz4     , bitshuffle ***  0.248 s (3.01 GB/s) / 0.146 s (5.11 GB/s)	Compr. ratio:   4.9x
      *** lz4hc   , noshuffle  ***  2.846 s (0.26 GB/s) / 0.204 s (3.66 GB/s)	Compr. ratio:   1.2x
      *** lz4hc   , shuffle    ***  0.564 s (1.32 GB/s) / 0.081 s (9.18 GB/s)	Compr. ratio:  24.1x
      *** lz4hc   , bitshuffle ***  3.937 s (0.19 GB/s) / 0.130 s (5.73 GB/s)	Compr. ratio:  35.0x
      *** snappy  , noshuffle  ***  0.258 s (2.89 GB/s) / 0.257 s (2.90 GB/s)	Compr. ratio:   1.0x
      *** snappy  , shuffle    ***  0.245 s (3.04 GB/s) / 0.168 s (4.45 GB/s)	Compr. ratio:   4.2x
      *** snappy  , bitshuffle ***  0.299 s (2.49 GB/s) / 0.193 s (3.86 GB/s)	Compr. ratio:   6.1x
      *** zlib    , noshuffle  ***  6.570 s (0.11 GB/s) / 0.715 s (1.04 GB/s)	Compr. ratio:   1.6x
      *** zlib    , shuffle    ***  1.310 s (0.57 GB/s) / 0.337 s (2.21 GB/s)	Compr. ratio:  27.0x
      *** zlib    , bitshuffle ***  1.346 s (0.55 GB/s) / 0.384 s (1.94 GB/s)	Compr. ratio:  35.2x

    *** the random distribution ***
      *** blosclz , noshuffle  ***  0.556 s (1.34 GB/s) / 0.255 s (2.92 GB/s)	Compr. ratio:   1.0x
      *** blosclz , shuffle    ***  0.215 s (3.47 GB/s) / 0.067 s (11.19 GB/s)	Compr. ratio:   3.9x
      *** blosclz , bitshuffle ***  0.182 s (4.08 GB/s) / 0.103 s (7.24 GB/s)	Compr. ratio:   6.1x
      *** lz4     , noshuffle  ***  0.385 s (1.94 GB/s) / 0.138 s (5.39 GB/s)	Compr. ratio:   2.1x
      *** lz4     , shuffle    ***  0.134 s (5.57 GB/s) / 0.096 s (7.78 GB/s)	Compr. ratio:   4.5x
      *** lz4     , bitshuffle ***  0.127 s (5.89 GB/s) / 0.136 s (5.48 GB/s)	Compr. ratio:   6.1x
      *** lz4hc   , noshuffle  ***  5.188 s (0.14 GB/s) / 0.096 s (7.76 GB/s)	Compr. ratio:   3.2x
      *** lz4hc   , shuffle    ***  3.664 s (0.20 GB/s) / 0.095 s (7.86 GB/s)	Compr. ratio:   5.4x
      *** lz4hc   , bitshuffle ***  0.432 s (1.72 GB/s) / 0.139 s (5.38 GB/s)	Compr. ratio:   6.2x
      *** snappy  , noshuffle  ***  0.475 s (1.57 GB/s) / 0.244 s (3.06 GB/s)	Compr. ratio:   2.2x
      *** snappy  , shuffle    ***  0.176 s (4.24 GB/s) / 0.155 s (4.80 GB/s)	Compr. ratio:   4.3x
      *** snappy  , bitshuffle ***  0.136 s (5.49 GB/s) / 0.166 s (4.48 GB/s)	Compr. ratio:   5.0x
      *** zlib    , noshuffle  ***  5.383 s (0.14 GB/s) / 0.494 s (1.51 GB/s)	Compr. ratio:   3.9x
      *** zlib    , shuffle    ***  2.900 s (0.26 GB/s) / 0.407 s (1.83 GB/s)	Compr. ratio:   6.1x
      *** zlib    , bitshuffle ***  1.401 s (0.53 GB/s) / 0.436 s (1.71 GB/s)	Compr. ratio:   6.3x

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
