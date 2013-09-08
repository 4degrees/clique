# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import pytest

from clique.sorted_set import SortedSet


def test_str():
    '''String representation.'''
    sorted_set = SortedSet([1, 3, 2])
    assert str(sorted_set) == '[1, 2, 3]'


def test_repr():
    '''Repr representation.'''
    sorted_set = SortedSet([1, 3, 2])
    assert repr(sorted_set) == '<SortedSet "[1, 2, 3]">'


@pytest.mark.parametrize(('sorted_set', 'item', 'expected'), [
    (SortedSet([1]), 1, True),
    (SortedSet([1]), 10, False)
], ids=[
    'item present',
    'item not present'
])
def test_contains(sorted_set, item, expected):
    '''Check item membership.'''
    assert (item in sorted_set) is expected


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


def test_update():
    '''Update with items from another iterable.'''
    sorted_set = SortedSet([1, 2, 3])
    sorted_set.update([1, 4, 5, 6])
    assert list(sorted_set) == [1, 2, 3, 4, 5, 6]


def test_iter():
    '''Iterate over ordered items.'''
    sorted_set = SortedSet([5, 2, 3, 4, 8, 9, 1, 1])
    assert list(sorted_set) == [1, 2, 3, 4, 5, 8, 9]

