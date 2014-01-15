########################################################################
#
#       License: MIT
#       Created: May 4, 2013
#       Author:  Valentin Haenel - valentin@haenel.co
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
print("Creating a large NumPy array with 10**%d int64 elements:" % Nexp)
in_ = np.arange(N, dtype=np.int64)  # the trivial linear distribution
#in_ = np.linspace(0, 100, N)  # another linear distribution
#in_ = np.random.random_integers(0, 100, N)  # random distribution
print(" ", in_)

tic = time.time()
out_ = np.copy(in_)
toc = time.time()
print("  Time for copying array with np.copy():     %.3f s" % (toc-tic,))
print()

for cname in blosc.compressor_list():
    print("Using *** %s *** compressor::" % cname)
    ctic = time.time()
    c = blosc.pack_array(in_, clevel=clevel, shuffle=True, cname=cname)
    ctoc = time.time()
    dtic = time.time()
    out = blosc.unpack_array(c)
    dtoc = time.time()
    assert((in_ == out).all())
    print("  Time for pack_array/unpack_array:     %.3f/%.3f s." % \
          (ctoc-ctic, dtoc-dtic), end='')
    print("\tCompr ratio: %.2f" % (in_.size*in_.dtype.itemsize*1. / len(c)))

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
    print("  Time for compress_ptr/decompress_ptr: %.3f/%.3f s." % \
          (ctoc-ctic, dtoc-dtic), end='')
    print("\tCompr ratio: %.2f" % (in_.size*in_.dtype.itemsize*1. / len(c)))

