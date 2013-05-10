---------
Tutorials
---------

Using `python-blosc` (or just `blosc`, because we are going to talk always on
how to use it in a Python environment) is pretty easy.  It basically mimics
the API of the `zlib` module included in the standard Python library.

Here are some examples on how to use it.  For the full documentation, please
refer to the :ref:`reference` section.

Most of the times in this tutorial have been obtained using a VM with 2 cores
on top of a Intel(R) Core(TM) i7-3930K CPU @ 3.20GHz.

Compressing and decompressing with `blosc`
==========================================

Let's start creating a NumPy array with 80 MB full of data::

  >>> import numpy as np
  >>> a = np.linspace(0, 100, 1e7)
  >>> bytes_array = a.tostring()  # get a bytes stream

and let's compare Blosc operation with `zlib`::

  >>> import zlib
  >>> %time zpacked = zlib.compress(bytes_array)
  CPU times: user 4.03 s, sys: 0.03 s, total: 4.06 s
  Wall time: 4.08 s   # ~ 20 MB/s
  >>> import blosc
  >>> %time bpacked = blosc.compress(bytes_array, typesize=8)
  CPU times: user 0.10 s, sys: 0.00 s, total: 0.11 s
  Wall time: 0.05 s   # ~ 1.6 GB/s and 80x faster than zlib
  >>> time acp = a.copy()   # a direct copy using memcpy() behind the scenes
  CPU times: user 0.03 s, sys: 0.01 s, total: 0.04 s
  Wall time: 0.04 s   # ~ 2 GB/s, just a 25% faster than Blosc

Now, see at the compression ratios::

  >>> len(zpacked)
  52994692
  >>> len(bytes_array) / float(len(zpacked))
  1.5095851486409242   # zlib achieves a 1.5x compression ratio
  >>> len(bpacked)
  7641156
  >>> len(bytes_array) / float(len(bpacked))
  10.469620041784253   # blosc reaches more than 10x compression ratio

Wow, looks like `blosc` is very efficient compressing binary data.  How to
decompress?  Well, it is exactly the same way than `zlib`::

  >>> %time bytes_array2 = zlib.decompress(zpacked)
  CPU times: user 0.28 s, sys: 0.02 s, total: 0.30 s
  Wall time: 0.31 s   # ~ 260 MB/s
  >>> %time bytes_array2 = blosc.decompress(bpacked)
  CPU times: user 0.07 s, sys: 0.02 s, total: 0.09 s
  Wall time: 0.05 s   # ~ 1.6 GB/s and 6x times faster than zlib

Packaging NumPy arrays
======================

Want to use `blosc` to compress and decompress NumPy objects without having to
worry about passing the typesize for optimal compression, or having to create
the final container for decompression?  `blosc` comes with the `pack_array`
and `unpack_array` to perform this in a handy way::

  >>> a = np.linspace(0, 100, 1e7)
  >>> packed = blosc.pack_array(a)
  >>> a2 = blosc.unpack_array(packed)
  >>> np.alltrue(a == a2)
  True

Although this is an convenient way for compressing/decompresssing NumPy
arrays, this method uses pickle/unpickle behind the scenes.  This step implies
an additional copy, which takes both memory and time.

Compressing from a data pointer
===============================

For avoiding the data copy problem in the previous section, `blosc` comes with
a couple of lower-level functions: `compress_ptr` and `uncompress_ptr`.  Here
are they in action::

  >>> c = blosc.compress_ptr(a.__array_interface__['data'][0],
                             a.size, a.dtype.itemsize, 9, True)
  >>> a2 = numpy.empty(a.size, dtype=a.dtype)
  >>> blosc.decompress_ptr(c, a2.__array_interface__['data'][0])
  >>> (a == a2).all()
  True

As you see, these are really low level functions because you should pass
actual pointers where the data is, as well as the size and itemsize (for
compression).  Needless to say, it is very easy to cause a segfault by passing
incorrect paramaters to the functions (wrong pointer or wrong size).

On the other hand, and contrarily to the `pack_array` / `unpack_array` method,
the `compress_ptr` / `uncompress_ptr` functions do not need to make internal
copies, but you have to provide a container when doing the de-serialization.

It is up to you to decide among the convenience of `pack_array` /
`unpack_array` functions or the speed of `compress_ptr` / `uncompress_ptr`.

