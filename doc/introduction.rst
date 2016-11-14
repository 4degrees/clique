..
    :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
    :license: See LICENSE.txt.

.. _introduction:

************
Introduction
************

Clique is a library for managing collections that have a common numerical
component.

A numerical component is any series of numbers in an item. The item
*sc010_020_v001.0005.dpx* has four possible numerical components
(**bolded**):

    * sc\ **010**\ _020_v001.0005.dpx
    * sc010\_\ **020**\ _v001.0005.dpx
    * sc010_020_v\ **001**\ .0005.dpx
    * sc010_020_v001.\ **0005**\ .dpx

A common use would be to determine sequences of files on disk. For example,
given the following input:

    * file.0001.dpx
    * file.0002.dpx
    * file.0001.jpg
    * file.0002.jpg

Clique can automatically assemble two collections:

    * file.[index].dpx
    * file.[index].jpg

where *[index]* is the commonly changing numerical component.

Read the :ref:`tutorial` to find out more.
