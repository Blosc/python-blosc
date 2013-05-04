""" Benchmarking two techniques for compressing numpy arrays with python-blosc.

Here it is compared the 'traditional' way of using `pack_array` and
`unpack_array` versus the 'new' way via the `compress_ptr` and
`uncompress_ptr`.  Each has advantages and disadvantages.

The `pack_array` / `unpack_array` keeps NumPy objects metadata, so it
can de-serialize the arrays without a need to provide the container.
However, it uses pickle/unpickle internally, so it has to perform
expensive in-memory copies.

On the other hand, the `compress_ptr` / `uncompress_ptr` method does
not need to do internal copies, but you have to provide a container
when doing the de-serialization.  In addition, this method is much
closer to C Blosc, so if you are not careful enough specifying the
length or the itemsize properly, it is very easy ending with a
segfault.

It is up to the user to decide among the convenience of `pack_array` /
`unpack_array` functions or the speed of `compress_ptr` /
`uncompress_ptr`.

"""

import numpy
import time
import blosc

N = 3e7

print "Creating a large NumPy array with %d int64 elements..." % N
in_ = numpy.arange(N, dtype=numpy.int64)
print in_

tic = time.time()
c = blosc.pack_array(in_)
out = blosc.unpack_array(c)
assert((in_ == out).all())
toc = time.time()
print "Time for pack_array/unpack_array: %.3f s" % (toc-tic,)

tic = time.time()
c = blosc.compress_ptr(in_.__array_interface__['data'][0],
		       in_.size, in_.dtype.itemsize, 9, True)
out = numpy.empty(in_.size, dtype=in_.dtype)
blosc.decompress_ptr(c, out.__array_interface__['data'][0])
assert((in_ == out).all())
toc = time.time()
print "Time for compress_ptr/decompress_ptr: %.3f s" % (toc-tic,)

