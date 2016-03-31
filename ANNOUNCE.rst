=============================
Announcing python-blosc 1.3.0
=============================

What is new?
============

There is support for newest C-Blosc.  As such, C-Blosc 1.8.0 is being
distributed internally.  Support for the new `BITSHUFFLE` filter,
allowing for more compression ratios in many cases, at the expense of
some slowdown.  For details see:

http://python-blosc.blosc.org/tutorial.html#using-different-filters

You can also run some benchmarks including different codecs and filters:

https://github.com/Blosc/python-blosc/blob/master/bench/compress_ptr.py

For more info, you can have a look at the release notes in:

https://github.com/Blosc/python-blosc/blob/master/RELEASE_NOTES.rst

More docs and examples are available in the documentation site:

http://python-blosc.blosc.org


What is it?
===========

Blosc (http://www.blosc.org) is a high performance compressor
optimized for binary data.  It has been designed to transmit data to
the processor cache faster than the traditional, non-compressed,
direct memory fetch approach via a memcpy() OS call.

Blosc is the first compressor that is meant not only to reduce the size
of large datasets on-disk or in-memory, but also to accelerate object
manipulations that are memory-bound
(http://www.blosc.org/docs/StarvingCPUs.pdf).  See
http://www.blosc.org/synthetic-benchmarks.html for some benchmarks on
how much speed it can achieve in some datasets.

Blosc works well for compressing numerical arrays that contains data
with relatively low entropy, like sparse data, time series, grids with
regular-spaced values, etc.

python-blosc (http://python-blosc.blosc.org/) is the Python wrapper for
the Blosc compression library.

There is also a handy tool built on Blosc called Bloscpack
(https://github.com/Blosc/bloscpack). It features a commmand line
interface that allows you to compress large binary datafiles on-disk.
It also comes with a Python API that has built-in support for
serializing and deserializing Numpy arrays both on-disk and in-memory at
speeds that are competitive with regular Pickle/cPickle machinery.


Installing
==========

python-blosc is in PyPI repository, so installing it is easy:

$ pip install -U blosc  # yes, you must omit the 'python-' prefix


Download sources
================

The sources are managed through github services at:

http://github.com/Blosc/python-blosc


Documentation
=============

There is Sphinx-based documentation site at:

http://python-blosc.blosc.org/


Mailing list
============

There is an official mailing list for Blosc at:

blosc@googlegroups.com
http://groups.google.es/group/blosc


Licenses
========

Both Blosc and its Python wrapper are distributed using the MIT license.
See:

https://github.com/Blosc/python-blosc/blob/master/LICENSES

for more details.

----

  **Enjoy data!**


.. Local Variables:
.. mode: rst
.. coding: utf-8
.. fill-column: 72
.. End:
.. vim: set tw=72:
