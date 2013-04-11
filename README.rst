blosc: a Python package that wraps the Blosc compressor
=======================================================

:Author: Francesc Alted i Abad
:Contact: faltet@pytables.org
:URL: http://blosc.pytables.org

What it is
==========

Blosc (http://blosc.pytables.org) is a high performance compressor
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
running::

    $ PYTHONPATH=.   (or "set PYTHONPATH=." on Win)
    $ export PYTHONPATH=.  (not needed on Win)
    $ python blosc/toplevel.py  (add -v for verbose mode)

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

Merging Blosc sources from upstream
===================================

We use the `subtree merge technique
<http://git-scm.com/book/en/Git-Tools-Subtree-Merging>`_ to maintain the
upstream Blosc sources. In case you need to synchronise, the following recipe
may help to get setup the first time.

1) Add the upstream Blosc sources as an additional remote called
``c-blosc-origin``::

    $ git remote add -f c-blosc-origin git://github.com/FrancescAlted/blosc.git

2) Checkout the ``master`` branch as ``c-blosc``::

    $ git co -b c-blosc c-blosc-origin/master

3) Reset the ``c-blosc`` branch to the desired tag::

    $ git reset --hard vX.Y.Z

4) Checkout the branch you want to subtree merge to::

    $ git checkout master

5) Actually perform the subtree merge::

    $ git merge --squash -s subtree --no-commit c-blosc

6) Finalize the subtree merge with a commit::

    $ git commit -m "subtree merge blosc vX.Y.Z"

If you alread have the ``c-blosc-origin`` remote set up and the ``c-blosc``
branch created, you can just update it::

    $ git checkout c-blosc
    $ git pull

And then proceed with step 3 above.

Mailing list
============

Discussion about this module is welcome in the Blosc list:

blosc@googlegroups.com
http://groups.google.es/group/blosc
