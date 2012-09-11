=======================
Releasing python-blosc
=======================

:Author: Francesc Alted
:Contact: faltet@pytables.org
:Date: 2010-11-16

Following are notes useful for releasing python-blosc.

Preliminaries
-------------

- Make sure that ``RELEASE_NOTES.rst`` and ``ANNOUNCE.rst`` are up to
  date with the latest news in the release.

- Check that ``VERSION`` file contains the correct number.

Testing
-------

- After compiling, run:

$ PYTHONPATH=.   (or "set PYTHONPATH=." on Win)
$ export PYTHONPATH=.  (not needed on Win)
$ python blosc/toplevel.py  (add -v for verbose mode)

- Run the test suite in different platforms (at least Linux and
  Windows) and make sure that all tests passes.

Packaging
---------

- Make the tarball with the command:

  $ python setup.py sdist

  Do a quick check that the tarball is sane.

- Make the binary packages for supported Python versions (2.6 and 2.7
  currently).  Check that installer works correctly.

Uploading
---------

- Go to the downloads section of the python-blosc project in github
  and upload the source tarball and the binary packages.

- Upload it also in the PyPi repository.

  * First, register the new version with:
    $ python setup.py register

  * Then upload the files manually using the PyPI web interface.

Announcing
----------

- Update the release notes in the python-blosc site:

  https://github.com/FrancescAlted/python-blosc/wiki/Release-notes

  *WARNING*: Remember that the syntax for github pages is "markdown"
   and not "RestructuredText" (not well supported, apparently).  When
   copying the text from ``RELEASE_NOTES.rst`` to the wiki, double
   chek that it reads as it should (the ``Preview`` button is your
   friend!).

- Send an announcement to the NumPy list and python-announce list.
  Use the ``ANNOUNCE.rst`` file as skeleton (or possibly as the
  definitive version).

Post-release actions
--------------------

- Create a tag ``X.Y`` from ``master``.  Use the next message::

    Created X.Y tag for python-blosc X.Y.

- Edit ``VERSION`` in master to increment the version to the next
  minor one (i.e. X.Y --> X.(Y+1)).

Do the next actions in master or any new branch (if applicable):

- Create new headers for adding new features in ``RELEASE_NOTES.rst``
  and empty the release-specific information in ``ANNOUNCE.rst`` and
  add this place-holder instead:

  #XXX version-specific blurb XXX#


That's all folks!


.. Local Variables:
.. mode: rst
.. coding: utf-8
.. fill-column: 70
.. End:
