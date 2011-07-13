# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `NameDisplay` class.

See its documentation for more information.
'''

import wx

from garlicsim_wx.widgets.general_misc.cute_static_text import CuteStaticText



class NameDisplay(CuteStaticText):
    def __init__(self, simpack_info_panel):
        ''' '''
        self.simpack_info_panel = simpack_info_panel
        CuteStaticText.__init__(self, simpack_info_panel)
        self.HelpText = "The currently-selected simpack's name."
        self.SetFont(wx.Font(24, wx.NORMAL, wx.NORMAL, wx.NORMAL))
        
    def refresh(self):
        simpack_metadata = self.simpack_info_panel.\
                                      simpack_selection_dialog.simpack_metadata
        self.SetLabel(simpack_metadata.name if simpack_metadata is not None
                      else '')
        