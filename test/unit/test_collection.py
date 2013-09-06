# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import inspect

import pytest

from clique.collection import Collection
from clique.error import CollectionError


def UnpaddedCollection(**kw):
    '''Return an unpadded collection.'''
    return Collection('/head.', '.ext', padding=0, **kw)


def PaddedCollection(**kw):
    '''Return a padded collection.'''
    return Collection('/head.', '.ext', padding=4, **kw)


@pytest.mark.parametrize(('collection', 'item', 'matches'), [
    (UnpaddedCollection(), '/head.1001.ext', True),
    (UnpaddedCollection(), '/head.0001.ext', False),

    (PaddedCollection(), '/head.0001.ext', True),
    (PaddedCollection(), '/head.1001.ext', True),
    (PaddedCollection(), '/head.10001.ext', False)
], ids=[
    'unpadded-collection:unpadded item',
    'unpadded-collection:padded item',

    'padded-collection:padded item',
    'padded-collection:unpadded item within padding bounds',
    'padded-collection:unpadded item outside padding bounds'
])
def test_match(collection, item, matches):
    '''Match item to collection.'''
    match = collection.match(item)
    if matches is True:
        assert match is not None
    else:
        assert match is None


@pytest.mark.parametrize(('collection', 'item', 'expected'), [
    (UnpaddedCollection(), '/head.1001.ext', set([1001])),
    (UnpaddedCollection(), '/head.0001.ext', CollectionError),

    (PaddedCollection(), '/head.0001.ext', set([1])),
    (PaddedCollection(), '/head.1001.ext', set([1001])),
    (PaddedCollection(), '/head.10001.ext', CollectionError)
], ids=[
    'unpadded-collection:unpadded item',
    'unpadded-collection:padded item',

    'padded-collection:padded item',
    'padded-collection:unpadded item within padding bounds',
    'padded-collection:unpadded item outside padding bounds'
])
def test_add(collection, item, expected):
    '''Add items to collection.'''
    if inspect.isclass(expected):
        with pytest.raises(expected):
            collection.add(item)

    else:
        collection.add(item)
        assert collection.indexes == expected


def test_add_duplicate():
    '''Add item twice.'''
    collection = PaddedCollection()
    assert collection.indexes == set()

    collection.add('/head.0001.ext')
    assert collection.indexes == set([1])

    collection.add('/head.0001.ext')
    assert collection.indexes == set([1])


def test_remove():
    '''Remove existing item from collection.'''
    collection = PaddedCollection(indexes=set([1, 5, 10]))
    assert collection.indexes == set([1, 5, 10])

    collection.remove('/head.0005.ext')
    assert collection.indexes == set([1, 10])


def test_remove_non_member():
    '''Remove item that is not member of collection.'''
    collection = PaddedCollection(indexes=set([1, 5, 10]))
    assert collection.indexes == set([1, 5, 10])

    with pytest.raises(CollectionError):
        collection.remove('/head.0100.ext')


@pytest.mark.parametrize(('pattern', 'expected'), [
    ('{head}', '/head'),
    ('{padding}', '%04d'),
    ('{tail}', '.ext'),
    ('{range}', '1-12'),
    ('{ranges}', '1-3, 7, 9-12'),
    ('{holes}', '4-6, 8'),

])
def test_format(pattern, expected):
    '''Format collection according to pattern.'''
    collection = PaddedCollection(indexes=set([1, 2, 3, 7, 9, 10, 11, 12]))
    assert collection.format(pattern) == expected


@pytest.mark.parametrize(('collection', 'expected'), [
    (PaddedCollection(indexes=set([])), True),
    (PaddedCollection(indexes=set([1])), True),
    (PaddedCollection(indexes=set([1, 2, 3])), True),
    (PaddedCollection(indexes=set([1, 3])), False)
], ids=[
    'empty',
    'single',
    'contiguous indexes',
    'non-contiguous'
])
def test_is_contiguous(collection, expected):
    '''Check whether collection is contiguous.'''
    assert collection.is_contiguous() is expected


@pytest.mark.parametrize(('indexes', 'expected'), [
    (set([]), []),
    (set([1]), []),
    (set([8, 9, 10, 11]), []),
    (set([2, 3]), []),
    (set([1, 3]), [set([2])]),
    (set([1, 5]), [set([2, 3, 4])]),
    (set([1, 5, 6, 7, 12]), [set([2, 3, 4]), set([8, 9, 10, 11])])
], ids=[
    'empty',
    'single index',
    'contiguous indexes',
    'missing leading index',
    'single missing index',
    'range of missing indexes',
    'multiple ranges of missing indexes'
])
def test_holes(indexes, expected):
    '''Retrieve holes in collection.'''
    collection = PaddedCollection(indexes=indexes)
    holes = collection.holes()
    assert len(holes) == len(expected)

    if expected:
        for index, indexes in enumerate(expected):
            assert holes[index].indexes == indexes


@pytest.mark.parametrize(('collection_a', 'collection_b', 'expected'), [
    (PaddedCollection(), PaddedCollection(), set([])),
    (PaddedCollection(indexes=set([1])), PaddedCollection(indexes=set([2])),
     set([1, 2])),
    (PaddedCollection(indexes=set([1, 2])), PaddedCollection(indexes=set([2])),
     set([1, 2]))
], ids=[
    'both empty',
    'complimentary',
    'duplicates'
])
def test_compatible_merge(collection_a, collection_b, expected):
    '''Merge a compatible collection into another.'''
    collection_a.merge(collection_b)
    assert collection_a.indexes == expected


@pytest.mark.parametrize(('collection_a', 'collection_b'), [
    (Collection('head', 'tail', 0), Collection('diff_head', 'tail', 0)),
    (Collection('head', 'tail', 0), Collection('head', 'diff_tail', 0)),
    (Collection('head', 'tail', 0), Collection('head', 'tail', 4))
], ids=[
    'incompatible head',
    'incompatible tail',
    'incompatible padding'
])
def test_incompatible_merge(collection_a, collection_b):
    '''Merge an incompatible collection into another.'''
    with pytest.raises(CollectionError):
        collection_a.merge(collection_b)


@pytest.mark.parametrize(('collection', 'expected'), [
    (PaddedCollection(indexes=set([])), [set([])]),
    (PaddedCollection(indexes=set([1])), [set([1])]),
    (PaddedCollection(indexes=set([1, 2, 3])), [set([1, 2, 3])]),
    (PaddedCollection(indexes=set([1, 2, 5, 6, 7, 9, 10])),
     [set([1, 2]), set([5, 6, 7]), set([9, 10])]),

], ids=[
    'empty',
    'single index',
    'contiguous indexes',
    'non-contiguous indexes'
])
def test_separate(collection, expected):
    '''Separate collection into contiguous parts.'''
    parts = collection.separate()
    assert len(parts) == len(expected)

    if expected:
        for index, indexes in enumerate(expected):
            assert parts[index].indexes == indexes

