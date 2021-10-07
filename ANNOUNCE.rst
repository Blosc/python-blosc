==============================
Announcing python-blosc 1.10.6
==============================

What is new?
============

This is a maintenance release for including the cmake directory in
distributed files.

We are generating wheels for Intel (64 bits) and all major OS
(Win, Linux, Mac). In addition to extensions, we are distributing library
binaries in the wheels too.  This way, people willing to use the C-Blosc
library can make use of these wheels to install the necessary development
files.  For details, see:
https://github.com/Blosc/c-blosc/blob/master/COMPILING_WITH_WHEELS.rst

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
numerical arrays that contain data with relatively low entropy, like
sparse data, time series, grids with regular-spaced values, etc.

python-blosc (http://python-blosc.blosc.org/) is the Python wrapper for
the Blosc compression library, with added functions (`compress_ptr()`
and `pack_array()`) for efficiently compressing NumPy arrays, minimizing
the number of memory copies during the process.  python-blosc can be
used to compress in-memory data buffers for transmission to other
machines, persistence or just as a compressed cache.

There is also a handy tool built on top of python-blosc called Bloscpack
(https://github.com/Blosc/bloscpack). It features a command line
interface that allows you to compress large binary datafiles on-disk.
It also comes with a Python API that has built-in support for
serializing and deserializing Numpy arrays both on-disk and in-memory at
speeds that are competitive with regular Pickle/cPickle machinery.


Sources repository
==================

The sources and documentation are managed through github services at:

http://github.com/Blosc/python-blosc


Twitter
=======

Please follow @Blosc2 to get informed about the latest developments.


----

  **Enjoy data!**


.. Local Variables:
.. mode: rst
.. coding: utf-8
.. fill-column: 72
.. End:
.. vim: set tw=72:
