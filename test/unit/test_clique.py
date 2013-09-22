# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import re

import pytest

import clique


def test_assemble():
    '''Assemble collections from arbitrary items.'''
    items = [
        'file.ext',
        'single.1.ext',
        '1', '3',
        '001', '003',
        'head.001.tail', 'head.002.tail',
        'head.1.tail', 'head.2.tail',
        'head.001.tail3', 'head.002.tail3',
        'head_v01.tail', 'head_v02.tail',
        'head_v1.tail', 'head_v2.tail',
        'head1_010_v1.0001.tail', 'head1_010_v1.0002.tail',
        'head1_010_v2.0001.tail', 'head1_010_v2.0002.tail',
        'head1_020_v1.0001.tail', 'head1_020_v1.0002.tail'
    ]
    
    collections = clique.assemble(items)

    expected = [
        clique.Collection('', '', 0, indexes=set([1, 3])),
        clique.Collection('', '', 3, indexes=set([1, 3])),
        clique.Collection('head.', '.tail', 3, indexes=set([1, 2])),
        clique.Collection('head.', '.tail', 0, indexes=set([1, 2])),
        clique.Collection('head.', '.tail3', 3, indexes=set([1, 2])),

        clique.Collection('head_v', '.tail', 2, indexes=set([1, 2])),
        clique.Collection('head_v', '.tail', 0, indexes=set([1, 2])),

        clique.Collection('head1_010_v1.', '.tail', 4, indexes=set([1, 2])),
        clique.Collection('head1_010_v2.', '.tail', 4, indexes=set([1, 2])),
        clique.Collection('head1_020_v1.', '.tail', 4, indexes=set([1, 2])),
        clique.Collection('head1_010_v', '.0001.tail', 0, indexes=set([1, 2])),
        clique.Collection('head1_010_v', '.0002.tail', 0, indexes=set([1, 2])),
        clique.Collection('head1_', '_v1.0001.tail', 3, indexes=set([10, 20])),
        clique.Collection('head1_', '_v1.0002.tail', 3, indexes=set([10, 20]))
    ]

    assert sorted(collections) == sorted(expected)


def test_assemble_no_patterns():
    '''Assemble with no patterns.'''
    assert clique.assemble(['1', '2'], patterns=[]) == []


def test_assemble_with_custom_pattern():
    '''Assemble with custom pattern.'''
    collections = clique.assemble(
        ['head_v1.001.ext', 'head_v1.002.ext'],
        patterns=[re.compile('\.{0}\.ext$'.format(clique.DIGITS_PATTERN))]
    )
    expected = [clique.Collection('head_v1.', '.ext', 3, indexes=set([1, 2]))]

    assert collections == expected


def test_assemble_compile_pattern():
    '''Compile string based custom pattern.'''
    collections = clique.assemble(
        ['head_v1.001.ext', 'head_v1.002.ext'],
        patterns=['\.{0}\.ext$'.format(clique.DIGITS_PATTERN)]
    )
    expected = [clique.Collection('head_v1.', '.ext', 3, indexes=set([1, 2]))]

    assert collections == expected


def test_assemble_minimum_items_filter():
    '''Filter assembled collections by minimum number of items.'''
    items = [
        'head_v1.001.ext', 'head_v1.002.ext', 'head_v1.003.ext',
        'head_v2.001.ext', 'head_v2.002.ext'
    ]

    collections = clique.assemble(items, minimum_items=1)
    expected = [
        clique.Collection('head_v', '.001.ext', 0, indexes=set([1, 2])),
        clique.Collection('head_v', '.002.ext', 0, indexes=set([1, 2])),
        clique.Collection('head_v', '.003.ext', 0, indexes=set([1])),
        clique.Collection('head_v1.', '.ext', 3, indexes=set([1, 2, 3])),
        clique.Collection('head_v2.', '.ext', 3, indexes=set([1, 2]))
    ]
    assert sorted(collections) == sorted(expected)

    collections = clique.assemble(items, minimum_items=3)
    expected = [
        clique.Collection('head_v1.', '.ext', 3, indexes=set([1, 2, 3]))
    ]
    assert collections == expected

    collections = clique.assemble(items, minimum_items=5)
    expected = []
    assert collections == expected


def test_assemble_boundary_padding():
    '''Assemble items across a padding boundary.'''
    items = ['0998', '0999', '1000', '1001', '9999']
    collections = clique.assemble(items)
    expected = [
        clique.Collection('', '', 4, indexes=set([998, 999, 1000, 1001, 9999]))
    ]

    assert sorted(collections) == sorted(expected)

