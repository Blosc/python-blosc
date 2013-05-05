blosc: a Python package that wraps the Blosc compressor
=======================================================

:Author: Francesc Alted
:Authonr: Valentin Hänel
:Contact: faltet@blosc.org
:URL: http://blosc.org

What it is
==========

Blosc (http://blosc.org) is a high performance compressor
optimized for binary data.  It has been designed to transmit data to
the processor cache faster than the traditional, non-compressed,
direct memory fetch approach via a memcpy() OS call.

Blosc works well for compressing numerical arrays that contains data
with relatively low entropy, like sparse data, time series, grids with
regular-spaced values, etc.

This is a Python package that wraps it.

Building
========

Assuming that you have a C compiler installed, do::

    $ python setup.py build_ext --inplace

This package supports Python 2.6, 2.7 and 3.1 or higher versions.

Testing
=======

After compiling, you can quickly check that the package is sane by
running the doctests in ``blosc/test.py``::

    $ PYTHONPATH=.   (or "set PYTHONPATH=." on Win)
    $ export PYTHONPATH=.  (not needed on Win)
    $ python blosc/test.py  (add -v for verbose mode)

Or alternatively, you can use the third-party ``nosetests`` script to run both
the doctests and the test suite::

    $ nosetests --with-doctest (add -v for verbose mode)

Once installed, you can re-run the tests at any time with::

    $ python -c "import blosc; blosc.test()"

Installing
==========

Install it as a typical Python package::

    $ python setup.py install

Documentation
=============

Please refer to docstrings.  Start by the main package::

    >>> import blosc
    >>> help(blosc)

and ask for more docstrings in the referenced functions.

Also, some examples are available on python-blosc wiki page:

http://github.com/FrancescAlted/python-blosc/wiki

A Sphinx based documentation is in the works.  Stay tuned.


Merging Blosc sources from upstream
===================================

We use the `subtree merge technique
<http://git-scm.com/book/en/Git-Tools-Subtree-Merging>`_ to maintain the
upstream Blosc sources. However, we do not use the technique exactly as listed
in the Pro-Git book.

The reason is quite technical: adding the Blosc Git repository as a remote will
also include the Blosc tags in your repository.  Since the Blosc and
python-blosc repositories share the same tagging scheme, i.e. ``v.X.Y.Z``, we
may have potentially conflicting tags. For example, one might want to tag
python-blosc ``v1.2.1``, however, since Blosc already has a tag of this name,
Git will deny you creating this. One could use the ``--no-tags`` option for
``git fetch`` when fetching Blosc -- but alas, this would defeat the purpose.
The tagged versions of Blosc are exactly the ones we are interested in for the
subtree merge! So, as a compromise there is a shell script
``subtree-merge-blosc.sh``.  This accepts a single tag as argument and does a
plain ``git fetch``. This has the effect of fetching the commit that the
requested tag points to, but not actually fetching that tag or any of the other
tags.

It is not perfect and can probably be improved upon, but it does have some
comments in the source, checks for some common errors and tries to abort as
early as possible in case things go wrong. A sample invocation is shown below:

.. code-block:: console

    $ ./subtree-merge-blosc.sh v1.2.1
    found remote tag: '4eda92c4dcba18849d482f5014b374d8b4b4cdfc	refs/tags/v1.2.1'
    warning: no common commits
    remote: Counting objects: 1558, done.
    remote: Compressing objects: 100% (606/606), done.
    remote: Total 1558 (delta 958), reused 1528 (delta 932)
    Receiving objects: 100% (1558/1558), 468.67 KiB | 304 KiB/s, done.
    Resolving deltas: 100% (958/958), done.
    From git://github.com/FrancescAlted/blosc
     + tag               v1.2.1     -> FETCH_HEAD
    Squash commit -- not updating HEAD
    Automatic merge went well; stopped before committing as requested
    [subtree-merge-blosc.sh b7a7378] subtree merge blosc v1.2.1
     16 files changed, 60 insertions(+), 43 deletions(-)


Mailing list
============

Discussion about this module is welcome in the Blosc list:

blosc@googlegroups.com
http://groups.google.es/group/blosc

----

  **Enjoy data!**
