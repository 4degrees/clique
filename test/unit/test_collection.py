# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import sys
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


@pytest.mark.parametrize(('name', 'value', 'pattern', 'item'), [
    (
     'head',
     'diff_head.',
     '^diff\\_head\\.(?P<index>(?P<padding>0*)\d+?)\\.tail$',
     'diff_head.1.tail'
    ),

    (
     'tail',
     '.diff_tail',
     '^head\\.(?P<index>(?P<padding>0*)\d+?)\\.diff\\_tail$',
     'head.1.diff_tail'
    ),
    (
     'padding',
     4,
     '^head\\.(?P<index>(?P<padding>0*)\d+?)\\.tail$',
     'head.0001.tail'
    )
])
def test_change_property(name, value, pattern, item):
    '''Change property.'''
    collection = Collection('head.', '.tail', 0, indexes=set([1]))

    setattr(collection, name, value)
    assert getattr(collection, name) == value

    assert collection._expression.pattern == pattern
    assert list(collection)[0] == item


def test_unsettable_indexes():
    '''Set new indexes by attribute assignment.'''
    collection = Collection('head.', '.tail', 0, indexes=set([1]))
    with pytest.raises(AttributeError):
        collection.indexes = [1, 3]


def test_str():
    '''String representation.'''
    collection = Collection('head.', '.tail', 0, indexes=set([1, 2, 3]))
    assert str(collection) == 'head.%d.tail [1-3]'


def test_repr():
    '''Repr representation.'''
    collection = Collection('head.', '.tail', 0, indexes=set([1, 2, 3]))
    assert repr(collection) == '<Collection "head.%d.tail [1-3]">'


@pytest.mark.parametrize(('collection', 'expected'), [
    (UnpaddedCollection(indexes=set([1, 100, 1000])),
     ['/head.1.ext', '/head.100.ext', '/head.1000.ext']),

    (PaddedCollection(indexes=set([1, 100, 1000])),
     ['/head.0001.ext', '/head.0100.ext', '/head.1000.ext'])
], ids=[
    'unpadded-collection',
    'padded-collection',
])
def test_iterator(collection, expected):
    '''Iterate over items in collection.'''
    assert list(collection) == expected


@pytest.mark.parametrize(('item', 'expected'), [
    ('/head.0001.ext', True),
    ('/diff_head.0001.ext', False),
    ('/head.0001.diff_ext', False),
    ('/head.1000.ext', False)
], ids=[
    'valid member',
    'different head',
    'different tail',
    'non-member index'
])
def test_contains(item, expected):
    '''Collection contains item.'''
    collection = PaddedCollection(indexes=set([1]))
    assert (item in collection) == expected


@pytest.mark.parametrize(('collection_a', 'collection_b', 'expected'), [
    (Collection('head', 'tail', 0), Collection('head', 'tail', 0), 0),
    (Collection('head', 'tail', 0), Collection('diff_head', 'tail', 0), -1),
    (Collection('head', 'tail', 0), Collection('head', 'diff_tail', 0), -1),
    (Collection('head', 'tail', 0), Collection('head', 'tail', 4), 1),
    (Collection('head', 'tail', 0, indexes=set([1, 2])),
     Collection('head', 'tail', 0, indexes=set([1])), -1),
], ids=[
    'equal',
    'different head (b > a)',
    'different tail (b > a)',
    'different padding (a > b)',
    'different indexes (b > a)'
])
def test_comparisons(collection_a, collection_b, expected):
    '''Compare collections.'''
    equal = (expected == 0)
    assert (collection_a == collection_b) == equal
    assert (collection_a != collection_b) == (not equal)

    if not equal:
        greater = (expected == -1)
        assert (collection_a > collection_b) == greater
        assert (collection_a < collection_b) == (not greater)

        assert (collection_a >= collection_b) == greater
        assert (collection_a <= collection_b) == (not greater)

    else:
        assert (collection_a >= collection_b) == True
        assert (collection_a <= collection_b) == True


def test_not_implemented_comparison():
    '''Compare collection against non-collection.'''
    collection = UnpaddedCollection()
    for comparison in (
        '__eq__', '__ne__', '__lt__', '__gt__', '__ge__', '__le__'
    ):
        assert getattr(collection, comparison)(None) is NotImplemented


@pytest.mark.parametrize(('collection', 'item', 'matches'), [
    (UnpaddedCollection(), '/diff_head.1001.ext', False),
    (UnpaddedCollection(), '/head.1001.diff_ext', False),

    (UnpaddedCollection(), '/head.1001.ext', True),
    (UnpaddedCollection(), '/head.0001.ext', False),

    (PaddedCollection(), '/head.0001.ext', True),
    (PaddedCollection(), '/head.1001.ext', True),
    (PaddedCollection(), '/head.10001.ext', False)
], ids=[
    'different head',
    'different tail',

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

    with pytest.raises(CollectionError):
        collection.remove('/diff_head.0001.ext')


@pytest.mark.parametrize(('CollectionCls', 'pattern', 'expected'), [
    (PaddedCollection, '{head}', '/head.'),
    (PaddedCollection, '{padding}', '%04d'),
    (UnpaddedCollection, '{padding}', '%d'),
    (PaddedCollection, '{tail}', '.ext'),
    (PaddedCollection, '{range}', '1-12'),
    (PaddedCollection, '{ranges}', '1-3, 7, 9-12'),
    (PaddedCollection, '{holes}', '4-6, 8'),
])
def test_format(CollectionCls, pattern, expected):
    '''Format collection according to pattern.'''
    collection = CollectionCls(indexes=set([1, 2, 3, 7, 9, 10, 11, 12]))
    assert collection.format(pattern) == expected


def test_format_sparse_collection():
    '''Format sparse collection without recursion error.'''
    recursion_limit = sys.getrecursionlimit()
    recursion_error_occurred = False

    try:
        collection = PaddedCollection(
            indexes=set(range(0, recursion_limit * 2, 2))
        )
        collection.format()
    except RuntimeError as error:
        if 'maximum recursion depth exceeded' in str(error):
            recursion_error_occurred = True
        else:
            raise

    assert not recursion_error_occurred


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
    (set([]), set([])),
    (set([1]), set([])),
    (set([8, 9, 10, 11]), set([])),
    (set([2, 3]), set([])),
    (set([1, 3]), set([2])),
    (set([1, 5]), set([2, 3, 4])),
    (set([1, 5, 6, 7, 12]), set([2, 3, 4, 8, 9, 10, 11]))
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
    assert holes.indexes == expected


@pytest.mark.parametrize(('collection_a', 'collection_b', 'expected'), [
    (Collection('head', 'tail', 0),
     Collection('head', 'tail', 0, indexes=set([1, 2])),
     True
    ),
    (Collection('head', 'tail', 0), Collection('diff_head', 'tail', 0), False),
    (Collection('head', 'tail', 0), Collection('head', 'diff_tail', 0), False),
    (Collection('head', 'tail', 0), Collection('head', 'tail', 4), False)
], ids=[
    'compatible',
    'incompatible head',
    'incompatible tail',
    'incompatible padding'
])
def test_is_compatible(collection_a, collection_b, expected):
    '''Check collection compatibility.'''
    assert collection_a.is_compatible(collection_b) == expected


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


def test_escaping_expression():
    '''Escape non-regular expression components.'''
    collection = Collection('prefix\\file.', '.ext', 1, [1])
    assert 'prefix\\file.1.ext' in collection
