------------
Installation
------------

python-blosc comes with C Blosc sources, so it does not depend on any other
library (bar Python itself of course). Of course, if you are going to install
from sources, you are going to need a C compiler (GCC, clang and MSVC
2008/2010/2012/2015 have been tested).

Also, there are situations where you may want to link with an already existing
Blosc library in your system.  You can do that too.

This package supports Python 2.6, 2.7 and 3.3 or higher versions.

Installing from PyPI repository
===============================

Do:

.. code-block:: console

  $ pip install -U blosc


Building manually
=================

First, go to the python-blosc official repository at
https://github.com/Blosc/python-blosc and download the sources.

Then, there are different ways to compile python-blosc, depending on whether
you want to link with an already installed Blosc library or not.

Installing via setuptools
-------------------------

`setuptools` is limited to using the compiler specified in the environment 
variable `CC` which on posix systems is usually `gcc`. This often causes 
trouble with the Snappy codec, which is written in C++, and as a result Snappy
is no longer compiled by default. This problem is not known to affect MSVC or 
clang. Snappy is considered optional in Blosc as its compression performance 
is below that of the other codecs.

Any codec can be enabled (`=1`) or disabled (`=0`) on this build-path with the appropriate
OS environment variables `INCLUDE_LZ4`, `INCLUDE_SNAPPY`, `INCLUDE_ZLIB`, and 
`INCLUDE_ZLIB`. Snappy is disabled by default on posix systems.

`python-blosc` comes with the Blosc sources with it and can be built with:

.. code-block:: console

    $ python setup.py build_ext --inplace

That's all. You can proceed with testing section now.


Compiling with an installed Blosc library
-----------------------------------------

This approach uses pre-built, fully optimized versions of Blosc built via
CMake. 

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


Generating Sphinx documentation
-------------------------------

In case you want to generate the documentation locally, you will need to
have the `Sphinx` documentation system, as well as the `numpydoc`
extension, installed.  Then go down to `doc/` directory and do:

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

Or alternatively, you can use the third-party ``nosetests`` script to run both
the doctests and the test suite:

.. code-block:: console

    $ nosetests --with-doctest (add -v for verbose mode)

Once installed, you can re-run the tests at any time with:

.. code-block:: console

    $ python -c "import blosc; blosc.test()"

Installing
==========

Install it as a typical Python package:

.. code-block:: console

    $ python setup.py install
