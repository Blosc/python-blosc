########################################################################
#
#       License: MIT
#       Created: Jan 19, 2013
#       Author:  Francesc Alted - faltet@gmail.com
#
########################################################################

"""
Small benchmark that compares a plain NumPy array copy against
compression through different compressors in Blosc.
"""

from __future__ import print_function
import numpy as np
import time
import blosc
import ctypes

N = int(1e8)
clevel = 5

Nexp = np.log10(N)
print("Creating NumPy arrays with 10**%d int64/float64 elements:" % Nexp)
arrays = ((np.arange(N, dtype=np.int64), "the arange linear distribution"),
          (np.linspace(0, 1000, N), "the linspace linear distribution"),
          (np.random.random_integers(0, 1000, N), "the random distribution")
          )

in_ = arrays[0][0]
out_ = np.empty(in_.size, dtype=in_.dtype)
t0 = time.time()
#out_ = np.copy(in_)
out_ = ctypes.memmove(out_.__array_interface__['data'][0],
                      in_.__array_interface__['data'][0], N*8)
tcpy = time.time() - t0
print("  *** ctypes.memmove() *** Time for memcpy():\t%.3f s\t(%.2f GB/s)" % (
    tcpy, (N*8 / tcpy) / 2**30))

print("\nTimes for compressing/decompressing with clevel=%d and %d threads" % (
    clevel, blosc.ncores))
for (in_, label) in arrays:
    print("\n*** %s ***" % label)
    for cname in blosc.compressor_list():
        t0 = time.time()
        c = blosc.compress_ptr(in_.__array_interface__['data'][0],
                               in_.size, in_.dtype.itemsize,
                               clevel=clevel, shuffle=True, cname=cname)
        tc = time.time() - t0
        out = np.empty(in_.size, dtype=in_.dtype)
        t0 = time.time()
        blosc.decompress_ptr(c, out.__array_interface__['data'][0])
        td = time.time() - t0
        assert((in_ == out).all())
        print("  *** %-8s *** %6.3f s (%.2f GB/s) / %5.3f s (%.2f GB/s)" % (
            cname, tc, ((N*8 / tc) / 2**30), td, ((N*8 / td) / 2**30)), end='')
        print("\tCompr. ratio: %5.1fx" % (N*8. / len(c)))
