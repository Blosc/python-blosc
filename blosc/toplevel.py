########################################################################
#
#       License: MIT
#       Created: September 22, 2010
#       Author:  Francesc Alted - faltet@pytables.org
#
########################################################################

import os, cPickle

import blosc
from blosc import blosc_extension as _ext


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
        else: # OSX:
            return int(os.popen2("sysctl -n hw.ncpu")[1].read())
    # Windows:
    if "NUMBER_OF_PROCESSORS" in os.environ:
        ncpus = int(os.environ["NUMBER_OF_PROCESSORS"]);
        if ncpus > 0:
            return ncpus
    return 1 # Default


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

    >>> oldn = set_nthreads(2)
    >>> set_nthreads(1)
    2

    """
    if nthreads > _ext.BLOSC_MAX_THREADS:
        raise ValueError("the number of threads cannot be larger than %d" % \
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

    >>> free_resources()
    >>>
    """
    _ext.free_resources()


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
    >>> c_bytesobj = compress(a_bytesobj, typesize=4)
    >>> len(c_bytesobj) < len(a_bytesobj)
    True

    """

    if type(bytesobj) is not bytes:
        raise ValueError(
            "only string (2.x) or bytes (3.x) objects supported as input")

    if len(bytesobj) > _ext.BLOSC_MAX_BUFFERSIZE:
        raise ValueError("bytesobj length cannot be larger than %d bytes" % \
                         _ext.BLOSC_MAX_BUFFERSIZE)

    if clevel < 0 or clevel > 9:
        raise ValueError("clevel can only be in the 0-9 range.")

    return _ext.compress(bytesobj, typesize, clevel, shuffle)


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
    >>> c_bytesobj = compress(a_bytesobj, typesize=4)
    >>> a_bytesobj2 = decompress(c_bytesobj)
    >>> a_bytesobj == a_bytesobj2
    True
    >>> "" == blosc.decompress(blosc.compress("", 1))
    True
    >>> "1"*7 == blosc.decompress(blosc.compress("1"*7, 8))
    True

    """

    if type(bytesobj) is not bytes:
        raise ValueError(
            "only string (2.x) or bytes (3.x) objects supported as input")

    return _ext.decompress(bytesobj)


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
    >>> parray = pack_array(a)
    >>> len(parray) < a.size*a.itemsize
    True

    """

    if not (hasattr(array, 'dtype') and hasattr(array, 'shape')):
        # This does not quack like an ndarray
        raise ValueError(
            "only NumPy ndarrays objects supported as input")

    itemsize = array.itemsize
    if array.size*itemsize > _ext.BLOSC_MAX_BUFFERSIZE:
        raise ValueError("array size cannot be larger than %d bytes" % \
                         _ext.BLOSC_MAX_BUFFERSIZE)

    # Use the fastest pickle available
    pickled_array = cPickle.dumps(array, cPickle.HIGHEST_PROTOCOL)
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
    >>> parray = pack_array(a)
    >>> len(parray) < a.size*a.itemsize
    True
    >>> a2 = unpack_array(parray)
    >>> numpy.alltrue(a == a2)
    True

    """

    if type(packed_array) is not bytes:
        raise ValueError(
            "only string (2.x) or bytes (3.x) objects supported as input")

    # First decompress the pickle
    pickled_array = _ext.decompress(packed_array)
    # ... and unpickle
    array = cPickle.loads(pickled_array)

    return array



if __name__ == '__main__':
    # test myself
    import doctest
    print("Testing python-blosc version: %s [C-Blosc: %s]" % \
          (blosc.__version__, blosc.blosclib_version))
    nfail, ntests = doctest.testmod()
    if nfail == 0:
        print("All %d tests passed successfuly!" % ntests)

    # detect_ncores cannot be safely tested
    #print("ncores-->", detect_number_of_cores())
