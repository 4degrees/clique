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
    
    collections, remainder = clique.assemble(items)

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

    expected = ['file.ext', 'single.1.ext']
    assert sorted(remainder) == sorted(expected)


def test_assemble_case_sensitive():
    '''Assemble collections respecting casing.'''
    collections, _ = clique.assemble(
        [
            'head_v1.001.ext', 'head_v1.002.ext',
            'HEAD_v1.003.ext', 'HEAD_v1.004.ext'
        ],
        case_sensitive=True
    )
    expected = [
        clique.Collection('head_v1.', '.ext', 3, indexes=set([1, 2])),
        clique.Collection('HEAD_v1.', '.ext', 3, indexes=set([3, 4]))
    ]

    assert collections == expected


def test_assemble_case_insensitive():
    '''Assemble collections ignoring casing.'''
    collections, _ = clique.assemble(
        ['head_v1.001.ext', 'HEAD_v1.002.ext', 'head_v1.003.ext'],
        case_sensitive=False
    )
    expected = [
        clique.Collection('head_v1.', '.ext', 3, indexes=set([1, 2, 3]))
    ]

    assert collections == expected


def test_assemble_no_patterns():
    '''Assemble with no patterns.'''
    assert clique.assemble(['1', '2'], patterns=[]) == ([], ['1', '2'])


def test_assemble_with_custom_pattern():
    '''Assemble with custom pattern.'''
    collections, _ = clique.assemble(
        ['head_v1.001.ext', 'head_v1.002.ext'],
        patterns=[re.compile('\.{0}\.ext$'.format(clique.DIGITS_PATTERN))]
    )
    expected = [clique.Collection('head_v1.', '.ext', 3, indexes=set([1, 2]))]

    assert collections == expected


def test_assemble_compile_pattern():
    '''Compile string based custom pattern.'''
    collections, _ = clique.assemble(
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

    collections, _ = clique.assemble(items, minimum_items=1)
    expected = [
        clique.Collection('head_v', '.001.ext', 0, indexes=set([1, 2])),
        clique.Collection('head_v', '.002.ext', 0, indexes=set([1, 2])),
        clique.Collection('head_v', '.003.ext', 0, indexes=set([1])),
        clique.Collection('head_v1.', '.ext', 3, indexes=set([1, 2, 3])),
        clique.Collection('head_v2.', '.ext', 3, indexes=set([1, 2]))
    ]
    assert sorted(collections) == sorted(expected)

    collections, _ = clique.assemble(items, minimum_items=3)
    expected = [
        clique.Collection('head_v1.', '.ext', 3, indexes=set([1, 2, 3]))
    ]
    assert collections == expected

    collections, _ = clique.assemble(items, minimum_items=5)
    expected = []
    assert collections == expected


@pytest.mark.parametrize(('items', 'expected'), [
    (
        ['0999', '1000', '1001', '9999'],
        [
            clique.Collection('', '', 4, indexes=set([999, 1000, 1001, 9999]))
        ]
    ),
    (
        ['999', '0999', '1000', '1001', '9999'],
        [
            clique.Collection('', '', 4, indexes=set([999, 1000, 1001, 9999])),
            clique.Collection('', '', 0, indexes=set([999, 1000, 1001, 9999]))
        ]
    ),
    (
        ['0999', '1000', '9999', '10001'],
        [
            clique.Collection('', '', 4, indexes=set([999, 1000, 9999])),
            clique.Collection('', '', 0, indexes=set([1000, 9999, 10001]))
        ]
    )
], ids=[
    'padding boundary aligned',
    'ambiguous padding boundary',
    'non-padding boundary indexes'
])
def test_assemble_boundary_padding(items, expected):
    '''Assemble items across a padding boundary.'''
    collections, _ = clique.assemble(items)
    assert sorted(collections) == sorted(expected)


def test_assemble_remainder_has_no_duplicates():
    '''Assemble items and check remainder contains no duplicates.'''
    items = ['00-11-22-33-44-55.jpg']
    collections, remainder = clique.assemble(items, minimum_items=2)
    assert remainder == items


@pytest.mark.parametrize(('items', 'assume_padded', 'expected'), [
    (
        ['1000', '1001', '1002'],
        False,
        [
            clique.Collection('', '', 0, indexes={1000, 1001, 1002})
        ]
    ),
    (
        ['1000', '1001', '1002'],
        True,
        [
            clique.Collection('', '', 4, indexes={1000, 1001, 1002})
        ]
    ),
    (
        ['999', '1000', '1001'],
        False,
        [
            clique.Collection('', '', 0, indexes={999, 1000, 1001})
        ]
    ),
    (
        ['999', '1000', '1001'],
        True,
        [
            clique.Collection('', '', 0, indexes={999, 1000, 1001})
        ]
    ),
    (
        ['0999', '1000', '1001'],
        False,
        [
            clique.Collection('', '', 4, indexes={999, 1000, 1001})
        ]
    ),
    (
        ['0999', '1000', '1001'],
        True,
        [
            clique.Collection('', '', 4, indexes={999, 1000, 1001})
        ]
    ),
    (
        [],
        True,
        []
    )
], ids=[
    'ambiguous assume unpadded',
    'ambiguous assume padded',
    'unambiguous unpadded assume unpadded',
    'unambiguous unpadded assume padded',
    'unambiguous padded assume unpadded',
    'unambiguous padded assume padded',
    'empty collection'
])
def test_assemble_assume_padded(items, assume_padded, expected):
    '''Assemble items according to assume padded option.'''
    collections, remainder = clique.assemble(
        items, assume_padded_when_ambiguous=assume_padded
    )
    assert collections == expected


@pytest.mark.parametrize(('value', 'pattern', 'expected'), [
    ('/path/to/file.%04d.ext []', None,
     clique.Collection('/path/to/file.', '.ext', 4, [])),
    ('/path/to/file.%04d.ext [1-3, 5, 7-8]', None,
     clique.Collection('/path/to/file.', '.ext', 4, [1, 2, 3, 5, 7, 8])),
    ('/path/to/file.%d.ext [1-3, 5, 7-8]', None,
     clique.Collection('/path/to/file.', '.ext', 0, [1, 2, 3, 5, 7, 8])),
    ('/path/to/file.%d.ext 1-8',
     '{head}{padding}{tail} {range}',
     clique.Collection('/path/to/file.', '.ext', 0, [1, 2, 3, 4, 5, 6, 7, 8])),
    ('/path/to/file.%d.ext 1-8 [2, 4-6]',
     '{head}{padding}{tail} {range} [{holes}]',
     clique.Collection('/path/to/file.', '.ext', 0, [1, 3, 7, 8]))
], ids=[
    'empty',
    'padded',
    'unpadded',
    'custom range pattern',
    'custom holes pattern'
])
def test_parse(value, pattern, expected):
    '''Construct collection by parsing formatted string.'''
    if pattern is None:
        assert clique.parse(value) == expected
    else:
        assert clique.parse(value, pattern=pattern) == expected


def test_non_matching_parse():
    '''Fail to parse non-matching value.'''
    with pytest.raises(ValueError):
        clique.parse('')