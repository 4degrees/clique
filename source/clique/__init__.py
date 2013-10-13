# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import re
from collections import defaultdict

from ._version import __version__
from .collection import Collection
from .error import CollectionError


#: Pattern for matching an index with optional padding.
DIGITS_PATTERN = '(?P<index>(?P<padding>0*)\d+)'

_DIGITS_REGEX = re.compile(DIGITS_PATTERN)

#: Common patterns that can be passed to :py:func:`~clique.assemble`.
PATTERNS = {
    'frames': '\.{0}\.\D+\d?$'.format(DIGITS_PATTERN),
    'versions': 'v{0}'.format(DIGITS_PATTERN)
}


def assemble(iterable, patterns=None, minimum_items=2):
    '''Assemble items in *iterable* into discreet collections.

    *patterns* may be specified as a list of regular expressions to limit
    the returned collection possibilities. Use this when interested in
    collections that only match specific patterns. Each pattern must contain
    the expression from :py:data:`DIGITS_PATTERN` exactly once.

    A selection of common expressions are available in :py:data:`PATTERNS`.

    .. note::

        If a pattern is supplied as a string it will be automatically compiled
        to a :py:class:`re.RegexObject` instance for convenience.

    When *patterns* is not specified, collections are formed by examining all
    possible groupings of the items in *iterable* based around common numerical
    components.

    *minimum_items* dictates the minimum number of items a collection must have
    in order to be included in the result. The default is 2, filtering out
    single item collections.

    Return tuple of two lists (collections, remainder) where 'collections' is a
    list of assembled :py:class:`~clique.collection.Collection` instances and
    'remainder' is a list of items that did not belong to any collection.

    '''
    collection_map = defaultdict(set)
    collections = []
    remainder = []

    # Compile patterns.
    compiled_patterns = []

    if patterns is not None:
        if not patterns:
            return collections, list(iterable)

        for pattern in patterns:
            if isinstance(pattern, basestring):
                compiled_patterns.append(re.compile(pattern))
            else:
                compiled_patterns.append(pattern)

    else:
        compiled_patterns.append(_DIGITS_REGEX)

    # Process iterable.
    for item in iterable:
        matched = False

        for pattern in compiled_patterns:
            for match in pattern.finditer(item):
                index = match.group('index')

                head = item[:match.start('index')]
                tail = item[match.end('index'):]

                padding = match.group('padding')
                if padding:
                    padding = len(index)
                else:
                    padding = 0

                key = (head, tail, padding)
                collection_map[key].add(int(index))
                matched = True

        if not matched:
            remainder.append(item)

    # Form collections.
    merge_candidates = []
    for (head, tail, padding), indexes in collection_map.items():
            collection = Collection(head, tail, padding, indexes)
            collections.append(collection)

            if collection.padding == 0:
                merge_candidates.append(collection)

    # Merge together collections that align on padding boundaries. For example,
    # 0998-0999 and 1000-1001 can be merged into 0998-1001. Note that only
    # indexes within the padding width limit are merged. If a collection is
    # entirely merged into another then it will not be included as a separate
    # collection in the results.
    fully_merged = []
    for collection in collections:
        if collection.padding == 0:
            continue

        for candidate in merge_candidates:
            if (candidate.head == collection.head and
                candidate.tail == collection.tail):

                merged_index_count = 0
                for index in candidate.indexes:
                    if len(str(abs(index))) == collection.padding:
                        collection.indexes.add(index)
                        merged_index_count += 1

                if merged_index_count == len(candidate.indexes):
                    fully_merged.append(candidate)

    # Filter out fully merged collections.
    collections = [collection for collection in collections
                   if collection not in fully_merged]

    # Filter out collections that do not have at least as many indexes as
    # minimum_items. In addition, add any members of a filtered collection,
    # which are not members of an unfiltered collection, to the remainder.
    filtered = []
    remainder_candidates = []
    for collection in collections:
        if len(collection.indexes) >= minimum_items:
            filtered.append(collection)
        else:
            for member in collection:
                remainder_candidates.append(member)

    for candidate in remainder_candidates:
        has_membership = False

        for collection in filtered:
            if candidate in collection:
                has_membership = True
                break

        if not has_membership:
            remainder.append(candidate)

    return filtered, remainder


def parse(value, pattern='{head}{padding}{tail} [{ranges}]'):
    '''Parse *value* into a :py:class:`~clique.collection.Collection`.

    Use *pattern* to extract information from *value*. It may make use of the
    following keys:

        * *head* - Common leading part of the collection.
        * *tail* - Common trailing part of the collection.
        * *padding* - Padding value in ``%0d`` format.
        * *range* - Total range in the form ``start-end``
        * *ranges* - Comma separated ranges of indexes.
        * *holes* - Comma separated ranges of missing indexes.

    .. note::

        *holes* only makes sense if *range* or *ranges* is also present.

    '''
    # Construct regular expression for given pattern.
    expressions = {
        'head': '(?P<head>.*)',
        'tail': '(?P<tail>.*)',
        'padding': '%(?P<padding>\d*)d',
        'range': '(?P<range>\d+-\d+)',
        'ranges': '(?P<ranges>[\d ,\-]+)',
        'holes': '(?P<holes>[\d ,\-]+)'
    }

    pattern_regex = re.escape(pattern)
    for key, expression in expressions.items():
        pattern_regex = pattern_regex.replace(
            '\{{{0}\}}'.format(key),
            expression
        )
    pattern_regex = '^{0}$'.format(pattern_regex)

    # Match pattern against value and use results to construct collection.
    match = re.search(pattern_regex, value)
    if match is None:
        raise ValueError('Value did not match pattern.')

    groups = match.groupdict()
    if 'padding' in groups and groups['padding']:
        groups['padding'] = int(groups['padding'])
    else:
        groups['padding'] = 0

    # Create collection and then add indexes.
    collection = Collection(
        groups.get('head', ''),
        groups.get('tail', ''),
        groups['padding']
    )

    if 'range' in groups:
        start, end = map(int, groups['range'].split('-'))
        collection.indexes.update(range(start, end + 1))

    if 'ranges' in groups:
        parts = [part.strip() for part in groups['ranges'].split(',')]
        for part in parts:
            index_range = map(int, part.split('-', 2))

            if len(index_range) > 1:
                # Index range.
                for index in range(index_range[0], index_range[1] + 1):
                    collection.indexes.add(index)
            else:
                # Single index.
                collection.indexes.add(index_range[0])

    if 'holes' in groups:
        parts = [part.strip() for part in groups['holes'].split(',')]
        for part in parts:
            index_range = map(int, part.split('-', 2))

            if len(index_range) > 1:
                # Index range.
                for index in range(index_range[0], index_range[1] + 1):
                    collection.indexes.remove(index)
            else:
                # Single index.
                collection.indexes.remove(index_range[0])

    return collection
