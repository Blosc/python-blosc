======================================
 Release notes for python-blosc 1.0.4
======================================

:Author: Francesc Alted i Abad
:Contact: faltet@pytables.org
:URL: http://blosc.pytables.org


Changes from 1.0.3 to 1.0.4
===========================

- (None yet)


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
