# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
This module defines the FlagRaiser class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.general_misc import cute_timer


class FlagRaiser(object): # todo: rename?
    '''When called, raises a flag of a window and then calls some function.'''
    def __init__(self, window, attribute_name=None, function=None, delay=None):
        '''
        Construct the flag raiser.
        
        `window` is the window we're acting on. `attribute_name` is the name of
        the flag that we set to True. `function` is the function we call after
        we set the flag. Default for `function` is `window.Refresh`.
        
        If we get a `delay` argument, then we don't call the function
        immediately, but wait for `delay` time, specified as seconds, then call
        it. If this flag raiser will be called again while the timer's on, it
        will not cause another function calling.
        '''
        assert isinstance(window, wx.Window)

        self.window = window
        '''The window that the flag raiser is acting on.'''
        
        self.attribute_name = attribute_name
        '''The name of the flag that this flag raiser raises.'''
        
        self.function = function or window.Refresh
        '''The function that this flag raiser calls after raising the flag.'''
        
        self.delay = delay
        '''The delay, in seconds, that we wait before calling the function.'''
        
        if delay is not None:
            
            self._delay_in_ms = delay * 1000
            '''The delay in milliseconds.'''
            
            self.timer = cute_timer.CuteTimer(self.window)
            '''The timer we use to call the function.'''
            
            self.timer.Bind(wx.EVT_TIMER, self.on_timer, self.timer)

            
    def __call__(self):
        '''Raise the flag and call the function. (With delay if we set one.)'''
        if self.attribute_name:
            setattr(self.window, self.attribute_name, True)
        if self.delay is None:
            self.function()
        else: # self.delay is a positive number
            if not self.timer.IsRunning():
                self.timer.Start(self._delay_in_ms, oneShot=True)
                
    def on_timer(self, event):
        '''EVT_TIMER event handler.'''
        if getattr(self.window, self.attribute_name) is True:
            self.function()