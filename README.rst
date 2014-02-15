blosc: a Python wrapper for the extremely fast Blosc compression library
========================================================================

:Author: Francesc Alted
:Author: Valentin Hänel
:Contact: faltet@gmail.com
:Contact: valentin@haenel.co
:URL: https://github.com/Blosc/python-blosc
:URL: http://blosc.pydata.org
:Travis CI: |travis|
:PyPi: |version| |pypi|

.. |travis| image:: https://travis-ci.org/Blosc/python-blosc.png?branch=master
        :target: https://travis-ci.org/Blosc/python-blosc
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

There are diferent ways to compile python-blosc, depending if you want
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
at 2.13 GHz, runnng Python 3.3 and Mac OSX 10.9, but YMMV (and will
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

In case you find your onw results interesting, please report them back
to the authors!

Installing
==========

Install it as a typical Python package:

.. code-block:: console

    $ python setup.py install

Documentation
=============

Please refer to docstrings.  Start by the main package:

.. code-block:: pycon

    >>> import blosc
    >>> help(blosc)

and ask for more docstrings in the referenced functions.

The Sphinx based documentation is here:

http://www.blosc.org

Also, some examples are available on python-blosc wiki page:

http://github.com/blosc/python-blosc/wiki



Merging Blosc sources from upstream
===================================

We use the `subtree merge technique
<http://git-scm.com/book/en/Git-Tools-Subtree-Merging>`_ to maintain the
upstream Blosc sources. However, we do not use the technique exactly as
listed in the Pro-Git book.

The reason is quite technical: adding the Blosc Git repository as a
remote will also include the Blosc tags in your repository.  Since the
Blosc and python-blosc repositories share the same tagging scheme,
i.e. ``v.X.Y.Z``, we may have potentially conflicting tags. For example,
one might want to tag python-blosc ``v1.2.3``, however, since Blosc
already has a tag of this name, Git will deny you creating this. One
could use the ``--no-tags`` option for ``git fetch`` when fetching Blosc
-- but alas, this would defeat the purpose.  The tagged versions of
Blosc are exactly the ones we are interested in for the subtree merge!
So, as a compromise there is a shell script ``subtree-merge-blosc.sh``.
This accepts a single tag as argument and does a plain ``git
fetch``. This has the effect of fetching the commit that the requested
tag points to, but not actually fetching that tag or any of the other
tags.

It is not perfect and can probably be improved upon, but it does have
some comments in the source, checks for some common errors and tries to
abort as early as possible in case things go wrong. A sample invocation
is shown below:

.. code-block:: console

    $ ./subtree-merge-blosc.sh v1.2.3
    found remote tag: '4eda92c4dcba18849d482f5014b374d8b4b4cdfc	refs/tags/v1.2.3'
    warning: no common commits
    remote: Counting objects: 1558, done.
    remote: Compressing objects: 100% (606/606), done.
    remote: Total 1558 (delta 958), reused 1528 (delta 932)
    Receiving objects: 100% (1558/1558), 468.67 KiB | 304 KiB/s, done.
    Resolving deltas: 100% (958/958), done.
    From git://github.com/Blosc/c-blosc
     + tag               v1.2.3     -> FETCH_HEAD
    Squash commit -- not updating HEAD
    Automatic merge went well; stopped before committing as requested
    [subtree-merge-blosc.sh b7a7378] subtree merge blosc v1.2.3
     16 files changed, 60 insertions(+), 43 deletions(-)


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
