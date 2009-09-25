# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
This module defines the SimpackGrokker class. See its documentation for more
details.
"""

import functools

from step_function_manipulators import \
     simple_history_step_from_step_generator, \
     simple_non_history_step_from_step_generator, \
     non_history_step_generator_from_simple_step, \
     history_step_generator_from_simple_step

#__all__ = ["SimpackGrokker"]

class InvalidSimpack(Exception):
    """
    An exception to raise when trying to load an invalid simpack.
    """
    pass

class SimpackGrokker(object):
    """
    An object that encapsulates a simpack, giving useful information about it
    and tools to use with it.
    """
    def __init__(self, simpack):
        self.simpack = simpack
        
        self.simple_non_history_step_defined = hasattr(simpack, "step")
        self.non_history_step_generator_defined = \
            hasattr(simpack, "step_generator")
        self.simple_history_step_defined = hasattr(simpack, "history_step")
        self.history_step_generator_defined = hasattr(simpack,
                                                      "history_step_generator")
        
        self.non_history_step_defined = \
            (self.simple_non_history_step_defined or \
             self.non_history_step_generator_defined)
        
        self.history_step_defined = (self.simple_history_step_defined or \
                                     self.history_step_generator_defined)
        
        self.simple_step_defined = (self.simple_non_history_step_defined or \
                                    self.simple_history_step_defined)
        
        self.step_generator_defined = \
            (self.non_history_step_generator_defined or \
             self.history_step_generator_defined)
        
        if self.history_step_defined and self.non_history_step_defined:
            raise StandardError("""The simulation package is defining both a \
            history-dependent step and a non-history-dependent step - That's \
            forbidden!""")
        
        assert self.simple_step_defined or self.step_generator_defined
        
        self.history_dependent = self.history_step_defined
        
        self.__init_step()
        self.step.history_dependent = self.history_step_defined
        
        self.__init_step_generator()
    
    def __init_step_generator(self):
        
        if self.step_generator_defined:
            """
            The simpack supplies a step generator, so we're gonna use that.
            """
            if self.history_step_defined:
                self.step_generator = self.simpack.history_step_generator
                return
            else: # It's a non-history simpack
                self.step_generator = self.simpack.step_generator
                return
                
        else:
            """
            The simpack supplied no step generator, only a simple step, so
            we're gonna make a generator that uses it.
            Remember, self.step is pointing to our simple step function,
            whether it's history-dependent or not, so we're gonna use self.step
            in our generator.
            """
            if self.history_step_defined:               
                        
                self.step_generator = functools.partial \
                    (history_step_generator_from_simple_step, self.step)
                return
                
    
            else: # It's a non-history simpack
                
                self.step_generator = functools.partial \
                    (non_history_step_generator_from_simple_step, self.step)
                return
                
        
    def step_generator(self, old_state_or_history_browser, *args, **kwargs):
        raise NotImplementedError
    
    def __init_step(self):
        if self.simple_step_defined:
            """
            If the simpack defines a simple step, we'll just point to that.
            """
            if self.history_dependent:
                self.step = self.simpack.history_step
                return
            else: # It's non-history dependent
                self.step = self.simpack.step
                return
                
        else:
            if self.history_dependent:
                
                self.step = functools.partial \
                    (simple_history_step_from_step_generator,
                     self.simpack.history_step_generator)
                return
                    
            else: # It's non-history dependent
                
                self.step = functools.partial \
                    (simple_non_history_step_from_step_generator,
                     self.simpack.step_generator)
                return
        
        
    def step(self, old_state_or_history_browser, *args, **kwargs):
        raise NotImplementedError
    