------------
Installation
------------

python-blosc comes with C Blosc sources, so it does not depend on any other
library (bar Python itself of course). Of course, if you are going to install
from sources, you are going to need a C compiler (GCC, clang and MSVC
2008/2010/2012 have been tested).


Installing from PyPI repository
===============================

Do::

  $ easy_install -U blosc

or::

  $ pip install -U blosc


Building from sources
=====================

Assuming that you have a C compiler installed, do::

    $ python setup.py build_ext --inplace

This package supports Python 2.6, 2.7, 3.1, 3.2 and 3.3 or higher versions.

Testing
=======

After compiling, you can quickly check that the package is sane by
running the doctests in ``blosc/test.py``::

    $ PYTHONPATH=.   (or "set PYTHONPATH=." on Win)
    $ export PYTHONPATH=.  (not needed on Win)
    $ python blosc/test.py  (add -v for verbose mode)

Or alternatively, you can use the third-party ``nosetests`` script to run both
the doctests and the test suite::

    $ nosetests --with-doctest (add -v for verbose mode)

Once installed, you can re-run the tests at any time with::

    $ python -c "import blosc; blosc.test()"

Installing
==========

Install it as a typical Python package::

    $ python setup.py install

