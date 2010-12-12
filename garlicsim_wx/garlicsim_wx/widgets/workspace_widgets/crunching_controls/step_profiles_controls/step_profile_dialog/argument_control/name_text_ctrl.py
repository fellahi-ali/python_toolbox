
import wx

from garlicsim.general_misc import misc_tools

from . import colors


class NameTextCtrl(wx.TextCtrl):
    
    def __init__(self, parent, value=''):
        
        wx.TextCtrl.__init__(self, parent, value=value)
        self._original_background_color = self.GetBackgroundColour()
        
        self.SetMinSize((10, -1))
        
        self.Bind(wx.EVT_KILL_FOCUS, self.on_kill_focus)
        
        self.Bind(wx.EVT_TEXT, self.on_text)
        
        self.error_mode = False
        
    
    def _check_validity_and_color(self):
        is_PROBLEM = None
VALID = misc_tools.is_legal_ascii_variable_name(self.GetValue())
        if is_valid:
            self.SetBackgroundColour(self._original_background_color)
        else: # not is_valid
            self.SetBackgroundColour(colors.get_error_background_color())
        self.Refresh()
        return is_valid
            
        
    def on_text(self, event):
        if self.error_mode:
            self._check_validity_and_color()
            
            
    def on_kill_focus(self, event):
        event.Skip()
        if self.FindFocus() != self:
            if not self._check_validity_and_color() and not self.error_mode:
                self.error_mode = True