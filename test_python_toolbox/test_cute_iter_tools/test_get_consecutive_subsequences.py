# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `cute_iter_tools.get_consecutive_subsequences`.'''

from python_toolbox import gc_tools
from python_toolbox import cute_testing
from python_toolbox import sequence_tools

from python_toolbox.cute_iter_tools import get_consecutive_subsequences


def test_length_2():
    
    # `get_consecutive_subsequences` returns an iterator, not a sequence:
    assert not sequence_tools.is_sequence(
        get_consecutive_subsequences(range(4))
    )
                                          
    assert tuple(get_consecutive_subsequences(range(4))) == \
           tuple(get_consecutive_subsequences(xrange(4))) == \
           ((0, 1), (1, 2), (2, 3))
                                          
    assert tuple(get_consecutive_subsequences(range(4), wrap_around=True)) == \
           tuple(get_consecutive_subsequences(xrange(4), wrap_around=True)) ==\
           ((0, 1), (1, 2), (2, 3), (3, 0))
                                          
    assert tuple(get_consecutive_subsequences('meow')) == \
           (('m', 'e'), ('e', 'o'), ('o', 'w'))
    
    
def test_iterable_too_short():
    with cute_testing.RaiseAssertor(NotImplementedError):
        tuple(get_consecutive_subsequences([1], wrap_around=True))
           
           
def test_various_lengths():
    assert tuple(get_consecutive_subsequences(xrange(7), length=3)) == \
                        ((0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6))
    assert tuple(get_consecutive_subsequences(xrange(7), length=4)) == \
                       ((0, 1, 2, 3), (1, 2, 3, 4), (2, 3, 4, 5), (3, 4, 5, 6))
    assert tuple(get_consecutive_subsequences(xrange(7), length=5)) == \
                            ((0, 1, 2, 3, 4), (1, 2, 3, 4, 5), (2, 3, 4, 5, 6))
    
    assert tuple(get_consecutive_subsequences(xrange(7), length=4,
            wrap_around=True)) == ((0, 1, 2, 3), (1, 2, 3, 4), (2, 3, 4, 5),
            (3, 4, 5, 6), (4, 5, 6, 0), (5, 6, 0, 1), (6, 0, 1, 2))
    assert tuple(get_consecutive_subsequences(xrange(7), length=5,
            wrap_around=True)) == ((0, 1, 2, 3, 4), (1, 2, 3, 4, 5),
            (2, 3, 4, 5, 6), (3, 4, 5, 6, 0), (4, 5, 6, 0, 1), (5, 6, 0, 1, 2),
            (6, 0, 1, 2, 3))
                                          
           
def test_garbage_collection():
    
    garbage_collected = set()

    class GarbageNoter(object):
        def __init__(self, n):
            assert isinstance(n, int)
            self.n = n
        def __del__(self):
            garbage_collected.add(self.n)
            
    iterable = (GarbageNoter(i) for i in xrange(7))
    
    consecutive_subsequences_iterator = \
                               get_consecutive_subsequences(iterable, length=3)
    
    def assert_garbage_collected(indexes):
        gc_tools.collect()
        assert set(indexes) == garbage_collected
        
    assert_garbage_collected(())
    next(consecutive_subsequences_iterator)
    assert_garbage_collected(())
    next(consecutive_subsequences_iterator)
    assert_garbage_collected((0,))
    next(consecutive_subsequences_iterator)
    assert_garbage_collected((0, 1))
    next(consecutive_subsequences_iterator)
    assert_garbage_collected((0, 1, 2))
    next(consecutive_subsequences_iterator)
    assert_garbage_collected((0, 1, 2, 3))
    with cute_testing.RaiseAssertor(StopIteration):
        next(consecutive_subsequences_iterator)
    assert_garbage_collected((0, 1, 2, 3, 4, 5, 6))
        
    
    
def test_garbage_collection_wrap_around():
    
    garbage_collected = set()

    class GarbageNoter(object):
        def __init__(self, n):
            assert isinstance(n, int)
            self.n = n
        def __del__(self):
            garbage_collected.add(self.n)
            
    iterable = (GarbageNoter(i) for i in xrange(7))
    
    consecutive_subsequences_iterator = \
             get_consecutive_subsequences(iterable, length=3, wrap_around=True)
    
    def assert_garbage_collected(indexes):
        gc_tools.collect()
        assert set(indexes) == garbage_collected
        
    assert_garbage_collected(())
    next(consecutive_subsequences_iterator)
    assert_garbage_collected(())
    next(consecutive_subsequences_iterator)
    assert_garbage_collected(())
    next(consecutive_subsequences_iterator)
    assert_garbage_collected(())
    next(consecutive_subsequences_iterator)
    assert_garbage_collected((2,))
    next(consecutive_subsequences_iterator)
    assert_garbage_collected((2, 3))
    next(consecutive_subsequences_iterator)
    assert_garbage_collected((2, 3, 4))
    next(consecutive_subsequences_iterator)
    assert_garbage_collected((2, 3, 4, 5))
    with cute_testing.RaiseAssertor(StopIteration):
        next(consecutive_subsequences_iterator)
    assert_garbage_collected((0, 1, 2, 3, 4, 5, 6))
        
    
    
    
            
            
    
            
            
    