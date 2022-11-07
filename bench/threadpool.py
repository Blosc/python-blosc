"""
threadpool.py
Created on Sun Oct 23 12:03:46 2016
@author: Robert A. Mcleod - robbmcleod@gmail.com

Compares running blosc with and without GIL release, and compares various
combinations of ThreadPool threads and blosc-threads for operating on large
chunks.  The target is an image stack [50,1024,1024], where each frame can
be compressed as a chunk.
"""

import numpy as np
import time
import blosc
from multiprocessing.pool import ThreadPool

nRuns = 5
dtype='int64'
m = 48
N = 2048
MegaBytes = m * N * N * np.dtype(dtype).itemsize / 2**20
maxThreads = blosc.nthreads

BLOCKSIZE = 2**18
CLEVEL = 4
SHUFFLE = blosc.SHUFFLE
COMPRESSOR = 'zstd'

def compressSlice( args ):
    """
    args = (numpy array address, array_size, item_size, bytesList, bytesIndex)
    """
    args[3][args[4]] = blosc.compress_ptr( args[0],  args[1], args[2], \
                       clevel=CLEVEL, shuffle=SHUFFLE, cname=COMPRESSOR )

def decompressSlice( J, list_bytes ):

    pass

def compressStack( imageStack, blosc_threads = 1, pool_threads=maxThreads ):
    """
    Does frame compression using a ThreadPool to distribute the load.
    """
    blosc.set_nthreads( blosc_threads )
    tPool = ThreadPool( pool_threads )

    num_slices = imageStack.shape[0]
    # Build parameters list for the threaded processeses, consisting of index
    tArgs = [None] * num_slices
    itemSize = imageStack.dtype.itemsize
    bytesList = [None] * num_slices
    for J in np.arange(num_slices):
        tArgs[J] = (imageStack[J,:,:].__array_interface__['data'][0], \
                    N*N, itemSize, bytesList, J)

    # All operations are done 'in-place'
    tPool.map( compressSlice, tArgs )
    tPool.close()
    tPool.join()

def decompressStack( imageShape, imageDtype, blosc_threads = 1, pool_threads=maxThreads ):
    blosc.set_nthreads( blosc_threads )
    tPool = ThreadPool( pool_threads )

    num_slices = imageShape[0]
    imageStack = np.full(imageShape, fill_value=0)


blosc.print_versions()
blosc.set_blocksize( BLOCKSIZE )
print("Creating NumPy stack with %d float32 elements:" %(m*N*N) )

stack = np.zeros( [m,N,N], dtype=dtype )
xmesh, ymesh = np.meshgrid( np.arange(-N/2,N/2), np.arange(-N/2,N/2) )
compress_mesh = (np.cos( xmesh ) + np.exp( -ymesh**2 / N )).astype(dtype)
for J in np.arange(m):
    stack[J,:,:] = compress_mesh


### Determine arrangement of pool threads and blosc threads
testCases = int( np.floor( np.log2( maxThreads )) + 1 )
powProduct = 2**np.arange(0,testCases)
poolThreads = np.hstack( [1, powProduct] )
bloscThreads = np.hstack( [1, powProduct[::-1]] )
# Let's try instead just pool threads...
#poolThreads = np.arange( 1, maxThreads+1 )
#bloscThreads = np.ones_like( poolThreads )

solo_times = np.zeros_like( poolThreads, dtype='float64' )
solo_unlocked_times = np.zeros_like( poolThreads, dtype='float64' )
locked_times = np.zeros_like( poolThreads, dtype='float64' )
unlocked_times = np.zeros_like( poolThreads, dtype='float64' )

for J in np.arange(nRuns):
    print( "Run  %d of %d" % (J+1, nRuns) )
    blosc.set_releasegil(False)
    for I in np.arange( len(poolThreads) ):
        t1 = time.time()
        blosc.set_nthreads( bloscThreads[I] )
        blosc.compress_ptr( stack.__array_interface__['data'][0], stack.size, stack.dtype.itemsize, \
                       clevel=CLEVEL, shuffle=SHUFFLE, cname=COMPRESSOR )
        solo_times[I] += time.time() - t1

    blosc.set_releasegil(True)
    for I in np.arange( len(poolThreads) ):
        t2 = time.time()
        blosc.set_nthreads( bloscThreads[I] )
        blosc.compress_ptr( stack.__array_interface__['data'][0], stack.size, stack.dtype.itemsize, \
                       clevel=CLEVEL, shuffle=SHUFFLE, cname=COMPRESSOR )
        solo_unlocked_times[I] += time.time() - t2

    blosc.set_releasegil(True)
    for I in np.arange( len(poolThreads) ):
        t3 = time.time()
        compressStack( stack, blosc_threads=bloscThreads[I], pool_threads=poolThreads[I] )
        unlocked_times[I] += time.time() - t3


    blosc.set_releasegil(False)
    for I in np.arange( len(poolThreads) ):
        t4 = time.time()
        compressStack( stack, blosc_threads=bloscThreads[I], pool_threads=poolThreads[I] )
        locked_times[I] += time.time() - t4

solo_times /= nRuns
solo_unlocked_times /= nRuns
locked_times /= nRuns
unlocked_times /=nRuns
print( "##### NO PYTHON THREADPOOL -- GIL LOCKED #####" )
print( " -- Baseline normal blosc operation --" )
for I in np.arange( len(poolThreads) ):
    print( "    Compressed %.2f MB with %d pool threads, %d blosc threads in: %f s" \
      % ( MegaBytes, 0, bloscThreads[I], solo_times[I]) )
print( "##### NO PYTHON THREADPOOL -- GIL RELEASED #####" )
print( " -- Shows penalty for releasing GIL in normal blosc operation --" )
for I in np.arange( len(poolThreads) ):
    print( "    Compressed %.2f MB with %d pool threads, %d blosc threads in: %f s" \
      % ( MegaBytes, 0, bloscThreads[I], solo_unlocked_times[I]) )
print( "##### GIL LOCKED w/ PYTHON THREADPOOL #####" )
print( " -- Shows that GIL stops ThreadPool from working --" )
for I in np.arange( len(poolThreads) ):
    print( "    Compressed %.2f MB with %d pool threads, %d blosc threads in: %f s" \
      % ( MegaBytes, poolThreads[I], bloscThreads[I], locked_times[I]) )
print( "##### GIL RELEASED w/ PYTHON THREADPOOL #####" )
print( " -- Shows scaling between Python multiprocessing.threadPool and blosc threads --" )
for I in np.arange( len(poolThreads) ):
    print( "    Compressed %.2f MB with %d pool threads, %d blosc threads in: %f s" \
      % ( MegaBytes, poolThreads[I], bloscThreads[I], unlocked_times[I]) )
