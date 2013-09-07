# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import collections
import bisect


class SortedSet(collections.MutableSet):
    '''Maintain sorted collection of unique items.'''

    def __init__(self, iterable=None):
        '''Initialise with items from *iterable*.'''
        super(SortedSet, self).__init__()
        self._members = []
        if iterable:
            for item in iterable:
                self.add(item)

    def __contains__(self, item):
        '''Return whether *item* is present.'''

    def __len__(self):
        '''Return number of items.'''

    def __iter__(self):
        '''Return iterator over items.'''

    def add(self, item):
        '''Add *item*.'''

    def discard(self, item):
        '''Remove *item*.'''
