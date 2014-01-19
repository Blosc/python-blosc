------------
Installation
------------

python-blosc comes with C Blosc sources, so it does not depend on any other
library (bar Python itself of course). Of course, if you are going to install
from sources, you are going to need a C compiler (GCC, clang and MSVC
2008/2010/2012 have been tested).

Also, there are situations where you may want to link with an already existing
Blosc library in your system.  You can do that too.

This package supports Python 2.6, 2.7 and 3.1, 3.2 and 3.3 or higher versions.

Installing from PyPI repository
===============================

Do:

.. code-block:: console

  $ easy_install -U blosc

or:

.. code-block:: console

  $ pip install -U blosc


Building manually
=================

First, go to the python-blosc official repository at
https://github.com/ContinuumIO/python-blosc and download the sources.

Then, there are different ways to compile python-blosc, depending if
you want to link with an already installed Blosc library or not.

Compiling without an installed Blosc library
--------------------------------------------

python-blosc comes with the Blosc sources with it so, assuming that you
have a C compiler installed, do:

.. code-block:: console

    $ python setup.py build_ext --inplace

That's all.  You can proceed with testing section now.

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

