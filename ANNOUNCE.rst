=============================
Announcing python-blosc 1.1
=============================

What is it?
===========

A Python wrapper for the Blosc compression library.

Blosc (http://blosc.org) is a high performance compressor optimized for
binary data.  It has been designed to transmit data to the processor
cache faster than the traditional, non-compressed, direct memory fetch
approach via a memcpy() OS call.

Blosc works well for compressing numerical arrays that contains data
with relatively low entropy, like sparse data, time series, grids with
regular-spaced values, etc.

There is also a handy command line for Blosc called Bloscpack
(https://github.com/esc/bloscpack) that allows you to compress large
binary datafiles on-disk.  Although the format for Bloscpack has not
stabilized yet, it allows you to effectively use Blosc from your
favorite shell.


What is new?
============

- Added new `compress_ptr` and `decompress_ptr` functions that allows to
  compress and decompress from/to a data pointer.  These are low level
  calls and user must make sure that the pointer data area is safe.

- Since Blosc (the C library) already supports to be installed as an
  standalone library (via cmake), it is also possible to link
  python-blosc against a possible system-wide Blosc library.

- Many checks on types and ranges of values have been added.  Most of
  the calls are now much safer when passed the wrong values.

- Docstrings are much improved. Also, Sphinx-based docs are available
  now.

Many thanks to Valentin Hänel for his excellent work on this release.

For more info, you can see the release notes in:

https://github.com/FrancescAlted/python-blosc/wiki/Release-notes

More docs and examples are available in the Quick User's Guide wiki page:

https://github.com/FrancescAlted/python-blosc/wiki/Quick-User's-Guide

Download sources
================

Go to:

http://github.com/FrancescAlted/python-blosc

and download the most recent release from there.

Blosc is distributed using the MIT license, see LICENSES/BLOSC.txt for
details.

Mailing list
============

There is an official mailing list for Blosc at:

blosc@googlegroups.com
http://groups.google.es/group/blosc


.. Local Variables:
.. mode: rst
.. coding: utf-8
.. fill-column: 72
.. End:
