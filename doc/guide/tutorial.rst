..
    :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
    :license: See LICENSE.txt.

.. _tutorial:

Tutorial
========

.. module:: clique

This tutorial gives a good introduction to using Clique.

First make sure that you have Clique :ref:`installed <installation>`.

Clique revolves around creating collections of items that all have a commonly
changing numerical component. Clique itself does not care what the numerical
component represents. It could be a frame index for a sequence of files or a
version number in a list of versioned files.

The easiest way to create these collections is to :py:func:`~clique.assemble`
them from arbitrary items.

First, import clique::

    >>> import clique

Then define the items to assemble (could be the result of :py:func:`os.listdir`
for example)::

    >>> items = ['file.0001.jpg', '_cache.txt', 'file.0002.jpg',
    ...          'foo.1.txt', 'file.0002.dpx', 'file.0001.dpx',
    ...          'file.0010.dpx', 'scene_v1.ma', 'scene_v2.ma']

Finally, assemble them into collections::

    >>> collections = clique.assemble(items)
    >>> for collection in collections:
    ...     print repr(collection)
    <Collection "scene_v%d.ma [1-2]">
    <Collection "file.%04d.dpx [1-2, 10]">
    <Collection "file.%04d.jpg [1-2]">

Notice how the items ``_cache.txt`` and ``foo.1.txt`` didn't form any
collections. This is because ``_cache.txt`` has no numerical component and
was ignored, whilst ``foo.1.txt`` resulted in a collection with only one
item and was filtered out of the result.

The minimum items filter can be altered at assembly time::

    >>> collections = clique.assemble(items, minimum_items=1)
    >>> for collection in collections:
    ...     print repr(collection)
    <Collection "scene_v%d.ma [1-2]">
    <Collection "foo.%d.txt [1]">
    <Collection "file.%04d.dpx [1-2, 10]">
    <Collection "file.%04d.jpg [1-2]">

.. seealso::

    There is a full guide to :ref:`assembly` available.

Each collection holds various properties to describe the items it
contains::

    >>> collection = collections[0]
    >>> print collection.head
    scene_v
    >>> print collection.tail
    .ma
    >>> print collection.padding
    0
    >>> print collection.indexes
    [1, 2]

.. seealso::

    There is a full guide to :ref:`collection` available.


