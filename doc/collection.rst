..
    :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
    :license: See LICENSE.txt.

.. _collection:

***********
Collections
***********

.. module:: clique.collection

A collection holds items that all have a single common numerical component,
whose value differs between each item.

Each collection comprises three main attributes:

    * :term:`head` - The common leading part of each item.
    * :term:`tail` - The common trailing part of each item.
    * :term:`padding` - The width of the index (to be padded to with zeros).

Given items such as:

    * file.0001.jpg
    * file.0002.jpg

The :term:`head` would be ``file.``, the :term:`tail` ``.jpg`` and the
:term:`padding` ``4``.

.. note::

    If the numerical component is unpadded then the :term:`padding` would be 0
    and a variable index width supported.

A collection can be manually created using the :py:class:`~Collection` class::

    >>> import clique
    >>> collection = clique.Collection(head='file.', tail='.jpg', padding=4)

Adding & Removing Items
=======================

Items can then be :py:meth:`added <Collection.add>` to the
collection::

    >>> collection.add('file.0001.jpg')

If an item does not match the collection's expression a
:py:class:`~clique.error.CollectionError` is raised:

    >>> collection.add('file.0001.dpx')
    CollectionError: Item does not match collection expression.

Whether an item matches the collection expression can be tested ahead of time
if desired using :py:meth:`~Collection.match`::

    >>> print collection.match('file.0002.jpg')
    <_sre.SRE_Match object at 0x0000000003710D78>
    >>> print collection.match('file.0002.dpx')
    None

To remove an item::

    >>> collection.remove('file.0001.jpg')

If the item is not present, a :py:class:`~clique.error.CollectionError` is
raised::

    >>> collection.remove('file.0001.jpg')
    CollectionError: Item not present in collection.

Accessing Items
===============

To access items in the collection, iterate over it::

    >>> collection.add('file.0001.jpg')
    >>> collection.add('file.0002.jpg')
    >>> for item in collection:
    ...     print item
    file.0001.jpg
    file.0002.jpg

.. note::

    A collection may be sparse and so is not directly indexable. If you need
    to access an item by index, convert the collection to a list::

        >>> print list(collection)[-1]
        file.0002.jpg

Manipulating Indexes
====================

Internally, Clique does not store the items directly, but rather just the
properties to recreate the items (:term:`head`, :term:`tail`, :term:`padding`).
In addition it holds a sorted set of indexes present in the collection.

This set of indexes can be manipulated directly to perform the equivalent of
adding and removing items (perhaps in bulk).

    >>> print collection.indexes
    [1, 2]
    >>> collection.indexes.update([2, 3, 4])
    >>> for item in collection:
    ...     print item
    file.0001.jpg
    file.0002.jpg
    file.0003.jpg
    file.0004.jpg

.. note::

    It is not possible to assign a new index set directly::

        >>> collection.indexes = set([1, 2, 3])
        AttributeError: Cannot set attribute defined as unsettable.

    Instead, first clear and update the set as required::

        >>> collection.indexes.clear()
        >>> collection.indexes.update(set([1, 2, 3])

Formatting
==========

It is useful to express a collection as a string that represents the collection
expression and ranges in a standard way. Clique supports basic formatting of a
collection through its :py:meth:`~Collection.format` method::

    >>> collection = clique.Collection('file.', '.jpg', 4, indexes=set([1, 2]))
    >>> print collection.format()
    file.%04d.jpg [1-2]

The :py:meth:`~Collection.format` method can be passed an
alternative pattern if required::

    >>> print collection.format('{head}[index]{tail}')
    file.[index].jpg

The passed pattern should match the formatting rules of Python's standard
string formatter and will have the following keyword variables available to it:

    * *:term:`head`* - Common leading part of the collection.
    * *:term:`tail`* - Common trailing part of the collection.
    * *:term:`padding`* - Padding value in ``%0d`` format.
    * *range* - Total range in the form ``start-end``
    * *ranges* - Comma separated ranges of indexes.
    * *holes* - Comma separated ranges of missing indexes.

Structure
=========

Clique makes it easy to get further information about the structure of a
collection and act on that structure.

To check if a collection contains items that make up a :term:`contiguous`
sequence use :py:meth:`~Collection.is_contiguous`::

    >>> collection = clique.Collection('file.', '.jpg', 4)
    >>> collection.indexes.update([1, 2, 3, 4, 5])
    >>> print collection
    file.%04d.jpg [1-5]
    >>> print collection.is_contiguous()
    True
    >>> collection.indexes.discard(3)
    >>> print collection
    file.%04d.jpg [1-2, 4-5]
    >>> print collection.is_contiguous()
    False

To access the missing indexes in a non-:term:`contiguous` collection use the
:py:meth:`~Collection.holes` method (which returns a new
:py:class:`Collection`)::

    >>> missing = collection.holes()
    >>> print missing.indexes
    [3]

To separate a non-:term:`contiguous` collection into a number of
:term:`contiguous` collections use the :py:meth:`~Collection.separate` method::

    >>> subcollections = collection.separate()
    >>> for subcollection in subcollections:
    ...     print subcollection
    file.%04d.jpg [1-2]
    file.%04d.jpg [4-5]

And to merge compatible collections into another use the
:py:meth:`~Collection.merge` method::

    >>> collection_a = clique.Collection('file.', '.jpg', 4, set([1, 2]))
    >>> collection_b = clique.Collection('file.', '.jpg', 4, set([4, 5]))
    >>> print collection_a.indexes
    [1, 2]
    >>> collection_a.merge(collection_b)
    >>> print collection_a.indexes
    [1, 2, 4, 5]

.. note::

    The collection being merged into is modified in-place, whilst the
    collection being merged is left unaltered.

A collection can be tested for compatibility using the
:py:meth:`~Collection.is_compatible` method::

    >>> collection_a = clique.Collection('file.', '.jpg', 4, set([1, 2]))
    >>> collection_b = clique.Collection('file.', '.jpg', 4, set([4, 5]))
    >>> collection_c = clique.Collection('file.', '.dpx', 4, set([4, 5]))

    >>> print collection_a.is_compatible(collection_b)
    True
    >>> print collection_a.is_compatible(collection_c)
    False

