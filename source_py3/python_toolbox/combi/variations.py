from python_toolbox import cute_iter_tools
from python_toolbox import nifty_collections
from python_toolbox import caching
from python_toolbox.third_party import sortedcontainers

from .selection_space import SelectionSpace


class UnsupportedVariationCombinationException(Exception):
    '''blocktodo use everywhere
    let it take variations
    make variation classes mostly for this and testing'''
    

class Variation(nifty_collections.CuteEnum):
    RAPPLIED = 'rapplied'
    RECURRENT = 'recurrent'
    PARTIAL = 'partial'
    COMBINATION = 'combination'
    DAPPLIED = 'dapplied'
    FIXED = 'fixed'
    DEGREED = 'degreed'
    SLICED = 'sliced'
    
        
variation_clashes = (
    {Variation.DEGREED: True, Variation.COMBINATION: True,},
    {Variation.DEGREED: True, Variation.PARTIAL: True,},
    {Variation.DEGREED: True, Variation.RECURRENT: True,},
    {Variation.COMBINATION: True, Variation.FIXED: True,},
    {Variation.RAPPLIED: False, Variation.RECURRENT: True,},
)


class VariationSelectionSpace(SelectionSpace):
    def __init__(self):
        SelectionSpace.__init__(self, Variation)
        
    @caching.cache()
    def __getitem__(self, i):
        return VariationSelection(SelectionSpace.__getitem__(self, i))
        
    def index(self, variation_selection):
        return super().index(variation_selection.variations)
        
    @caching.cache()
    def __repr__(self):
        return '<VariationSelectionSpace>'
    
        
class VariationSelectionType(type):
    __call__ = lambda cls, variations: cls._create_from_tuple(
                                           cls, tuple(sorted(set(variations))))
    
class VariationSelection(metaclass=VariationSelectionType):
    __call__ = classmethod(
        lambda cls, variations: cls._create_from_tuple(
                                           cls, tuple(sorted(set(variations))))
    )
    @caching.cache()
    def _create_from_tuple(cls, variations):
        # This method exsits so we could cache canonically. The `__new__`
        # method canonicalizes the `variations` argument and we cache according
        # to it.
        variation_selection = super().__new__(cls)
        variation_selection.__init__(variations)
        return variation_selection
        
    def __init__(self, variations):
        self.variations = variations
        assert cute_iter_tools.is_sorted(self.variations)
        self.is_rapplied = Variation.RAPPLIED in self.variations
        self.is_recurrent = Variation.RECURRENT in self.variations
        self.is_partial = Variation.PARTIAL in self.variations
        self.is_combination = Variation.COMBINATION in self.variations
        self.is_dapplied = Variation.DAPPLIED in self.variations
        self.is_fixed = Variation.FIXED in self.variations
        self.is_degreed = Variation.DEGREED in self.variations
        self.is_sliced = Variation.SLICED in self.variations
        
    @caching.cache()
    def __repr__(self):
        return '<%s: %s>' % (
            type(self).__name__,
            ', '.join(variation.value for variation in self.variations)
        )
    
    @caching.CachedProperty
    def is_allowed(self):
        _variations_set = set(self.variations)
        for variation_clash in variation_clashes:
            for variation, included in variation_clash.items():
                if (variation in _variations_set) != included:
                    continue
            else:
                return False
        else:
            return True
    
     
variation_selection_space = VariationSelectionSpace()
variation_selection_space[7].is_allowed
tuple(variation_selection_space)
repr(variation_selection_space[7])