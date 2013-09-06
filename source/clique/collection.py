# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import re

import clique.descriptor


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

    def add(self, item):
        '''Add *item* to collection.

        raise :py:class:`~clique.error.CollectionError` if *item* cannot be
        added to the collection.

        '''

    def remove(self, item):
        '''Remove *item* from collection.

        raise :py:class:`~clique.error.CollectionError` if *item* cannot be
        removed from the collection.

        '''

    def format(self, pattern):
        '''Return string representation as specified by *pattern*.'''

    def is_contiguous(self):
        '''Return whether entire collection is contiguous.'''

    def holes(self):
        '''Return holes in collection.

        Return :py:class:`~clique.collection.Collection` of missing indexes.

        '''

    def merge(self, collection):
        '''Merge *collection* into this collection.

        If the *collection* is compatible with this collection then update
        indexes with all indexes in *collection*.

        '''

    def separate(self):
        '''Return contiguous parts of collection as separate collections.

        Return as list of :py:class:`~clique.collection.Collection` instances.

        '''
