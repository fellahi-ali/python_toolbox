# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
This module defines the AboutDialog class.

See its documentation for more info.
'''

import time
import webbrowser

import pkg_resources

import wx.html

import garlicsim_wx

from bitmap_viewer import BitmapViewer

from . import images as __images_package
images_package = __images_package.__name__


class AboutDialog(wx.Dialog):
    '''
    '''
    def __init__(self, frame):
   
        wx.Dialog.__init__(self, frame, title='About GarlicSim',
                           size=(628, 600))
        
        self.SetBackgroundColour(wx.Color(212, 208, 200))
        
        self.SetDoubleBuffered(True)
        
        self.frame = frame

        v_sizer = wx.BoxSizer(wx.VERTICAL)
        

        self._original_image = wx.ImageFromStream(
            pkg_resources.resource_stream(
                images_package,
                'about.png'
            )
        )
        
        self.static_bitmap = wx.StaticBitmap(
            self,
            -1,
            wx.BitmapFromImage(self._original_image)
        )
        v_sizer.Add(self.static_bitmap, 0)
        
        self.static_bitmap.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        
        
        self.html_window = wx.html.HtmlWindow(self, size=(628, 270))
        v_sizer.Add(self.html_window, 0)
        
        self.html_window.SetPage(
            '''
            <html>
                <body bgcolor="#d4d0c8">
                    <div align="center"> <font size="1">
                        &copy; 2009-2010 Ram Rachum (a.k.a. cool-RR)
                        <br />                        
                        No part of this program may be used, copied or
                        distributed without explicit written permission from Ram
                        Rachum.
                        <br />
                    </font></div>
                    <div> 
                        GarlicSim is a platform for writing, running and
                        analyzing computer simulations. It is general enough to
                        handle any kind of simulation: Physics, game theory,
                        epidemic spread, electronics, etc.<br />
                        <font size="1"><br /></font>
                        <b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Version %s</b>
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Website:
                        <a href="http://garlicsim.org">http://garlicsim.org</a>
                    </div>
                    <div>
                        <font size="1"><br /></font>
                        I would like to thank the open source community for
                        making this program possible. This includes the
                        developers of Python, Psyco, wxPython, wxWidgets,
                        Mayavi, git, and so many others... And more thanks to
                        the many people who spent many hours helping me out
                        with various issues, on mailing lists such as
                        wxpython-users and on the StackOverflow website.
                    </div>
                </body>
            </html>
            ''' % garlicsim_wx.__version__
        )
        
        self.html_window.Bind(
            wx.html.EVT_HTML_LINK_CLICKED, 
            lambda event: webbrowser.open_new_tab(
                event.GetLinkInfo().GetHref()
                ),
            self.html_window
        )

        
        self.button_sizer = button_sizer = wx.StdDialogButtonSizer()
        self.ok_button = wx.Button(self, wx.ID_OK,
                                   "Let's get back to simulating!")
        self.ok_button.SetDefault()
        button_sizer.SetAffirmativeButton(self.ok_button)
        self.Bind(wx.EVT_BUTTON, self.on_ok, self.ok_button)
        button_sizer.AddButton(self.ok_button)
        button_sizer.Realize()
        button_sizer.SetMinSize((500, -1))
        v_sizer.Add(button_sizer, 0)
        
        
        self.SetSizer(v_sizer)
        self.Layout()

        
        self.timer = wx.Timer(self)
        self.timer.Start(40)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        
        self._rotate_image_hue()

        
    def on_ok(self, e=None):
        '''Do 'Okay' on the dialog.'''

        self.EndModal(wx.ID_OK)

        
    def on_timer(self, event):
        self._rotate_image_hue()

        
    def _rotate_image_hue(self):
        new_image = self._original_image.Copy()
        t = time.time()
        new_image.RotateHue((t / 50.) % 1)
        self.static_bitmap.SetBitmap(wx.BitmapFromImage(new_image))

        
    def EndModal(self, *args, **kwargs):
        self.timer.Stop()
        wx.Dialog.EndModal(self, *args, **kwargs)

        
        