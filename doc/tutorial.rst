---------
Tutorials
---------

Using `python-blosc` (or just `blosc`, because we are going to talk always on
how to use it in a Python environment) is pretty easy.  It basically mimics
the API of the `zlib` module included in the standard Python library.

Here are some examples on how to use it.  For the full documentation, please
refer to the :ref:`reference` section.

Most of the times in this tutorial have been obtained using a VM with 2 cores
on top of a Intel(R) Core(TM) i5-3380M CPU @ 2.90GHz.

Compressing and decompressing with `blosc`
==========================================

Let's start creating a NumPy array with 80 MB full of data::

  >>> import numpy as np
  >>> a = np.linspace(0, 100, 1e7)
  >>> bytes_array = a.tostring()  # get a bytes stream

and let's compare Blosc operation with `zlib` (please note that we are
using IPython for leveraging its timing capabilities)::

  >>> import zlib
  >>>%time zpacked = zlib.compress(bytes_array)
  CPU times: user 5.17 s, sys: 14 ms, total: 5.19 s
  Wall time: 5.2 s    # ~ 15 MB/s
  >>> import blosc
  >>> %time bpacked = blosc.compress(bytes_array, typesize=8)
  CPU times: user 125 ms, sys: 0 ns, total: 125 ms
  Wall time: 38.8 ms  # ~ 2.0 GB/s and 130x faster than zlib
  >>> %time acp = a.copy()   # a direct copy using memcpy() behind the scenes
  CPU times: user 15 ms, sys: 8 ms, total: 23 ms
  Wall time: 22.6 ms  # ~ 3.5 GB/s, just a 1.7x faster than Blosc

Now, see at the compression ratios::

  >>> len(zpacked)
  52994692
  >>> len(bytes_array) / float(len(zpacked))
  1.5095851486409242   # zlib achieves a 1.5x compression ratio
  >>> len(bpacked)
  7641156
  >>> len(bytes_array) / float(len(bpacked))
  10.469620041784253   # blosc reaches more than 10x compression ratio

Wow, looks like Blosc is very efficient compressing binary data.  How
to decompress?  Well, it is exactly the same way than Zlib::

  >>> %time bytes_array2 = zlib.decompress(zpacked)
  CPU times: user 345 ms, sys: 9 ms, total: 354 ms
  Wall time: 354 ms   # ~ 225 MB/s
  >>> %time bytes_array2 = blosc.decompress(bpacked)
  CPU times: user 82 ms, sys: 10 ms, total: 92 ms
  Wall time: 36.3 ms   # ~ 2.2 GB/s and ~ 10x times faster than zlib


Using different compressors inside Blosc
========================================

Since Blosc 1.3.0, you can use different compressors inside it.  That
allows for these compressors to leverage Blosc powerful
multi-threading and shuffling machinery.

The examples above where using the default 'blosclz' compressor.  Here
there is another example using 'zlib'::

  >>> %time bpacked = blosc.compress(bytes_array, typesize=8, cname='zlib')
  CPU times: user 1.09 s, sys: 15 ms, total: 1.1 s
  Wall time: 290 ms   # ~ 275 MB/s and 18x faster than plain zlib

So, by using Zlib inside Blosc we can make it work at speeds that are
up to 18x faster than plain Zlib.  How that can be?  Well, as said
before, Blosc has efficient machinery for dealing with binary data
(shuffling) and leveraging multithreading.  In addition, it uses block
sizes for compressing data that are typically smaller than Zlib, so
the cost for compressing is further reduced.

In terms of compression ratio, 'zlib' inside Blosc behaves very well
too::

  >>> len(bpacked)
  1011304     #  ~ 7.5x smaller than blosclz and ~ 50x than plain zlib

So, 'zlib' here can do a much better job than 'blosclz', although at
the expenses of being slower (7.5x).

Decompression speed is pretty good too::

  >>> %time bytes_array2 = blosc.decompress(bpacked)
  CPU times: user 209 ms, sys: 9 ms, total: 218 ms
  Wall time: 67.6 ms  # ~ 1.2 GB/s and 5x faster than plain zlib

So, when mixing Zlib and Blosc, we can easily achieve decompression
speeds above 1 GB/s, which is quite impressive for a relatively slow
compressor like Zlib.

You can play with other compressors too, like 'lz4', 'lz4hc' and
'snappy'. 'lz4' and snappy are in the same class than 'blosclz', so
you can expect similar results.  However, 'lz4hc' is variation of
'lz4' that typically spends more time compressing for a better
compression ratio, so it is very good for read-only data.

Supporting the buffer interface
===============================

As of version 1.2.8 python-blosc supports compressing and decompressing from
any bytes-like object that supports the buffer-interface: this includes
`buffer`, `memoryview` and `bytearray`::

    >>> input_bytes = b"abcdefghijklmnopqrstuvwxyz"

    >>> blosc.compress(input_bytes, typesize=1)
    '\x02\x01\x03\x01\x1a\x00\x00\x00\x1a\x00\x00\x00*\x00\x00\x00abcdefghijklmnopqrstuvwxyz'

    >>> blosc.compress(memoryview(input_bytes), typesize=1)
    '\x02\x01\x03\x01\x1a\x00\x00\x00\x1a\x00\x00\x00*\x00\x00\x00abcdefghijklmnopqrstuvwxyz'

    >>> blosc.compress(bytearray(input_bytes), typesize=1)
    '\x02\x01\x03\x01\x1a\x00\x00\x00\x1a\x00\x00\x00*\x00\x00\x00abcdefghijklmnopqrstuvwxyz'

    >>> compressed = blosc.compress(input_bytes, typesize=1)

    >>> blosc.decompress(compressed)
    'abcdefghijklmnopqrstuvwxyz'

    >>> blosc.decompress(memoryview(compressed))
    'abcdefghijklmnopqrstuvwxyz'

    >>> blosc.decompress(bytearray(compressed))
    'abcdefghijklmnopqrstuvwxyz'

Note however, that there are subtle differences between Python 2.x and 3.x.
For example, in Python 2.x we can compress/decompress both `str` and `unicode`
types, whereas in Python 3.x we can only compress 'binary' data which does
*not* include `unicode`.


Packaging NumPy arrays
======================

Want to use `blosc` to compress and decompress NumPy objects without having to
worry about passing the typesize for optimal compression, or having to create
the final container for decompression?  `blosc` comes with the `pack_array`
and `unpack_array` to perform this in a handy way::

  >>> a = np.linspace(0, 100, 1e7)
  >>> %time packed = blosc.pack_array(a)
  CPU times: user 172 ms, sys: 84 ms, total: 256 ms
  Wall time: 151 ms
  >>> %time a2 = blosc.unpack_array(packed)
  CPU times: user 116 ms, sys: 60 ms, total: 176 ms
  Wall time: 104 ms
  >>> np.alltrue(a == a2)
  True

Although this is a convenient way for compressing/decompressing NumPy
arrays, this method uses pickle/unpickle behind the scenes.  This step
implies additional copies, which takes both memory and time.


Compressing from a data pointer
===============================

For avoiding the data copy problem in the previous section, `blosc`
comes with a couple of lower-level functions: `compress_ptr` and
`decompress_ptr`.  Here are they in action::

  >>> %time c = blosc.compress_ptr(a.__array_interface__['data'][0], a.size,
                             a.dtype.itemsize, 9, True)
  CPU times: user 144 ms, sys: 0 ns, total: 144 ms
  Wall time: 37.2 ms
  >>> a2 = numpy.empty(a.size, dtype=a.dtype)
  >>> %time blosc.decompress_ptr(c, a2.__array_interface__['data'][0])
  CPU times: user 80 ms, sys: 0 ns, total: 80 ms
  Wall time: 24.9 ms
  80000000L
  >>> (a == a2).all()
  True

As you see, these are really low level functions because you should
pass actual pointers where the data is, as well as the size and
itemsize (for compression).  Needless to say, it is very easy to cause
a segfault by passing incorrect parameters to the functions (wrong
pointer or wrong size).

On the other hand, and contrarily to the `pack_array` / `unpack_array`
method, the `compress_ptr` / `decompress_ptr` functions do not need to
make internal copies of the data buffers, so they are extremely fast
(as much as the C-Blosc library can be), but you have to provide a
container when doing the de-serialization.


Packing NumPy arrays with Bloscpack
===================================

While `pack_array` / `unpack_array` have been designed for convenience
and `compress_ptr` / `decompress_ptr` have been designed for speed
there is also a third option that combines the best of both worlds:
`Bloscpack <https://github.com/esc/bloscpack>`_. Since version 0.4.0,
Bloscpack is able to natively `de/serialize NumPy arrays
<https://github.com/esc/bloscpack#numpy>`_::

  >>> import bloscpack as bp
  >>> %time bp_packed = bp.pack_ndarray_str(a)
  CPU times: user 152 ms, sys: 20 ms, total: 172 ms
  Wall time: 76.8 ms
  >>> %time bp_unpacked  = unpack_ndarray_str(bp_packed)
  CPU times: user 100 ms, sys: 8 ms, total: 108 ms
  Wall time: 58 ms
  >>> (a == bp_unpacked).all()
  True
