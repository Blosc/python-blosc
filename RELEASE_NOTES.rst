================================
 Release notes for python-blosc
================================

:Author: The Blosc development team
:Contact: blosc@blosc.org
:URL: http://python-blosc.blosc.org
:URL: https://github.com/Blosc/python-blosc


Changes from 1.9.2 to 1.10.0
===========================

- Updated vendored C-Blosc to 1.21.0.

- Wheels for Intel (32 and 64 bits) and all major OS (Win, Linux, Mac) are here.
  The wheels have support for runtime detection for AVX2, so it will be
  automatically leveraged in case the local host has AVX2.  No need anymore to
  worry about using different binaries for CPUs not having AVX2 hardware.

  Also, we are distributing binaries for C-Blosc libraries (dynamic and static)
  and headers.  This way, people trying to use the C-Blosc library can use the
  python-blosc wheels to install the necessary development files.  For details,
  see: https://github.com/Blosc/c-blosc/blob/master/COMPILING_WITH_WHEELS.rst

  We gratefully acknowledge Jeff Hammerbacher for supporting the addition of
  wheels for Blosc.

- Officially drop support for Python < 3.7.  Although we did not any explicit
  action that is incompatible with older Python versions, we only provide
  wheels for Python >= 3.7 (til 3.9).


Changes from 1.9.1 to 1.9.2
===========================

- Internal C-Blosc updated to 1.20.1.  This fixes
  https://github.com/Blosc/python-blosc/issues/229, and also brings
  many new updates in internal codecs, providing interesting bumps
  in performance in some cases.

- Due to recent addition of more cores in new CPUs, the number of
  internal threads to be used by default has been increased from 4 to 8.

- Allow zero-copy decompression by allowing bytes-like input.  See PR:
  https://github.com/Blosc/python-blosc/pull/230.  Thanks to Lehman
  Garrison.

- Fix DeprecationWarning due to invalid escape sequence and use
  array.tobytes for Python 3.9.


Changes from 1.9.0 to 1.9.1
===========================

- Disable the attempt to include support for SSE2 and AVX2 on non-Intel
  platforms, allowing the build on such platforms (see #244).  Thanks
  to Lehman Garrison.


Changes from 1.8.3 to 1.9.0
===========================

- Dropped support for Python 2.7 and 3.5.

- Fixed the copy of the leftovers of a chunk when its size is not a
  multiple of the typesize.  Although this is a very unusual situation,
  it can certainly happen (e.g.
  https://github.com/Blosc/python-blosc/issues/220).


Changes from 1.8.2 to 1.8.3
===========================

- Add a missing pyproject.toml to MANIFEST.in.  This allows to install the necessary
  skbuild module.  Thanks to Manuel Castro.

Changes from 1.8.1 to 1.8.2
===========================

- Use cmake internally to build the Python extension via the scikit-build library.
  This seems enough to cope with the conflicting types in using XGETBV when using
  a recent GCC (>= 9.1) compiler.  Fixes #203 and #209.
  Thanks to Matt McCormick.

- Include C-Blosc v1.17.1.

Changes from 1.8.0 to 1.8.1
===========================

- Fix a bug that prevented the source distribution from PyPi to be compiled.
  Specifcally, `*.inc` were not included via the manifest.

Changes from 1.7.0 to 1.8.0
===========================

- Include C-Blosc v1.16.2
- Fix cpuinfo.py usage on Windows. Thanks to Robert McLeod
- Implement Python access to the C function `cbuffer_validate` which
  was added to c-blosc in version 1.16.0
- Check if compiler supports CPU capabilities. Thanks to Nicholas Devenish
- Many minor improvements and fixes

Changes from 1.6.2 to 1.7.0
===========================

- Include C-Blosc v1.15.1
- Remove Support for Python 2.6 and 3.3
- Fix vendored cpuinfo.py
- Rework Windows CI via Appveyor
- Various minor bugfixes

Changes from 1.6.1 to 1.6.2
===========================

- Fixed `numpy` import in `toplevel.py`, this makes python-blosc usable without
  numpy once again.

Changes from 1.5.1 to 1.6.1
===========================

- Updated C-Blosc to 1.14.3

- Adding support for aarch64

- `unpack_array` can now accepts keyword arguments. This allows decompressing
  pickled arrays that were compressed with Python 2.x using Python 3.x. Thanks
  to Simba Nyatsanga and Juan Maree.

- Implemented `get_blocksize()`, thanks to Alberto Sabater

- Seperate compilation of codecs, thanks to Robert McLeod

- Removal of Numpy dependencies, thanks to Robert McLeod

- Allow codecs to be included by using environment variables, thanks to
  Robert McLeod

- Don't compile snappy by default, thanks to Robert McLeod

- Update cpuinfo.py to use dmesg.boot, thanks to Prakhar Goel

- Allow SSE2 and AVX2 detection to be disabled via environment variables,
  thanks to Lorenzo Bolla

- Varios minor fixes


Changes from 1.5.0 to 1.5.1
===========================

- License updated from MIT to BSD.

- Updated to C-Blosc 1.11.3.


Changes from 1.4.4 to 1.5.0
===========================

- Added a new `blosc.set_releasegil()` function that allows to
  release/acquire the GIL at will.  See PR #116.
  Thanks to Robert McLeod.

- Updated to C-Blosc 1.11.2.

- Added tests that detect possible memory leaks.
  Thanks to Robert McLeod.


Changes from 1.4.3 to 1.4.4
===========================

- Updated to C-Blosc 1.11.1.  Fixes #115.


Changes from 1.4.1 to 1.4.3
===========================

- Internal C-Blosc sources updated to 1.11.0. Among other things, this
  updates the internal Zstd codec to version 1.0.0 (i.e. it is
  officially apt for production usage!).


Changes from 1.4.0 to 1.4.1
===========================

- Internal C-Blosc sources updated to 1.10.1.  This fixes an outstanding issue
  with the clang compiler.  For details, see:
  https://github.com/Blosc/bloscpack/issues/50.


Changes from 1.3.3 to 1.4.0
===========================

- Internal C-Blosc sources updated to 1.10.0.

- Benchmarks updated for a Skylake processor (Xeon E3-1245 v5 @
  3.50GHz).


Changes from 1.3.2 to 1.3.3
===========================

- Internal C-Blosc sources updated to 1.9.3.

- C-Blosc do not segfaults anymore, so -O1 flag on Linux is not the
  default anymore.

- SSE2 and AVX2 are now auto-discovered so the internal C-Blosc will be
  compiled with maximum optimization on processors supporting them.


Changes from 1.3.1 to 1.3.2
===========================

- Fixed the version of the include C-Blosc library (should be 1.8.1 not
  1.8.2.dev).


Changes from 1.3.0 to 1.3.1
===========================

- Use the -O1 flag for compiling the included C-Blosc sources on Linux.
  This represents slower performance, but fixes the nasty issue #110.
  Also, it prints a warning for using an external C-Blosc library.

- Internal C-Blosc version bumped to 1.8.1 for better compatibility
  with gcc 5.3.1 in forthcoming Ubuntu Xenial.

- Added a protection to avoid using BITSHUFLE with C-Blosc < 1.8.0.

- Restored old symbols for backward compatibility with pre 1.3.0:
    BLOSC_VERSION_STRING
    BLOSC_VERSION_DATE
    BLOSC_MAX_BUFFERSIZE
    BLOSC_MAX_THREADS
    BLOSC_MAX_TYPESIZE
  However, these are considered deprecated and should be replaced by
  libraries using python-blosc by the ones without the `BLOSC_` prefix.


Changes from 1.2.8 to 1.3.0
===========================

- Internal C-Blosc version bumped to 1.8.0.  As consequence, support for
  BITSHUFFLE is here.  For activating it, just pass `blosc.BITSHUFFLE`
  to the `shuffle` parameter of compression functions.

- Added a new `as_bytearray=False` parameter to the `decompress()` function
  so that a mutable bytearray will be returned instead of a bytes one
  (inmutable).  PR #107.  Thanks to Joe Jevnik.

- The '__all__' variable has been removed from the module.  I consider
  this good practice to avoid things like "from blosc import *".

- For consistency, the next symbols have been renamed:
    BLOSC_VERSION_STRING -> VERSION_STRING,
    BLOSC_VERSION_DATE -> VERSION_DATE,
    BLOSC_MAX_BUFFERSIZE -> MAX_BUFFERSIZE,
    BLOSC_MAX_THREADS -> MAX_THREADS,
    BLOSC_MAX_TYPESIZE -> MAX_TYPESIZE,

- The `typesize` parameter is set by default to 8 in compression
  functions.  This usually behaves well for 4-bytes typesizes too.
  Nevertheless, it is advised to use the actual typesize.

- The maximum number of threads to use by default is set to 4 (less if
  less cores are detected).  Feel free to use more or less threads
  depending on the resources you want to use for compression.


Changes from 1.2.7 to 1.2.8
===========================

- Updated to c-blosc v1.7.0.  However, the new bitshuffle filter has not
  been made public because recent reports indicate that it seems too
  green for production.

- Support bytes-like objects that support the buffer interface as input to
  ``compress`` and ``decompress``. On Python 2.x this includes unicode, on
  Python 3.x it doesn't.  (#80 #94 @esc)

- Fix a memory leak in ``decompress``.  Added tests to catch memory
  leaks. (#102 #103 #104 @sdvillal)

- Various miscellaneous fixes and improvements.


Changes from 1.2.5 to 1.2.7
===========================

- Updated to c-blosc v1.6.1.  Although that this supports AVX2, it is
  not enabled in python-blosc because we still need a way to devise how
  to detect AVX2 in the underlying platform.


Changes from 1.2.4 to 1.2.5
===========================

- Updated to c-blosc v1.5.4.

- Added wrapper for the expert function ``set_blocksize``. (#72 @esc)

- Fix setup.py to allow compilation on posix architectures without SSE2. (#70
  @andreas-schwab)

- Don't release the GIL on compression/decompression (#77 @esc)

- Various miscellaneous fixes.


Changes from 1.2.3 to 1.2.4
===========================

- Updated to c-blosc 1.4.0.  This added support for non-Intel
  architectures, most specially those not supporting unaligned access.


Changes from 1.2.2 to 1.2.3
===========================

- Updated to c-blosc 1.3.5.  This removed a 'pointer from integer
  without a cast' compiler warning due to a bad macro definition.


Changes from 1.2.1 to 1.2.2
===========================

- Updated to c-blosc 1.3.4.  This fixed a false buffer overrun
  condition.  This bug made c-blosc (and hence python-blosc) to fail,
  even if the failure was not real.


Changes from 1.2.0 to 1.2.1
===========================

- Updated to c-blosc 1.3.3.

- Added a new `cname2clib` map for programatically determine the library
  associated to a compressor.

- New `get_clib(cbuffer)` that tells which compression library format
  has been used to created the compressed `cbuffer`.


Changes from 1.1.0 to 1.2.0
===========================

This release adds support for the multiple compressors added in Blosc
1.3 series.

- Added new `cname` parameter in compression functions like
  `compress()`, `compress_ptr()` and `pack_array()`.

- Added a new utility function named `compressor_list()` that returns
  the list of compressors supported in the Blosc build.

- Added 'bench/compress_ptr.py' for comparing times of the different
  compressors in Blosc and NumPy.


Changes from 1.0.6 to 1.1.0
===========================

- Added new `compress_ptr` and `decompress_ptr` functions that allows to
  compress and decompress from/to a data pointer.  These are low level
  calls and user must make sure that the pointer data area is safe.

- Since Blosc (the C library) already supports to be installed as an
  standalone library (via cmake), it is also possible to link
  python-blosc against a system Blosc library.

- The Python calls to Blosc are now thread-safe (another consequence of
  recent Blosc library supporting this at C level).

- Many checks on types and ranges of values have been added.  Most of
  the calls will now complain when passed the wrong values.

- Docstrings are much improved. Also, Sphinx-based docs are available
  now.

Many thanks to Valentin Hänel for his excellent work on this release.


Changes from 1.0.5 to 1.0.6
===========================

- Fix compile error with msvc compilers.  Thanks to Christoph Gohlke.


Changes from 1.0.4 to 1.0.5
===========================

- Upgraded to latest Blosc 1.1.4.

- Better handling of condition errors, and improved memory releasing in
  case of errors (thanks to Valentin Haenel and Han Genuit).

- Better handling of types (should compile without warning now, at least
  with GCC).


Changes from 1.0.3 to 1.0.4
===========================

- Optimized the amount of data copied during compression (using
  _PyBytes_Resize() now instead of old PyBytes_FromStringAndSize()).

  This leads to improvements in compression speed ranging from 1.2x for
  highly compressible chunks up to 7x for mostly uncompressible data.
  Thanks to Valentin Haenel for this nice contribution.


Changes from 1.0.2 to 1.0.3
===========================

- Updated to Blosc 1.1.3.  Much improved compression ratio when using
  large blocks (> 64 KB) and high compression levels (> 6) under some
  circumstances (special data distribution).

- The number of cores on Windows are detected now correctly.  Thanks to
  Han Genuit for noticing that and suggesting a patch.


Changes from 1.0.1 to 1.0.2
===========================

- Updated to Blosc 1.1.2.  Fixes some bugs when dealing with very small
  buffers (typically smaller than specified typesizes).  Closes #1.


1.0.1
=====

- First public release.





.. Local Variables:
.. mode: rst
.. coding: utf-8
.. fill-column: 72
.. End:
