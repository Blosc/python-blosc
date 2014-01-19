=============================
Announcing python-blosc 1.2.0
=============================

What is new?
============

This release adds support for the multiple compressors added in Blosc
1.3 series.  The new compressors are:

* lz4 (http://code.google.com/p/lz4/): A very fast
  compressor/decompressor.  Could be thought as a replacement of the
  original BloscLZ, but it can behave better is some scenarios.

* lz4hc (http://code.google.com/p/lz4/): This is a variation of LZ4
  that achieves much better compression ratio at the cost of being
  much slower for compressing.  Decompression speed is unaffected (and
  sometimes better than when using LZ4 itself!), so this is very good
  for read-only datasets.

* snappy (http://code.google.com/p/snappy/): A very fast
  compressor/decompressor.  Could be thought as a replacement of the
  original BloscLZ, but it can behave better is some scenarios.

* zlib (http://www.zlib.net/): This is a classic.  It achieves very
  good compression ratios, at the cost of speed.  However,
  decompression speed is still pretty good, so it is a good candidate
  for read-only datasets.

Selecting the compressor is just a matter of specifying the new `cname`
parameter in compression functions.  For example::

  in = numpy.arange(N, dtype=numpy.int64)
  out = blosc.pack_array(in, cname="lz4")

Here it is the output of the included compress-ptr.py benchmark::

  Creating different NumPy arrays with 10**7 int64/float64 elements:
    *** np.copy() **** Time for memcpy():     0.106 s

  *** the arange linear distribution ***
    *** blosclz  *** Time for comp/decomp: 0.034/0.077 s.	Compr ratio: 136.83
    *** lz4      *** Time for comp/decomp: 0.030/0.080 s.	Compr ratio: 137.19
    *** lz4hc    *** Time for comp/decomp: 0.370/0.097 s.	Compr ratio: 165.12
    *** snappy   *** Time for comp/decomp: 0.054/0.081 s.	Compr ratio:  20.38
    *** zlib     *** Time for comp/decomp: 0.415/0.170 s.	Compr ratio: 407.60

  *** the linspace linear distribution ***
    *** blosclz  *** Time for comp/decomp: 0.112/0.094 s.	Compr ratio:  10.47
    *** lz4      *** Time for comp/decomp: 0.063/0.084 s.	Compr ratio:  13.68
    *** lz4hc    *** Time for comp/decomp: 0.412/0.097 s.	Compr ratio:  70.84
    *** snappy   *** Time for comp/decomp: 0.099/0.341 s.	Compr ratio:   9.74
    *** zlib     *** Time for comp/decomp: 0.620/0.333 s.	Compr ratio:  79.11

  *** the random distribution ***
    *** blosclz  *** Time for comp/decomp: 0.102/0.210 s.	Compr ratio:   7.76
    *** lz4      *** Time for comp/decomp: 0.044/0.090 s.	Compr ratio:   7.76
    *** lz4hc    *** Time for comp/decomp: 0.352/0.103 s.	Compr ratio:   7.78
    *** snappy   *** Time for comp/decomp: 0.073/0.084 s.	Compr ratio:   6.01
    *** zlib     *** Time for comp/decomp: 0.709/0.218 s.	Compr ratio:   9.41

That means that Blosc in combination with LZ4 can compress at speeds
that can be up to 3x faster than a pure memcpy operation.  Decompression
is a bit slower (but still faster than memcpy()) probably because
writing to memory is slower than reading.  This was using an Intel Core
2 Duo at 2.13 GHz, runnng Python 3.3 and Mac OSX 10.9, but YMMV (and
will vary!).

For more info, you can have a look at the release notes in:

https://github.com/FrancescAlted/python-blosc/wiki/Release-notes

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

http://github.com/FrancescAlted/python-blosc


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

https://github.com/FrancescAlted/python-blosc/blob/master/LICENSES

for more details.



.. Local Variables:
.. mode: rst
.. coding: utf-8
.. fill-column: 72
.. End:
