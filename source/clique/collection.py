# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import re

import clique.descriptor
import clique.error


class Collection(object):
    '''Represent group of items that differ only by numerical component.'''

    head = clique.descriptor.ReadOnly('head')
    tail = clique.descriptor.ReadOnly('tail')
    padding = clique.descriptor.ReadOnly('padding')

    def __init__(self, head, tail, padding, indexes=None):
        '''Initialise collection.

        *head* is the leading common part whilst *tail* is the trailing
        common part.

        *padding* specifies the "width" of the numerical component. An index
        will be padded with zeros to fill this width. A *padding* of zero
        implies no padding and width may be any size so long as no leading
        zeros are present.

        *indexes* can specify a set of numerical indexes to initially populate
        the collection with.

        '''
        super(Collection, self).__init__()
        self.__dict__.update({
            'head': head,
            'tail': tail,
            'padding': padding
        })
        self.indexes = set()
        if indexes is not None:
            self.indexes.update(indexes)

        self._pattern = re.compile('^{0}(?P<index>(?P<padding>0*)\d+?){1}$'
                                   .format(self.head, self.tail))

    def __iter__(self):
        '''Return iterator over items in collection.'''

    def __contains__(self, item):
        '''Return whether *item* is present in collection.'''

    def match(self, item):
        '''Return whether *item* matches this collection pattern.

        If a match is successful return data about the match otherwise return
        None.

        '''
        match = self._pattern.match(item)
        if not match:
            return None

        index = match.group('index')
        padded = False
        if match.group('padding'):
            padded = True

        if self.padding == 0:
            if padded:
                return None

        elif len(index) != self.padding:
            return None

        return match

    def add(self, item):
        '''Add *item* to collection.

        raise :py:class:`~clique.error.CollectionError` if *item* cannot be
        added to the collection.

        '''
        match = self.match(item)
        if match is None:
            raise clique.error.CollectionError(
                'Item does not match sequence pattern.'
            )

        self.indexes.add(int(match.group('index')))

    def remove(self, item):
        '''Remove *item* from collection.

        raise :py:class:`~clique.error.CollectionError` if *item* cannot be
        removed from the collection.

        '''
        match = self.match(item)
        if match is None:
            raise clique.error.CollectionError('Item not present in sequence.')

        index = int(match.group('index'))
        try:
            self.indexes.remove(index)
        except KeyError:
            raise clique.error.CollectionError('Item not present in sequence.')

    def format(self, pattern):
        '''Return string representation as specified by *pattern*.'''

    def is_contiguous(self):
        '''Return whether entire collection is contiguous.'''
        previous = None
        for index in sorted(self.indexes):
            if previous is None:
                previous = index
                continue

            if index != (previous + 1):
                return False

            previous = index

        return True

    def holes(self):
        '''Return holes in collection.

        Return :py:class:`~clique.collection.Collection` of missing indexes.

        '''
        missing = set([])
        previous = None
        for index in sorted(self.indexes):
            if previous is None:
                previous = index
                continue

            if index != (previous + 1):
                missing.update(range(previous + 1, index))

            previous = index

        return Collection(self.head, self.tail, self.padding, indexes=missing)

    def is_compatible(self, collection):
        '''Return whether *collection* is compatible with this collection.

        To be compatible *collection* must have the same head, tail and padding
        properties as this collection.

        '''
        return all([
            isinstance(collection, Collection),
            collection.head == self.head,
            collection.tail == self.tail,
            collection.padding == self.padding
        ])

    def merge(self, collection):
        '''Merge *collection* into this collection.

        If the *collection* is compatible with this collection then update
        indexes with all indexes in *collection*.

        raise :py:class:`~clique.error.CollectionError` if *collection* is not
        compatible with this collection.

        '''
        if not self.is_compatible(collection):
            raise clique.error.CollectionError('Collection is not compatible '
                                               'with this collection.')

        self.indexes.update(collection.indexes)

    def separate(self):
        '''Return contiguous parts of collection as separate collections.

        Return as list of :py:class:`~clique.collection.Collection` instances.

        '''
