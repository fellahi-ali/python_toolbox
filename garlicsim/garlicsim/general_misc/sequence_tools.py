


def heads(sequence, include_empty=False, include_full=True):    
    for i in range(0 if include_empty else 1, len(sequence)):
        yield sequence[:i]
    if include_full:
        yield sequence[:]
        
def are_equal_regardless_of_order(seq1, seq2):
    # Will fail for items that have problems with comparing
    return sorted(seq1) == sorted(seq2)
        

def flatten(iterable):
    iterator = iter(iterable)
    try:
        first_item = iterator.next()
    except StopIteration:
        return []
    return sum(iterator, first_item)


#def is_sequence(thing):
    #return hasattr(thing, '__len__') and hasattr(thing, '__getitem__') and hasattr(thing, '__iter__') and 
    #pass