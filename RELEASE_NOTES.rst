======================================
 Release notes for python-blosc 1.0.7
======================================

:Author: Francesc Alted i Abad
:Contact: faltet@pytables.org
:URL: http://blosc.pytables.org


Changes from 1.0.6 to 1.0.7
===========================

  #XXX version-specific blurb XXX#


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
