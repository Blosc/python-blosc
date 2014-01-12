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

Here it is the output of the included compare-pack-ptr.py benchmark:

```
Creating a large NumPy array with 10000000 int64 elements...
[      0       1       2 ..., 9999997 9999998 9999999]
Time for copying array with numpy.copy():     0.016 s.

Using *** blosclz *** compressor
Time for pack_array/unpack_array:     0.068/0.053 s.    Compr ratio: 136.24
Time for compress_ptr/decompress_ptr: 0.011/0.017 s.    Compr ratio: 136.83
Using *** lz4 *** compressor
Time for pack_array/unpack_array:     0.064/0.054 s.    Compr ratio: 136.73
Time for compress_ptr/decompress_ptr: 0.008/0.020 s.    Compr ratio: 137.19
Using *** lz4hc *** compressor
Time for pack_array/unpack_array:     0.163/0.074 s.    Compr ratio: 164.97
Time for compress_ptr/decompress_ptr: 0.105/0.028 s.    Compr ratio: 165.12
Using *** snappy *** compressor
Time for pack_array/unpack_array:     0.067/0.056 s.    Compr ratio: 20.36
Time for compress_ptr/decompress_ptr: 0.015/0.023 s.    Compr ratio: 20.38
Using *** zlib *** compressor
Time for pack_array/unpack_array:     0.271/0.099 s.    Compr ratio: 406.45
Time for compress_ptr/decompress_ptr: 0.222/0.061 s.    Compr ratio: 407.60
```

That means that Blosc in combination with LZ4 can compress at speeds
that can be up to 2x faster than a pure memcpy operation.  Decompression
is a bit slower probably because writing to memory is slower than
reading.  This was using a laptop with a i5-3380M CPU @ 2.90GHz, but
YMMV.

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
