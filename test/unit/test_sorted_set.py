# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import pytest

from clique.sorted_set import SortedSet


@pytest.fixture
def standard_set(request):
    '''Return sorted set.'''
    return SortedSet([4, 5, 6, 7, 2, 1, 1])


@pytest.mark.parametrize(('item', 'expected'), [
    (1, True),
    (10, False)
], ids=[
    'item present',
    'item not present'
])
def test_contains(item, expected, standard_set):
    '''Check item membership.'''
    assert (item in standard_set) is expected


@pytest.mark.parametrize(('sorted_set', 'expected'), [
    (SortedSet(), 0),
    (SortedSet([]), 0),
    (SortedSet([1]), 1),
    (SortedSet([1, 2, 3]), 3),
    (SortedSet([1, 1, 2, 2, 3, 3]), 3)
], ids=[
    'no iterable',
    'empty iterable',
    'single item',
    'multiple items',
    'duplicate multiple items'
])
def test_len(sorted_set, expected):
    '''Calculate set length.'''
    assert len(sorted_set) == expected


@pytest.fixture
def standard_set(request):
    '''Return sorted set.'''
    return SortedSet([4, 5, 6, 7, 2, 1, 1])


@pytest.mark.parametrize(('sorted_set', 'item', 'expected'), [
    (SortedSet(), 1, 1),
    (SortedSet([1]), 1, 1),
    (SortedSet([1]), 2, 2)
], ids=[
    'item',
    'existing item',
    'new item'
])
def test_add(sorted_set, item, expected):
    '''Add item.'''
    sorted_set.add(item)
    assert item in sorted_set
    assert len(sorted_set) == expected


@pytest.mark.parametrize(('sorted_set', 'item'), [
    (SortedSet([1]), 1),
    (SortedSet(), 1)
], ids=[
    'present item',
    'missing item'
])
def test_discard(sorted_set, item):
    '''Discard item.'''
    sorted_set.discard(item)
    assert item not in sorted_set
