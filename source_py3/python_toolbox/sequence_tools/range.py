import abc
import builtins
import types
import collections
import numbers

from python_toolbox import caching

infinity = float('inf')
infinities = (infinity, -infinity)
NoneType = type(None)


def parse_range_args(*args):
    assert 0 <= len(args) <= 3

    if len(args) == 0:
        return (0, infinity, 1)
    
    elif len(args) == 1:
        (stop,) = args
        if stop == -infinity: raise TypeError
        elif stop is None: stop = infinity
        return (0, stop, 1)
    
    elif len(args) == 2:
        (start, stop) = args
        
        if start in infinities: raise TypeError
        elif start is None: start = 0

        if stop == -infinity: raise TypeError
        elif stop is None: stop = infinity
        
        return (start, stop, 1)
    
    else:
        assert len(args) == 3
        (start, stop, step) = args
        
        if step == 0: raise TypeError

        if start in infinities: raise TypeError
        elif start is None: start = 0
        
        elif step > 0:
                
            if stop == -infinity: raise TypeError
            elif stop is None: stop = infinity
            
        else:
            assert step < 0
        
            if stop == infinity: raise TypeError
            elif stop is None: stop = (-infinity)
            
            
        return (start, stop, step)
    

def _is_integral_or_none(thing):
    return isinstance(thing, (numbers.Integral, NoneType))


class RangeType(abc.ABCMeta):
    '''Metaclass for `Range`, see its docstring for details.'''
    def __call__(cls, *args, _avoid_builtin_range=False):
        # Our job here is to decide whether to instantiate using the built-in
        # `range` or our kickass `Range`.
        from python_toolbox import math_tools
        
        if (cls is Range) and (not _avoid_builtin_range):
            start, stop, step = parse_range_args(*args)
            
            use_builtin_range = True # Until challenged.
            
            if not all(map(_is_integral_or_none, (start, stop, step))):
                # If any of `(start, stop, step)` are not integers or `None`, we
                # definitely need `Range`.
                use_builtin_range = False
                
            if (step > 0 and stop == infinity) or \
                                            (step < 0 and stop == (-infinity)):
                # If the range of numbers is infinite, we sure as shit need
                # `Range`.
                use_builtin_range = False
                    
            if use_builtin_range:
                return range(*args)
            else:
                return super().__call__(*args)
        
        else: # (cls is not Range) or _avoid_builtin_range
            return super().__call__(*args)
        

class Range(collections.Sequence, metaclass=RangeType):
    '''
    Improved version of Python's `range` that has extra features.
    
    `Range` is like Python's built-in `range`, except (1) it's with a capital R
    and (2) it's completely different. LOL, just kidding.
    
    
    '''
    def __init__(self, *args):
        self.start, self.stop, self.step = parse_range_args(*args)
        
    _reduced = property(lambda self: (type(self), (self.start, self.stop,
                                                   self.end)))
        
    __eq__ = lambda self, other: (isinstance(other, Range) and
                                  (self._reduced == other._reduced))
    
    distance_to_cover = caching.CachedProperty(lambda self:
                                                        self.stop - self.start)
    
    @caching.CachedProperty
    def length(self):
        from python_toolbox import math_tools
        
        if math_tools.get_sign(self.distance_to_cover) != \
                                                math_tools.get_sign(self.step):
            return 0
        else:
            raw_length, remainder = divmod(self.distance_to_cover, self.step)
            raw_length += (remainder != 0)
            return raw_length
    
    __repr__ = lambda self: self._repr
        
        
    @caching.CachedProperty
    def _repr(self):
        return '%s(%s%s%s)' % (
            type(self).__name__,
            '%s, ' % self.start,
            '%s' % self.stop, 
            (', %s' % self.step) if self.step != 1 else '',
        )
        
        
    
    def __getitem__(self, i):
        from python_toolbox import sequence_tools
        if isinstance(i, numbers.Integral):
            if 0 <= i < self.length:
                return self.start + (self.step * i)
            elif (-self.length) <= i < 0:
                return self.start + (self.step * (i + self.length))
            else:
                raise IndexError
        elif isinstance(i, (slice, sequence_tools.CanonicalSlice)):
            canonical_slice = sequence_tools.CanonicalSlice(
                i, iterable_or_length=self
            )
            if not (0 <= canonical_slice.start < self.length and
                    0 <= canonical_slice.stop < self.length):
                raise TypeError
            return Range(
                self[canonical_slice.start],
                self[canonical_slice.stop],
                self.step * canonical_slice.step
            )
        else:
            raise TypeError
        
    def __len__(self):
        # Sadly Python doesn't allow infinity here.
        return self.length if (self.length not in infinities) else 0
        
    def __contains__(self, i):
        try: self.index(i)
        except ValueError: return False
        else: return True
        
    def index(self, i):
        if not isinstance(i, numbers.Number):
            raise ValueError
        else:
            distance = i - self.start
            if math_tools.get_sign(distance) != math_tools.get_sign(self.step):
                raise ValueError
            index, remainder = divmod(distance, self.step)
            if remainder == 0:
                return index
            else:
                raise ValueError
        
    
Range.register(range)