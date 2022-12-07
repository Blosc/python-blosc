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

* Go to Blosc/blogsite repo and click on the `Re-run all jobs` button to regenerate the
  documentation and check that it has been correctly updated in https://www.blosc.org.

Tagging
-------

* Create a signed tag ``X.Y.Z`` from ``master``.  Use the next message::

    $ git tag -s vX.Y.Z -m "Tagging version X.Y.Z"

* Push the tag to the github repo::

    $ git push
    $ git push --tags

* Check that wheels are created and uploaded to PyPI.

Releasing on GitHub
-------------------

* Go to: https://github.com/Blosc/python-blosc/releases.

* Draft a new release. Make sure you use an existing tag.

Announcing
----------

* Send an announcement to the blosc, pydata list and python-announce
  lists.  Use the ``ANNOUNCE.rst`` file as skeleton (or possibly as
  the definitive version).

* Announce via Twitter and any other appropriate service such as Mastodon.


Post-release actions
--------------------

* Make sure you are in the master branch.

* Edit ``VERSION`` in master to increment the version to the next
  minor one (i.e. X.Y.Z --> X.Y.(Z+1).dev0).

* Also, update the ``version`` and ``release`` variables in doc/conf.py.

* Create new headers for adding new features in ``RELEASE_NOTES.rst``
  add this place-holder::

  #XXX version-specific blurb XXX#

* Commit your changes with::

  $ git commit -a -m"Post X.Y.Z release actions done"
  $ git push


That's all folks!


.. Local Variables:
.. mode: rst
.. coding: utf-8
.. fill-column: 70
.. End:
