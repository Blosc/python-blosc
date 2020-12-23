=======================
Releasing python-blosc
=======================

:Author: The Blosc Development Team
:Contact: blosc@blosc.org
:Date: 2020-12-22


Preliminaries
-------------

* Make sure that the current master branch is passing the tests on Github Actions.

* Make sure that ``RELEASE_NOTES.rst``
  and ``ANNOUNCE.rst`` are up to date with the latest news in the release.

* Check that ``VERSION`` and ``doc/conf.py`` files contains the correct number.

* Check any copyright listings and update them if necessary. You can use
  ``git grep -i copyright`` to figure out where they might be.

* Commit the changes::

  $ git commit -a -m"Getting ready for release X.Y.Z"

Updating the online documentation site
--------------------------------------

* Go to the doc directory::

  $ cd doc

* Make the html version of the docs::

  $ rm -rf _build/html
  $ PYTHONPATH=../ make html

* Make a backup and upload the files in the doc site (xodo) (this step is
  currently pretty broken and won't work as listed, just make sure the docs are
  in the right place with the correct permissions.)::

  $ export UPSTREAM="/home/blosc/srv/www/python-blosc.blosc.org"
  $ ssh blosc@xodo.blosc.org "mv $UPSTREAM/docs/html $UPSTREAM/docs/html.bck"
  $ scp -r _build/html blosc@xodo.blosc.org:$UPSTREAM/docs

* Check that the new manual is accessible in http://python-blosc.blosc.org

* If everything goes well, remove the old docs backup::

  $ ssh blosc@xodo.blosc.org "rm -r $UPSTREAM/docs/html.bck"

* Go up to the root directory for further proceeding with packging::

  $ cd ..


Tagging
-------

* Create a signed tag ``X.Y.Z`` from ``master``.  Use the next message::

    $ git tag -s vX.Y.Z -m "Tagging version X.Y.Z"

* Push the tag to the github repo::

    $ git push
    $ git push --tags


* Check that wheels are created and uploaded to PyPI.

Announcing
----------

* Send an announcement to the blosc, pydata list and python-announce
  lists.  Use the ``ANNOUNCE.rst`` file as skeleton (or possibly as
  the definitive version).

* Announce via Twitter and any other appropriate service such as Mastodon.


Post-release actions
--------------------

* Edit ``VERSION`` in master to increment the version to the next
  minor one (i.e. X.Y.Z --> X.Y.(Z+1).dev0).

* Also, update the ``version`` and ``release`` variables in doc/conf.py.

* Create new headers for adding new features in ``RELEASE_NOTES.rst``
  add this place-holder::

  #XXX version-specific blurb XXX#

* Commit your changes with::

  $ git commit -a -m"Post X.Y.Z release actions done"


That's all folks!


.. Local Variables:
.. mode: rst
.. coding: utf-8
.. fill-column: 70
.. End:
