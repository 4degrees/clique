..
    :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
    :license: See LICENSE.txt.

.. _release/release_notes:

*************
Release Notes
*************

.. release:: 1.5.0
    :date: 2017-08-05

    .. change:: new

        Support controlling :func:`clique.assemble` padding behaviour for
        ambiguous collections, through use of a new
        *assume_padded_when_ambiguous* option.

.. release:: 1.4.2
    :date: 2017-07-23

    .. change:: fixed

        :func:`clique.parse` errors under Python 3 due to change in :func:`map`
        behaviour.

.. release:: 1.4.1
    :date: 2017-07-23

    .. change:: fixed

        Documentation fails to build on `Read The Docs
        <http://readthedocs.org/>`__ due to 'doc' extras not being installed.

.. release:: 1.4.0
    :date: 2017-07-23

    .. change:: changed

        Modernised project structure. No API changes.

        Project is now easier to install, manage and develop. It also comes with
        release notes!

.. release:: 1.3.1
    :date: 2016-04-30

    .. change:: fixed

        :meth:`Collection.format <clique.collection.Collection.format>` hits
        maximum recursion depth for collections with lots of holes.

.. release:: 1.3.0
    :date: 2014-08-31

    .. change:: new

        Support ability to control case sensitivity when :func:`assembling
        <clique.assemble>` collections.

        .. seealso:: :ref:`assembly/case_sensitivity`

    .. change:: fixed

        Parsing a string representing an empty collection fails.

.. release:: 1.2.1
    :date: 2014-07-09

    .. change:: fixed

        :func:`clique.assemble` returns incorrect remainder when input path
        matches several patterns.

.. release:: 1.2.0
    :date: 2013-10-15

    .. change:: new

        Support :func:`parsing <clique.parse>` a string to create a
        :class:`clique.collection.Collection`.

.. release:: 1.1.0
    :date: 2013-10-03

    .. change:: new

        Return from :func:`clique.assemble` items that do not belong to any
        collection in addition to the assembled collections::

            collections, remainder = clique.assemble(items)

    .. change:: new

        Support :func:`assembling <clique.assemble>` collections that cross
        padding boundaries. For example, 0998-1001.

    .. change:: fixed

        :meth:`Collection.match` returns incorrect result when :term:`head` or
        :term:`tail` contain characters that can be interpreted as regular
        expression patterns.

.. release:: 1.0.0
    :date: 2013-09-06
    
    .. change:: new

        Initial release.

        Provide :class:`~clique.collection.Collection` to represent collections
        of items that differ only by a commonly changing numerical component.
        Include helper functions for :func:`assembling <clique.assemble>`
        collections automatically from input data.

        .. seealso:: :ref:`introduction`
