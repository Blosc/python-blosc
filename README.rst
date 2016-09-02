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
    python-blosc version: 1.4.2.dev0
    Blosc version: 1.11.0 ($Date:: 2016-09-02 #$)
    Compressors available: ['blosclz', 'lz4', 'lz4hc', 'snappy', 'zlib', 'zstd']
    Compressor library versions:
      BloscLZ: 1.0.5
      LZ4: 1.7.2
      Snappy: 1.1.1
      Zlib: 1.2.8
      Zstd: 1.0.0
    Python version: 3.5.2 |Continuum Analytics, Inc.| (default, Jul  2 2016, 17:53:06)
    [GCC 4.4.7 20120313 (Red Hat 4.4.7-1)]
    Platform: Linux-4.7.2-gentoo-x86_64 (#1 SMP Mon Aug 29 17:01:31 CEST 2016)
    Linux dist: debian stretch/sid
    Processor: x86_64
    Byte-ordering: little
    Detected cores: 8
    Number of threads to use by default: 4
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    Creating NumPy arrays with 10**8 int64/float64 elements:
      *** ctypes.memmove() *** Time for memcpy():	0.109 s	(6.82 GB/s)

    Times for compressing/decompressing with clevel=5 and 8 threads

    *** the arange linear distribution ***
      *** blosclz , noshuffle  ***  0.460 s (1.62 GB/s) / 0.106 s (7.06 GB/s)	Compr. ratio:   1.0x
      *** blosclz , shuffle    ***  0.069 s (10.74 GB/s) / 0.054 s (13.78 GB/s)	Compr. ratio:  57.1x
      *** blosclz , bitshuffle ***  0.128 s (5.84 GB/s) / 0.101 s (7.38 GB/s)	Compr. ratio:  74.0x
      *** lz4     , noshuffle  ***  0.422 s (1.77 GB/s) / 0.233 s (3.20 GB/s)	Compr. ratio:   2.0x
      *** lz4     , shuffle    ***  0.049 s (15.26 GB/s) / 0.070 s (10.63 GB/s)	Compr. ratio:  68.6x
      *** lz4     , bitshuffle ***  0.122 s (6.09 GB/s) / 0.130 s (5.73 GB/s)	Compr. ratio:  53.3x
      *** lz4hc   , noshuffle  ***  8.168 s (0.09 GB/s) / 0.254 s (2.93 GB/s)	Compr. ratio:   2.0x
      *** lz4hc   , shuffle    ***  0.560 s (1.33 GB/s) / 0.080 s (9.33 GB/s)	Compr. ratio:  97.5x
      *** lz4hc   , bitshuffle ***  5.399 s (0.14 GB/s) / 0.103 s (7.24 GB/s)	Compr. ratio: 179.2x
      *** snappy  , noshuffle  ***  0.356 s (2.09 GB/s) / 0.196 s (3.80 GB/s)	Compr. ratio:   2.0x
      *** snappy  , shuffle    ***  0.057 s (12.99 GB/s) / 0.102 s (7.34 GB/s)	Compr. ratio:  17.4x
      *** snappy  , bitshuffle ***  0.123 s (6.07 GB/s) / 0.143 s (5.22 GB/s)	Compr. ratio:  18.2x
      *** zlib    , noshuffle  ***  4.191 s (0.18 GB/s) / 0.507 s (1.47 GB/s)	Compr. ratio:   5.3x
      *** zlib    , shuffle    ***  0.991 s (0.75 GB/s) / 0.403 s (1.85 GB/s)	Compr. ratio: 120.8x
      *** zlib    , bitshuffle ***  1.080 s (0.69 GB/s) / 0.402 s (1.85 GB/s)	Compr. ratio: 260.1x
      *** zstd    , noshuffle  ***  4.207 s (0.18 GB/s) / 0.595 s (1.25 GB/s)	Compr. ratio:   7.8x
      *** zstd    , shuffle    ***  0.248 s (3.00 GB/s) / 0.072 s (10.41 GB/s)	Compr. ratio: 156.7x
      *** zstd    , bitshuffle ***  0.337 s (2.21 GB/s) / 0.124 s (6.02 GB/s)	Compr. ratio: 320.6x

    *** the linspace linear distribution ***
      *** blosclz , noshuffle  ***  0.465 s (1.60 GB/s) / 0.113 s (6.58 GB/s)	Compr. ratio:   1.0x
      *** blosclz , shuffle    ***  0.299 s (2.49 GB/s) / 0.085 s (8.74 GB/s)	Compr. ratio:   2.0x
      *** blosclz , bitshuffle ***  0.456 s (1.63 GB/s) / 0.154 s (4.83 GB/s)	Compr. ratio:   2.8x
      *** lz4     , noshuffle  ***  0.244 s (3.05 GB/s) / 0.110 s (6.78 GB/s)	Compr. ratio:   1.0x
      *** lz4     , shuffle    ***  0.193 s (3.86 GB/s) / 0.114 s (6.56 GB/s)	Compr. ratio:   3.2x
      *** lz4     , bitshuffle ***  0.266 s (2.80 GB/s) / 0.172 s (4.34 GB/s)	Compr. ratio:   5.0x
      *** lz4hc   , noshuffle  ***  4.121 s (0.18 GB/s) / 0.245 s (3.05 GB/s)	Compr. ratio:   1.2x
      *** lz4hc   , shuffle    ***  0.575 s (1.30 GB/s) / 0.085 s (8.81 GB/s)	Compr. ratio:   8.6x
      *** lz4hc   , bitshuffle ***  4.699 s (0.16 GB/s) / 0.146 s (5.09 GB/s)	Compr. ratio:  14.2x
      *** snappy  , noshuffle  ***  0.104 s (7.17 GB/s) / 0.105 s (7.12 GB/s)	Compr. ratio:   1.0x
      *** snappy  , shuffle    ***  0.218 s (3.41 GB/s) / 0.141 s (5.29 GB/s)	Compr. ratio:   4.2x
      *** snappy  , bitshuffle ***  0.320 s (2.33 GB/s) / 0.152 s (4.90 GB/s)	Compr. ratio:   6.1x
      *** zlib    , noshuffle  ***  6.210 s (0.12 GB/s) / 0.860 s (0.87 GB/s)	Compr. ratio:   1.6x
      *** zlib    , shuffle    ***  1.424 s (0.52 GB/s) / 0.451 s (1.65 GB/s)	Compr. ratio:  10.7x
      *** zlib    , bitshuffle ***  1.850 s (0.40 GB/s) / 0.383 s (1.94 GB/s)	Compr. ratio:  18.0x
      *** zstd    , noshuffle  ***  4.586 s (0.16 GB/s) / 0.398 s (1.87 GB/s)	Compr. ratio:   1.9x
      *** zstd    , shuffle    ***  0.754 s (0.99 GB/s) / 0.256 s (2.91 GB/s)	Compr. ratio:  14.2x
      *** zstd    , bitshuffle ***  0.893 s (0.83 GB/s) / 0.253 s (2.94 GB/s)	Compr. ratio:  22.2x

    *** the random distribution ***
      *** blosclz , noshuffle  ***  0.571 s (1.31 GB/s) / 0.116 s (6.43 GB/s)	Compr. ratio:   1.0x
      *** blosclz , shuffle    ***  0.203 s (3.66 GB/s) / 0.066 s (11.27 GB/s)	Compr. ratio:   3.9x
      *** blosclz , bitshuffle ***  0.236 s (3.16 GB/s) / 0.080 s (9.34 GB/s)	Compr. ratio:   6.1x
      *** lz4     , noshuffle  ***  0.399 s (1.87 GB/s) / 0.236 s (3.16 GB/s)	Compr. ratio:   2.4x
      *** lz4     , shuffle    ***  0.119 s (6.23 GB/s) / 0.096 s (7.78 GB/s)	Compr. ratio:   4.4x
      *** lz4     , bitshuffle ***  0.132 s (5.62 GB/s) / 0.182 s (4.10 GB/s)	Compr. ratio:   6.2x
      *** lz4hc   , noshuffle  ***  4.518 s (0.16 GB/s) / 0.107 s (6.98 GB/s)	Compr. ratio:   3.5x
      *** lz4hc   , shuffle    ***  1.260 s (0.59 GB/s) / 0.086 s (8.62 GB/s)	Compr. ratio:   5.2x
      *** lz4hc   , bitshuffle ***  0.313 s (2.38 GB/s) / 0.115 s (6.45 GB/s)	Compr. ratio:   6.2x
      *** snappy  , noshuffle  ***  0.478 s (1.56 GB/s) / 0.199 s (3.75 GB/s)	Compr. ratio:   2.2x
      *** snappy  , shuffle    ***  0.155 s (4.80 GB/s) / 0.125 s (5.94 GB/s)	Compr. ratio:   4.3x
      *** snappy  , bitshuffle ***  0.133 s (5.59 GB/s) / 0.133 s (5.61 GB/s)	Compr. ratio:   5.0x
      *** zlib    , noshuffle  ***  5.072 s (0.15 GB/s) / 0.408 s (1.83 GB/s)	Compr. ratio:   4.0x
      *** zlib    , shuffle    ***  2.672 s (0.28 GB/s) / 0.522 s (1.43 GB/s)	Compr. ratio:   5.5x
      *** zlib    , bitshuffle ***  1.255 s (0.59 GB/s) / 0.488 s (1.53 GB/s)	Compr. ratio:   6.2x
      *** zstd    , noshuffle  ***  6.834 s (0.11 GB/s) / 0.693 s (1.07 GB/s)	Compr. ratio:   4.2x
      *** zstd    , shuffle    ***  1.624 s (0.46 GB/s) / 0.125 s (5.96 GB/s)	Compr. ratio:   5.9x
      *** zstd    , bitshuffle ***  0.273 s (2.73 GB/s) / 0.107 s (6.95 GB/s)	Compr. ratio:   6.4x


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
