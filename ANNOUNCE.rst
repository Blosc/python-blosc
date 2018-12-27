=============================
Announcing python-blosc 1.7.0
=============================

What is new?
============

This is a maintenance release which takes care of several housekeepting
tasks. Support for older versions of Python (2.6 and 3.3) has been
removed from the codebase. A new version of C-Blosc (1.5.1) that now
passes all unit and integration tests across all supported platforms has
been included. Finally, a the vendored cpuinfo.py has been upgraded and
the automatic tests on Windows via Appveyor have been upgraded to
include a larger variety of Windows/Python combinations.

A big thank you goes out to Daniel Stender from the Debian project for his
continued efforts to package the Blosc stack -- including python-blosc -- for
Debian. This also means it is likely that a recent version of
python-blosc will be included in Buster.

For more info, you can have a look at the release notes in:

https://github.com/Blosc/python-blosc/blob/master/RELEASE_NOTES.rst

More docs and examples are available in the documentation site:

http://python-blosc.blosc.org


What is it?
===========

Blosc (http://www.blosc.org) is a high performance compressor optimized
for binary data.  It has been designed to transmit data to the processor
cache faster than the traditional, non-compressed, direct memory fetch
approach via a memcpy() OS call.  Blosc works well for compressing
numerical arrays that contains data with relatively low entropy, like
sparse data, time series, grids with regular-spaced values, etc.

python-blosc (http://python-blosc.blosc.org/) is the Python wrapper for
the Blosc compression library, with added functions (`compress_ptr()`
and `pack_array()`) for efficiently compressing NumPy arrays, minimizing
the number of memory copies during the process.  python-blosc can be
used to compress in-memory data buffers for transmission to other
machines, persistence or just as a compressed cache.

There is also a handy tool built on top of python-blosc called Bloscpack
(https://github.com/Blosc/bloscpack). It features a commmand line
interface that allows you to compress large binary datafiles on-disk.
It also comes with a Python API that has built-in support for
serializing and deserializing Numpy arrays both on-disk and in-memory at
speeds that are competitive with regular Pickle/cPickle machinery.


Sources repository
==================

The sources and documentation are managed through github services at:

http://github.com/Blosc/python-blosc



----

  **Enjoy data!**


.. Local Variables:
.. mode: rst
.. coding: utf-8
.. fill-column: 72
.. End:
.. vim: set tw=72:
