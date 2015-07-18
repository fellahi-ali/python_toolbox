# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing

from python_toolbox.misc_tools import OverridableProperty


def test():
    class A(object):
        @OverridableProperty
        def meow(self):
            return 'bark bark!'
        
    a = A()
    assert a.meow == 'bark bark!'
    assert a.meow == 'bark bark!'
    assert a.meow == 'bark bark!'
    a.meow = 'Meow indeed, my love.'
    assert a.meow == 'Meow indeed, my love.'
            
            