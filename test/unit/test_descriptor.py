# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import pytest

import clique.descriptor


class Mock(object):
    '''Mock class for test.'''

    x = clique.descriptor.Unsettable('x')


def test_unsettable():
    '''Unsettable descriptor prevent standard setting of attribute.'''
    instance = Mock()
    assert instance.x is None

    instance.__dict__['x'] = True
    assert instance.x is True

    with pytest.raises(AttributeError):
        instance.x = False
