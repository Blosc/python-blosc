=============================
Announcing python-blosc 1.0.5
=============================

What is it?
===========

A Python wrapper for the Blosc compression library.

Blosc (http://blosc.pytables.org) is a high performance compressor
optimized for binary data.  It has been designed to transmit data to
the processor cache faster than the traditional, non-compressed,
direct memory fetch approach via a memcpy() OS call.

Blosc works well for compressing numerical arrays that contains data
with relatively low entropy, like sparse data, time series, grids with
regular-spaced values, etc.

python-blosc is a Python package that wraps it.

What is new?
============

- Upgraded to latest Blosc 1.1.4.

- Better handling of condition errors, and improved memory releasing in
  case of errors (thanks to Valentin Haenel and Han Genuit).

- Better handling of types (should compile without warning now, at least
  with GCC).

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
