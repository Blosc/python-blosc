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
.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/esc/python-blosc 
        :target: https://ci.appveyor.com/project/esc/python-blosc/branch/master 
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

Compiling without an installed Blosc library
--------------------------------------------

python-blosc come with the Blosc sources with it so, assuming that you
have a C++ compiler installed, do:

.. code-block:: console

    $ python setup.py build_ext --inplace

That's all.  You can proceed with testing section now.

Note: The requirement for the C++ compiler is just for the Snappy
dependency.  The rest of the other components of Blosc are pure C
(including the LZ4 and Zlib libraries).

Compiling with an installed Blosc library
-----------------------------------------

In case you have Blosc installed as an external library (and disregard
the included Blosc sources) you can link with it in a couple of ways.

Using an environment variable:

.. code-block:: console

    $ BLOSC_DIR=/usr/local     (or "set BLOSC_DIR=\blosc" on Win)
    $ export BLOSC_DIR         (not needed on Win)
    $ python setup.py build_ext --inplace

Using a flag:

.. code-block:: console

    $ python setup.py build_ext --inplace --blosc=/usr/local

Generating Sphinx documentation
-------------------------------

In case you want to generate the documentation locally, you will need to
have the Sphinx documentation system, as well as the numpydoc
extension, installed.  Then go down to ``doc/`` directory and do:

.. code-block:: console

    $ make html|latex|latexpdf

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

Just to wet you appetite, here are the results for an Intel Core 2 Duo
at 2.13 GHz, running Python 3.3 and Mac OSX 10.9, but YMMV (and will
vary!)::

  Creating different NumPy arrays with 10**7 int64/float64 elements:
    *** np.copy() **** Time for memcpy():     0.106 s

  *** the arange linear distribution ***
    *** blosclz  *** Time for comp/decomp: 0.034/0.077 s.	Compr ratio: 136.83
    *** lz4      *** Time for comp/decomp: 0.030/0.080 s.	Compr ratio: 137.19
    *** lz4hc    *** Time for comp/decomp: 0.370/0.097 s.	Compr ratio: 165.12
    *** snappy   *** Time for comp/decomp: 0.054/0.081 s.	Compr ratio:  20.38
    *** zlib     *** Time for comp/decomp: 0.415/0.170 s.	Compr ratio: 407.60

  *** the linspace linear distribution ***
    *** blosclz  *** Time for comp/decomp: 0.112/0.094 s.	Compr ratio:  10.47
    *** lz4      *** Time for comp/decomp: 0.063/0.084 s.	Compr ratio:  13.68
    *** lz4hc    *** Time for comp/decomp: 0.412/0.097 s.	Compr ratio:  70.84
    *** snappy   *** Time for comp/decomp: 0.099/0.341 s.	Compr ratio:   9.74
    *** zlib     *** Time for comp/decomp: 0.620/0.333 s.	Compr ratio:  79.11

  *** the random distribution ***
    *** blosclz  *** Time for comp/decomp: 0.102/0.210 s.	Compr ratio:   7.76
    *** lz4      *** Time for comp/decomp: 0.044/0.090 s.	Compr ratio:   7.76
    *** lz4hc    *** Time for comp/decomp: 0.352/0.103 s.	Compr ratio:   7.78
    *** snappy   *** Time for comp/decomp: 0.073/0.084 s.	Compr ratio:   6.01
    *** zlib     *** Time for comp/decomp: 0.709/0.218 s.	Compr ratio:   9.41

That means that Blosc in combination with LZ4 can compress at speeds
that can be up to 3x faster than a pure memcpy operation.  Decompression
is a bit slower (but still faster than ``memcpy()``) probably because
writing to memory is slower than reading.

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
