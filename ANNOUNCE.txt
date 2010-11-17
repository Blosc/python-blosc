====================================================
 Announcing python-blosc *** version here ***
 A Python wrapper for the Blosc compression library
====================================================

What is it?
===========

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

#XXX version-specific blurb XXX#

For more info, you can see the release notes in:

https://github.com/FrancescAlted/python-blosc/wiki/Release-notes

Basic Usage
===========

# Create a binary string made of int (32-bit) elements
>>> import array
>>> a = array.array('i', range(10*1000*1000))
>>> bytes_array = a.tostring()

# Compress it
>>> import blosc
>>> bpacked = blosc.compress(bytes_array, typesize=a.itemsize)
>>> len(bytes_array) / len(bpacked)
110      # 110x compression ratio.  Not bad!

# Compression speed?
>>> from timeit import timeit
>>> timeit("blosc.compress(bytes_array, a.itemsize)",
           "import blosc, array; \
            a = array.array('i', range(10*1000*1000)); \
            bytes_array = a.tostring()", \
            number=10)
0.040534019470214844
>>> len(bytes_array)*10 / 0.0405 / (1024*1024*1024)
9.1982476505232444  # wow, compressing at ~ 9 GB/s.  That's fast!
# This is actually much faster than a `memcpy` system call
>>> timeit("ctypes.memmove(b.buffer_info()[0], a.buffer_info()[0], \
            len(a)*a.itemsize)",
            "import array, ctypes; \
            a = array.array('i', range(10*1000*1000)); \
            b = a[::-1]", number=10)
0.10316681861877441
>>> len(bytes_array)*10 / 0.1031 / (1024*1024*1024)
3.6132786600018565  # ~ 3.6 GB/s is memcpy speed

# Decompress it
>>> bytes_array2 = blosc.decompress(bpacked)
# Check whether our data have had a good trip
>>> bytes_array == bytes_array2
True    # yup, it seems so

# Decompression speed?
>>> timeit("s2 = blosc.decompress(bpacked)",
           "import blosc, array; \
            a = array.array('i', range(10*1000*1000)); \
            bytes_array = a.tostring(); \
            bpacked = blosc.compress(bytes_array, a.itemsize)", \
            number=10)
0.083872079849243164
> len(bytes_array)*10 / 0.0838 / (1024*1024*1024)
4.4454538167803275  # decompressing at ~ 4.4 GB/s is pretty good too!

[Using a machine with 8 physical cores with hyper-threading]

The above examples use maximum compression level 9 (default), and
although lower compression levels produce smaller compression ratios,
they are also faster (reaching speeds exceeding 11 GB/s).

More examples showing other features (and using NumPy arrays) are
available on the python-blosc wiki page:

http://github.com/FrancescAlted/python-blosc/wiki

Documentation
=============

Please refer to docstrings.  Start by the main package:

>>> import blosc
>>> help(blosc)

and ask for more docstrings in the referenced functions.

Download sources
================

Go to:

http://github.com/FrancescAlted/python-blosc

and download the most recent release from here.

Blosc is distributed using the MIT license, see LICENSES/BLOSC.txt for
details.

Mailing list
============

There is an official mailing list for Blosc at:

blosc@googlegroups.com
http://groups.google.es/group/blosc


----

  **Enjoy data!**
