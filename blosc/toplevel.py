########################################################################
#
#       License: MIT
#       Created: September 22, 2010
#       Author:  Francesc Alted - faltet@pytables.org
#
########################################################################

import os
import sys
try:
    import cPickle as pickle
except ImportError:
    import pickle

from blosc import blosc_extension as _ext
import blosc  # needed for running doctests from nosetests

if sys.version_info[0] < 3:
    int_ = (int, long)
else:
    int_ = (int,)

def detect_number_of_cores():
    """
    detect_number_of_cores()

    Detect the number of cores in this system.

    Returns
    -------
    out : int
        The number of cores in this system.

    """
    # Linux, Unix and MacOS:
    if hasattr(os, "sysconf"):
        if "SC_NPROCESSORS_ONLN" in os.sysconf_names:
            # Linux & Unix:
            ncpus = os.sysconf("SC_NPROCESSORS_ONLN")
            if isinstance(ncpus, int) and ncpus > 0:
                return ncpus
        else:  # OSX:
            return int(os.popen2("sysctl -n hw.ncpu")[1].read())
    # Windows:
    if "NUMBER_OF_PROCESSORS" in os.environ:
        ncpus = int(os.environ["NUMBER_OF_PROCESSORS"])
        if ncpus > 0:
            return ncpus
    return 1  # Default


def set_nthreads(nthreads):
    """
    set_nthreads(nthreads)

    Set the number of threads to be used during Blosc operation.

    Parameters
    ----------
    nthreads : int
        The number of threads to be used during Blosc operation.

    Returns
    -------
    out : int
        The previous number of used threads.

    Notes
    -----
    The number of threads for Blosc is the maximum number of cores
    detected on your machine (via `detect_number_of_cores`).  In some
    cases Blosc gets better results if you set the number of threads
    to a value slightly below than your number of cores.

    Examples
    --------
    Set the number of threads to 2 and then to 1:

    >>> oldn = blosc.set_nthreads(2)
    >>> blosc.set_nthreads(1)
    2

    """
    if nthreads > _ext.BLOSC_MAX_THREADS:
        raise ValueError("the number of threads cannot be larger than %d" %
                         _ext.BLOSC_MAX_THREADS)

    return _ext.set_nthreads(nthreads)


def free_resources():
    """
    free_resources()

    Free possible memory temporaries and thread resources.

    Returns
    -------
        out : None

    Notes
    -----
    Blosc maintain a pool of threads waiting for work as well as some
    temporary space.  You can use this function to release these
    resources when you are not going to use Blosc for a long while.

    Examples
    --------

    >>> blosc.free_resources()
    >>>
    """
    _ext.free_resources()


def _check_clevel(clevel):
    if not 0 <= clevel <= 9:
        raise ValueError("clevel can only be in the 0-9 range.")


def compress(bytesobj, typesize, clevel=9, shuffle=True):
    """compress(bytesobj, typesize[, clevel=9, shuffle=True]])

    Compress bytesobj, with a given type size.

    Parameters
    ----------
    bytesobj : str / bytes
        The data to be compressed.
    typesize : int
        The data type size.
    clevel : int (optional)
        The compression level from 0 (no compression) to 9
        (maximum compression).  The default is 9.
    shuffle : bool (optional)
        Whether you want to activate the shuffle filter or not.
        The default is True.

    Returns
    -------
    out : str / bytes
        The compressed data in form of a Python str / bytes object.

    Examples
    --------

    >>> import array
    >>> a = array.array('i', range(1000*1000))
    >>> a_bytesobj = a.tostring()
    >>> c_bytesobj = blosc.compress(a_bytesobj, typesize=4)
    >>> len(c_bytesobj) < len(a_bytesobj)
    True

    """

    if not isinstance(bytesobj, bytes):
        raise TypeError(
                "only string (2.x) or bytes (3.x) objects supported as input")

    if len(bytesobj) > _ext.BLOSC_MAX_BUFFERSIZE:
        raise ValueError("bytesobj length cannot be larger than %d bytes" %
                         _ext.BLOSC_MAX_BUFFERSIZE)

    _check_clevel(clevel)

    return _ext.compress(bytesobj, typesize, clevel, shuffle)


def compress_ptr(address, items, typesize, clevel=9, shuffle=True):
    """compress_ptr(address, items, typesize[, clevel=9, shuffle=True]])

    Compress the data at address with given items and typesize.

    Parameters
    ----------
    address : int or long
        the pointer to the data to be compressed
    items : int
        The number of items (of typesize) to be compressed.
    typesize : int
        The data type size.
    clevel : int (optional)
        The compression level from 0 (no compression) to 9
        (maximum compression).  The default is 9.
    shuffle : bool (optional)
        Whether you want to activate the shuffle filter or not.
        The default is True.

    Returns
    -------
    out : str / bytes
        The compressed data in form of a Python str / bytes object.

    Notes
    -----
    This function can be used anywhere that a memory address is available in
    Python. For example the Numpy "__array_interface__['data'][0]" construct,
    or when using the ctypes modules.

    Importantly, the user is responsible for making sure that the memory
    address is valid and that the memory pointed to is contiguous. Passing a
    non-valid address has a high likelihood of crashing the interpreter by
    segfault.

    Examples
    --------

    >>> import numpy
    >>> items = 7
    >>> np_array = numpy.arange(items)
    >>> c = blosc.compress_ptr(np_array.__array_interface__['data'][0], \
        items, np_array.dtype.itemsize)
    >>> d = blosc.decompress(c)
    >>> np_ans = numpy.fromstring(d, dtype=np_array.dtype)
    >>> (np_array == np_ans).all()
    True

    >>> import ctypes
    >>> typesize = 8
    >>> data = [float(i) for i in range(items)]
    >>> Array = ctypes.c_double * items
    >>> a = Array(*data)
    >>> c = blosc.compress_ptr(ctypes.addressof(a), items, typesize)
    >>> d = blosc.decompress(c)
    >>> import struct
    >>> ans = [struct.unpack('d', d[i:i+typesize])[0] \
            for i in range(0,items*typesize,typesize)]
    >>> data == ans
    True
    """

    if not isinstance(address, int_):
        raise TypeError("only int or long objects are supported as address")

    if items < 0:
        raise ValueError("items cannot be negative")

    length = items * typesize
    if length > _ext.BLOSC_MAX_BUFFERSIZE:
        raise ValueError("length cannot be larger than %d bytes" %
                         _ext.BLOSC_MAX_BUFFERSIZE)

    _check_clevel(clevel)

    return _ext.compress_ptr(address, length, typesize, clevel, shuffle)


def decompress(bytesobj):
    """decompress(bytesobj)

    Decompresses a bytesobj compressed object.

    Parameters
    ----------
    bytesobj : str / bytes
        The data to be decompressed.

    Returns
    -------
    out : str / bytes
        The decompressed data in form of a Python str / bytes object.

    Examples
    --------

    >>> import array
    >>> a = array.array('i', range(1000*1000))
    >>> a_bytesobj = a.tostring()
    >>> c_bytesobj = blosc.compress(a_bytesobj, typesize=4)
    >>> a_bytesobj2 = blosc.decompress(c_bytesobj)
    >>> a_bytesobj == a_bytesobj2
    True
    >>> b"" == blosc.decompress(blosc.compress(b"", 1))
    True
    >>> b"1"*7 == blosc.decompress(blosc.compress(b"1"*7, 8))
    True

    """

    if not isinstance(bytesobj, bytes):
        raise TypeError(
                "only string (2.x) or bytes (3.x) objects supported as input")

    return _ext.decompress(bytesobj)

def decompress_ptr(bytesobj, address):
    """decompress_ptr(bytesobj, address)

    Decompresses a bytesobj compressed object into the memory at address.

    Parameters
    ----------
    bytesobj : str / bytes
        The data to be decompressed.
    address : int or long
        the pointer to the data to be compressed

    Returns
    -------
    nbytes : int
        the number of bytes written to the buffer

    Notes
    -----
    This function can be used anywhere that a memory address is available in
    Python. For example the Numpy "__array_interface__['data'][0]" construct,
    or when using the ctypes modules.

    Importantly, the user is responsible for making sure that the memory
    address is valid and that the memory pointed to is contiguous and can be
    written to. Passing a non-valid address has a high likelihood of crashing
    the interpreter by segfault.

    Examples
    --------

    >>> import numpy
    >>> items = 7
    >>> np_array = numpy.arange(items)
    >>> c = blosc.compress_ptr(np_array.__array_interface__['data'][0], \
        items, np_array.dtype.itemsize)
    >>> np_ans = numpy.empty(items, dtype=np_array.dtype)
    >>> nbytes = blosc.decompress_ptr(c, np_ans.__array_interface__['data'][0])
    >>> (np_array == np_ans).all()
    True
    >>> nbytes == items * np_array.dtype.itemsize
    True

    >>> import ctypes
    >>> typesize = 8
    >>> data = [float(i) for i in range(items)]
    >>> Array = ctypes.c_double * items
    >>> in_array = Array(*data)
    >>> c = blosc.compress_ptr(ctypes.addressof(in_array), items, typesize)
    >>> out_array = ctypes.create_string_buffer(items*typesize)
    >>> nbytes = blosc.decompress_ptr(c, ctypes.addressof(out_array))
    >>> import struct
    >>> ans = [struct.unpack('d', out_array[i:i+typesize])[0] \
            for i in range(0,items*typesize,typesize)]
    >>> data == ans
    True
    >>> nbytes == items * typesize
    True

    """

    if not isinstance(bytesobj, bytes):
        raise TypeError(
                "only string (2.x) or bytes (3.x) objects supported as input")

    if not isinstance(address, int_):
        raise TypeError( "only int or long objects are supported as address")

    return _ext.decompress_ptr(bytesobj, address)

def pack_array(array, clevel=9, shuffle=True):
    """pack_array(array[, clevel=9, shuffle=True]])

    Pack (compress) a NumPy array.

    Parameters
    ----------
    array : ndarray
        The NumPy array to be packed.
    clevel : int (optional)
        The compression level from 0 (no compression) to 9
        (maximum compression).  The default is 9.
    shuffle : bool (optional)
        Whether you want to activate the shuffle filter or not.
        The default is True.

    Returns
    -------
    out : str / bytes
        The packed array in form of a Python str / bytes object.

    Examples
    --------

    >>> import numpy
    >>> a = numpy.arange(1e6)
    >>> parray = blosc.pack_array(a)
    >>> len(parray) < a.size*a.itemsize
    True

    """

    if not (hasattr(array, 'dtype') and hasattr(array, 'shape')):
        # This does not quack like an ndarray
        raise TypeError(
            "only NumPy ndarrays objects supported as input")

    itemsize = array.itemsize
    if array.size*itemsize > _ext.BLOSC_MAX_BUFFERSIZE:
        raise ValueError("array size cannot be larger than %d bytes" %
                         _ext.BLOSC_MAX_BUFFERSIZE)

    _check_clevel(clevel)

    # Use the fastest pickle available
    pickled_array = pickle.dumps(array, pickle.HIGHEST_PROTOCOL)
    # ... and compress the pickle
    packed_array = compress(pickled_array, itemsize, clevel, shuffle)

    return packed_array


def unpack_array(packed_array):
    """unpack_array(packed_array)

    Unpack (decompress) a packed NumPy array.

    Parameters
    ----------
    packed_array : str / bytes
        The packed array to be decompressed.

    Returns
    -------
    out : ndarray
        The decompressed data in form of a NumPy array.

    Examples
    --------

    >>> import numpy
    >>> a = numpy.arange(1e6)
    >>> parray = blosc.pack_array(a)
    >>> len(parray) < a.size*a.itemsize
    True
    >>> a2 = blosc.unpack_array(parray)
    >>> numpy.alltrue(a == a2)
    True

    """

    if not isinstance(packed_array, bytes):
        raise TypeError(
                "only string (2.x) or bytes (3.x) objects supported as input")

    # First decompress the pickle
    pickled_array = _ext.decompress(packed_array)
    # ... and unpickle
    array = pickle.loads(pickled_array)

    return array


# For the load tests protocol:
# http://docs.python.org/2/library/unittest.html#load-tests-protocol
def load_tests(loader, tests, pattern):
    import doctest
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == '__main__':
    # test myself
    import doctest
    print("Testing python-blosc version: %s [C-Blosc: %s]" %
          (blosc.__version__, blosc.blosclib_version))
    nfail, ntests = doctest.testmod()
    if nfail == 0:
        print("All %d tests passed successfuly!" % ntests)

    # detect_ncores cannot be safely tested
    #print("ncores-->", detect_number_of_cores())
