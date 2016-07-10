=============================
Announcing python-blosc 1.3.3
=============================

What is new?
============

This is a maintenance release that updates internal C-Blosc sources to
1.9.3 and uses default compiler optimization (maximum) because the latest
C-Blosc do not segfaults anymore with this setting.

For whetting your appetite, look at some benchmarks here:

https://github.com/Blosc/python-blosc#benchmarking

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
