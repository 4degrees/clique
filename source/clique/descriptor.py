# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.


class ReadOnly(object):
    '''Read-only descriptor.'''

    def __init__(self, label):
        '''Initialise descriptor with property *label*.

        *label* should match the name of the property being described::

            x = ReadOnly('x')

        '''
        self.label = label
        super(ReadOnly, self).__init__()

    def __get__(self, instance, owner):
        '''Return value of property for *instance*.'''
        if instance is None:
            return self

        return instance.__dict__.get(self.label)

    def __set__(self, instance, value):
        '''Set *value* for *instance* property.'''
        raise AttributeError('Cannot set read-only attribute.')

