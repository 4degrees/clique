..
    :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
    :license: See LICENSE.txt.

********
Glossary
********

.. glossary::

    contiguous
        When all items in a collection are sequential with no missing indexes.
        For example, *1, 2, 3* is contiguous whilst *1, 3* is not.

    head
        The common leading part of items in a collection. For example, the
        items *file.0001.jpg*, *file.0002.jpg*, *file.0003.jpg* have a head
        value of *file.*

    padding
        The width of the numerical index in a collection. Each item's index
        will be padded with zeroes to match this width. A padding of 4 would
        result in *1* becoming *0001*. A padding of 0 means no width is defined
        and an index can be any width so long as it has no preceding zeroes.

    pip
        The recommended tool for installing Python packages.

        .. seealso:: https://pip.pypa.io

    tail
        The common trailing part of items in a collection. For example, the
        items *file.0001.jpg*, *file.0002.jpg*, *file.0003.jpg* have a tail
        value of *.jpg*

    Virtualenv
        A tool to create isolated Python environments.

        .. seealso:: https://virtualenv.pypa.io/en/latest/

