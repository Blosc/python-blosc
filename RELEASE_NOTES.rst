======================================
 Release notes for python-blosc 1.2.8
======================================

:Author: Francesc Alted
:Author: Valentin Hänel
:Contact: faltet@gmail.com
:Contact: valentin@haenel.co
:URL: http://python-blosc.blosc.org
:URL: https://github.com/Blosc/python-blosc


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
