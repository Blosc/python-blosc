=============================
Announcing python-blosc 1.2.1
=============================

What is new?
============

- Updated to c-blosc 1.3.3.

- Added a new `cname2clib` map for programatically determine the library
  associated to a compressor.

- New `get_clib(cbuffer)` that tells which compression library format
  has been used to created the compressed `cbuffer`.

For more info, you can have a look at the release notes in:

https://github.com/Blosc/python-blosc/wiki/Release-notes

More docs and examples are available in the documentation site:

http://blosc.pydata.org


What is it?
===========

python-blosc (http://blosc.pydata.org/) is a Python wrapper for the
Blosc compression library.

Blosc (http://blosc.org) is a high performance compressor optimized for
binary data.  It has been designed to transmit data to the processor
cache faster than the traditional, non-compressed, direct memory fetch
approach via a memcpy() OS call.  Whether this is achieved or not
depends of the data compressibility, the number of cores in the system,
and other factors.  See a series of benchmarks conducted for many
different systems: http://blosc.org/trac/wiki/SyntheticBenchmarks.

Blosc works well for compressing numerical arrays that contains data
with relatively low entropy, like sparse data, time series, grids with
regular-spaced values, etc.

There is also a handy command line for Blosc called Bloscpack
(https://github.com/esc/bloscpack) that allows you to compress large
binary datafiles on-disk.  Although the format for Bloscpack has not
stabilized yet, it allows you to effectively use Blosc from your
favorite shell.


Installing
==========

python-blosc is in PyPI repository, so installing it is easy:

$ pip install -U blosc  # yes, you should omit the python- prefix


Download sources
================

The sources are managed through github services at:

http://github.com/Blosc/python-blosc


Documentation
=============

There is Sphinx-based documentation site at:

http://blosc.pydata.org/


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
