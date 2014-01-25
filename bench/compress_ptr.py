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

N = 1e7
clevel = 9

Nexp = np.log10(N)
print("Creating different NumPy arrays with 10**%d int64/float64 elements:" % Nexp)
arrays = [None]*3
labels = [None]*3
arrays[0] = np.arange(N, dtype=np.int64)
labels[0] = "the arange linear distribution"
arrays[1] = np.linspace(0, 1000, N)
labels[1] = "the linspace linear distribution"
arrays[2] = np.random.random_integers(0, 1000, N)
labels[2] = "the random distribution"

tic = time.time()
out_ = np.copy(arrays[0])
toc = time.time()
print("  *** np.copy() **** Time for memcpy():     %.3f s" % (toc-tic,))

for (in_, label) in zip(arrays, labels):
    print("\n*** %s ***" % label)
    for cname in blosc.compressor_list():
        ctic = time.time()
        c = blosc.compress_ptr(in_.__array_interface__['data'][0],
                               in_.size, in_.dtype.itemsize,
                               clevel=clevel, shuffle=True, cname=cname)
        ctoc = time.time()
        out = np.empty(in_.size, dtype=in_.dtype)
        dtic = time.time()
        blosc.decompress_ptr(c, out.__array_interface__['data'][0])
        dtoc = time.time()
        assert((in_ == out).all())
        print("  *** %-8s *** Time for comp/decomp: %.3f/%.3f s." % \
              (cname, ctoc-ctic, dtoc-dtic), end='')
        print("\tCompr ratio: %6.2f" % (in_.size*in_.dtype.itemsize*1. / len(c)))
