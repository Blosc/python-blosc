blosc: a Python package that wraps the Blosc compressor
=======================================================

:Author: Francesc Alted i Abad
:Contact: faltet@pytables.org
:URL: http://blosc.pytables.org

What it is
==========

Blosc (http://blosc.pytables.org) is a high performance compressor
optimized for binary data.  It has been designed to transmit data to
the processor cache faster than the traditional, non-compressed,
direct memory fetch approach via a memcpy() OS call.

Blosc works well for compressing numerical arrays that contains data
with relatively low entropy, like sparse data, time series, grids with
regular-spaced values, etc.

This is a Python package that wraps it.

Building
========

Assuming that you have a C compiler installed, do:

$ python setup.py build_ext --inplace

This package supports Python 2.6, 2.7 and 3.1 or higher versions.

Testing
=======

After compiling, you can quickly check that the package is sane by
running:

$ PYTHONPATH=.   (or "set PYTHONPATH=." on Win)
$ export PYTHONPATH=.  (not needed on Win)
$ python blosc/toplevel.py  (add -v for verbose mode)

Installing
==========

Install it as a typical Python package:

$ python setup.py install

Documentation
=============

Please refer to docstrings.  Start by the main package:

>>> import blosc
>>> help(blosc)

and ask for more docstrings in the referenced functions.

Also, some examples are available on python-blosc wiki page:

http://github.com/FrancescAlted/python-blosc/wiki

Mailing list
============

Discussion about this module is welcome in the Blosc list:

blosc@googlegroups.com
http://groups.google.es/group/blosc
