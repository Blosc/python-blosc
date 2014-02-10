########################################################################
#
#       License: MIT
#       Created: September 22, 2010
#       Author:  Francesc Alted - faltet@gmail.com
#
########################################################################


from blosc.version import __version__

from blosc.toplevel import (
    compress,
    compress_ptr,
    decompress,
    decompress_ptr,
    pack_array,
    unpack_array,
    detect_number_of_cores,
    free_resources,
    set_nthreads,
    compressor_list,
    code_to_name,
    name_to_code,
    clib_info,
    get_clib,
    print_versions,
    )

# Dictionaries for the maps between compressor names and libs
cnames = compressor_list()
# Map for compression names and libs
cname2clib = dict((name, clib_info(name)[0]) for name in cnames)
# Map for compression libraries and versions
clib_versions = dict(clib_info(name) for name in cnames)

# Blosc symbols that we want to export
from blosc.blosc_extension import (
    BLOSC_VERSION_STRING,
    BLOSC_VERSION_DATE,
    BLOSC_MAX_BUFFERSIZE,
    BLOSC_MAX_THREADS,
    BLOSC_MAX_TYPESIZE,
    init,
    destroy,
    )


# Initialize Blosc
init()
ncores = detect_number_of_cores()
set_nthreads(ncores)
blosclib_version = "%s (%s)" % (BLOSC_VERSION_STRING, BLOSC_VERSION_DATE)
import atexit
atexit.register(destroy)

# Tests
from blosc.test import run as test

__all__ = ['compress', 'compress_ptr', 'decompress', 'decompress_ptr',
           'pack_array', 'unpack_array',
           'detect_number_of_cores', 'free_resources', 'set_nthreads',
           'compressor_list', 'clib_info', 'get_clib',
           'print_versions', 'test']
