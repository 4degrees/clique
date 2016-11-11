..
    :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
    :license: See LICENSE.txt.

.. _assembly:

********
Assembly
********

.. module:: clique

As seen in the :ref:`tutorial`, Clique provides the high-level
:py:func:`assemble` function to support automatically assembling items into
relevant :ref:`collections <collection>` based on a common changing
numerical component::

    >>> import clique
    >>> collections, remainder = clique.assemble([
    ...     'file.0001.jpg', 'file.0002.jpg', 'file.0003.jpg',
    ...     'file.0001.dpx', 'file.0002.dpx', 'file.0003.dpx'
    ... ])
    >>> print collections
    [<Collection "file.%04d.dpx [1-3]">, <Collection "file.%04d.jpg [1-3]">]

.. note::

    Any items that are not members of a returned collection can be found in
    the *remainder* list.

However, as mentioned in the :ref:`introduction`, Clique has no understanding
of what a numerical component represents. Therefore, it takes a conservative
approach and considers **all** collections with a common changing numerical
component as valid. This can lead to surprising results at first::

    >>> collections, remainder = clique.assemble([
    ...     'file_v1.0001.jpg', 'file_v1.0002.jpg', 'file_v1.0003.jpg',
    ...     'file_v2.0001.jpg', 'file_v2.0002.jpg', 'file_v2.0003.jpg'
    ... ])
    >>> print collections
    [<Collection "file_v1.%04d.jpg [1-3]">,
     <Collection "file_v2.%04d.jpg [1-3]">,
     <Collection "file_v%d.0001.jpg [1-2]">,
     <Collection "file_v%d.0002.jpg [1-2]">,
     <Collection "file_v%d.0003.jpg [1-2]">]

Here, Clique returned more collections than might have been expected, but, as
can be seen, they are all valid collections. This is an important feature of
Clique - it doesn't attempt to guess. Instead, it is designed to be wrapped
easily with domain specific logic to get the results desired.

There are a couple of ways to influence the returned result from the
:py:func:`~assemble` function:

    * Pass a *minimum_items* argument.
    * Pass custom *patterns*.

Minimum Items
=============

By default, Clique will filter out any collection from the returned result of
:py:func:`~assemble` that has less than two items. This value can be customised
per :py:func:`~assemble` call by passing *minimum_items* as a keyword::

    >>> print clique.assemble(['file.0001.jpg'])[0]
    []
    >>> print clique.assemble(['file.0001.jpg'], minimum_items=1)[0]
    [<Collection "file.%04d.jpg [1]">]

Patterns
========

By default, Clique finds all groups of numbers in each item and creates
collections that have common :term:`head`, :term:`tail` and :term:`padding`
values.

Custom patterns can be used to tailor the process. Pass them as a list of
regular expressions (either strings or :py:class:`re.RegexObject` instances)::

    >>> items = [
    ...     'file.0001.jpg', 'file.0002.jpg', 'file.0003.jpg',
    ...     'file.0001.dpx', 'file.0002.dpx', 'file.0003.dpx'
    ... ])
    >>> print clique.assemble(items, patterns=[
    ...     '\.(?P<index>(?P<padding>0*)\d+)\.\D+\d?$'
    ... ])[0]
    [<Collection "file_v1.%04d.jpg [1-3]">,
     <Collection "file_v2.%04d.jpg [1-3]">]

.. note::

    Each custom expression **must** contain the expression from
    :py:data:`DIGITS_PATTERN` exactly once. An easy way to do this is using
    Python's string formatting.

    So, instead of::

        '\.(?P<index>(?P<padding>0*)\d+)\.\D+\d?$'

    use::

        '\.{0}\.\D+\d?$'.format(clique.DIGITS_PATTERN)

Some common expressions are predefined in the :py:data:`~clique.PATTERNS`
dictionary (contributions welcome!)::

    >>> print clique.assemble(items, patterns=[clique.PATTERNS['frames']])[0]
    [<Collection "file_v1.%04d.jpg [1-3]">,
     <Collection "file_v2.%04d.jpg [1-3]">]

.. _assembly/case_sensitivity:

Case Sensitivity
================

When assembling collections, it is sometimes useful to be able to specify
whether the case of the items should be important or not. For example,
"file.0001.jpg" and "FILE.0002.jpg" could be identified as part of the same
collection or not.

By default the assembly is case sensitive, but this can be controlled by setting
the *case_sensitive* argument::

    >>> items = ['file.0001.jpg', 'FILE.0002.jpg', 'file.0003.jpg']
    >>> print clique.assemble(items, case_sensitive=False)
    [<Collection "file.%04d.jpg [1-3]">], []
    >>> print clique.assemble(items, case_sensitive=True)
    [<Collection "file.%04d.jpg [1, 3]">], ['FILE.0002.jpg']

A common use case might be to ignore case sensitivity when on a Windows or Mac
machine::

    >>> import sys
    >>> clique.assemble(
    ...     items, case_sensitive=sys.platform not in ('win32', 'darwin')
    ... )
