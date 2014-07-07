=======================
Releasing python-blosc
=======================

:Author: Francesc Alted
:Contact: faltet@gmail.com
:Date: 2012-09-16


Preliminaries
-------------

* Make sure that ``RELEASE_NOTES.rst`` and ``ANNOUNCE.rst`` are up to
  date with the latest news in the release.

* Check that ``VERSION`` file contains the correct number.

Testing
-------

* After compiling, run:

$ PYTHONPATH=.   (or "set PYTHONPATH=." on Win)
$ export PYTHONPATH=.  (not needed on Win)
$ python -c "import blosc; blosc.test()"

* Run the test suite in different platforms (at least Linux and
  Windows) and make sure that all tests passes.


Updating documentation site (gh-pages)
--------------------------------------

* Go to the doc directory in the *master* branch::

  $ git checkout master
  $ cd doc

* Make sure that the `version`/`release` variables are updated in
  'conf.py'.

* Make the html version of the docs::

  $ rm -rf _build/html
  $ make html

* Checkout the gh-pages and copy the new version of the manual::

  $ cd ..
  $ git checkout gh-pages
  $ cp -r doc/_build/html/ python-blosc-manual
  $ git diff # just check that the version is actually the new one
  $ git commit -a -m"Uploading new version of the manual"
  $ git push

* Done.  Go back to master branch before proceeding further::

  $ git checkout master

Packaging
---------

* Make the tarball with the command:

  $ python setup.py sdist

  Do a quick check that the tarball is sane.


Uploading
---------

* Register and upload it also in the PyPi repository::

    $ python setup.py sdist upload
    $ python setup.py register

Tagging
-------

* Create a tag ``X.Y.Z`` from ``master``.  Use the next message::

    $ git tag -a vX.Y.Z -m "Tagging version X.Y.Z"

* Push the tag to the github repo::

    $ git push --tags

Announcing
----------

* Update the release notes in the python-blosc site:

  https://github.com/Blosc/python-blosc/wiki/Release-notes

* Send an announcement to the blosc, numpy list and python-announce
  lists.  Use the ``ANNOUNCE.rst`` file as skeleton (or possibly as the
  definitive version).

Post-release actions
--------------------

* Edit ``VERSION`` in master to increment the version to the next
  minor one (i.e. X.Y.Z --> X.Y.(Z+1).dev).

* Also, update the `version` and `release` variables in doc/conf.py.

* Create new headers for adding new features in ``RELEASE_NOTES.rst``
  and empty the release-specific information in ``ANNOUNCE.rst`` and
  add this place-holder instead:

  #XXX version-specific blurb XXX#


That's all folks!


.. Local Variables:
.. mode: rst
.. coding: utf-8
.. fill-column: 70
.. End:
