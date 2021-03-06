#!/usr/bin/env python
"""
Copyright (C) 2003-2004 Andrew Straw, Jeremy O'Donoghue and others
 
License: This work is licensed under the PSF. A copy should be included
with this source code, and is also available at
http://www.python.org/psf/license.html

This is yet another example of using matplotlib with wx.  Hopefully
this is pretty full-featured:

  - both matplotlib toolbar and WX buttons manipulate plot
  - full wxApp framework, including widget interaction
  - XRC (XML wxWidgets resource) file to create GUI (made with XRCed)

This was derived from embedding_in_wx and dynamic_image_wxagg.

Thanks to matplotlib and wx teams for creating such great software!

"""
import sys, time, os, gc
import matplotlib
matplotlib.use('WXAgg')
# some of this code is numarray dependent
matplotlib.rcParams['numerix'] = 'numarray'  
import matplotlib.cm as cm
from matplotlib.backends.backend_wxagg import Toolbar, FigureCanvasWxAgg
from matplotlib.figure import Figure
import matplotlib.numerix as numerix
from matplotlib.mlab import meshgrid

from wxPython.wx import *
from wxPython.xrc import *

ERR_TOL = 1e-5 # floating point slop for peak-detection


matplotlib.rc('image', origin='lower')

class PlotPanel(wxPanel):

    def __init__(self, parent):
        wxPanel.__init__(self, parent, -1)

        self.fig = Figure((5,4), 75)
        self.canvas = FigureCanvasWxAgg(self, -1, self.fig)
        self.toolbar = Toolbar(self.canvas) #matplotlib toolbar
        self.toolbar.Realize()
        #self.toolbar.set_active([0,1])

        # Now put all into a sizer
        sizer = wxBoxSizer(wxVERTICAL)
        # This way of adding to sizer allows resizing
        sizer.Add(self.canvas, 1, wxLEFT|wxTOP|wxGROW)
        # Best to allow the toolbar to resize!
        sizer.Add(self.toolbar, 0, wxGROW)
        self.SetSizer(sizer)
        self.Fit()

    def init_plot_data(self):
        a = self.fig.add_subplot(111)
        
        x = numerix.arange(120.0)*2*numerix.pi/60.0
        y = numerix.arange(100.0)*2*numerix.pi/50.0
        self.x, self.y = meshgrid(x, y)
        z = numerix.sin(self.x) + numerix.cos(self.y)
        self.im = a.imshow( z, cmap=cm.jet)#, interpolation='nearest')
        
        zmax = numerix.max(numerix.max(z))-ERR_TOL
        
        ymax_i, xmax_i = numerix.nonzero(
            numerix.greater_equal(z, zmax))
        if self.im.origin == 'upper':
            ymax_i = z.shape[0]-ymax_i
        self.lines = a.plot(xmax_i,ymax_i,'ko')

        self.toolbar.update() # Not sure why this is needed - ADS

    def GetToolBar(self):
        # You will need to override GetToolBar if you are using an 
        # unmanaged toolbar in your frame
        return self.toolbar
		
    def OnWhiz(self,evt):
        self.x += numerix.pi/15
        self.y += numerix.pi/20
        z = numerix.sin(self.x) + numerix.cos(self.y)
        self.im.set_array(z)

        zmax = numerix.max(numerix.max(z))-ERR_TOL
        ymax_i, xmax_i = numerix.nonzero(
            numerix.greater_equal(z, zmax))
        if self.im.origin == 'upper':
            ymax_i = z.shape[0]-ymax_i
        self.lines[0].set_data(xmax_i,ymax_i)

        self.canvas.draw()
        
    def onEraseBackground(self, evt):
        # this is supposed to prevent redraw flicker on some X servers...
        pass

class MyApp(wxApp):
    def OnInit(self):
        self.res = wxXmlResource("data/embedding_in_wx3.xrc")

        # main frame and panel ---------

        self.frame = self.res.LoadFrame(None,"MainFrame")
        self.panel = XRCCTRL(self.frame,"MainPanel")

        # matplotlib panel -------------

        # container for matplotlib panel (I like to make a container
        # panel for our panel so I know where it'll go when in XRCed.)
        plot_container = XRCCTRL(self.frame,"plot_container_panel")
        sizer = wxBoxSizer(wxVERTICAL)
        
        # matplotlib panel itself
        self.plotpanel = PlotPanel(plot_container)
        self.plotpanel.init_plot_data()

        # wx boilerplate
        sizer.Add(self.plotpanel, 1, wxEXPAND)
        plot_container.SetSizer(sizer)

        # whiz button ------------------

        whiz_button = XRCCTRL(self.frame,"whiz_button")
        EVT_BUTTON(whiz_button, whiz_button.GetId(),
                   self.plotpanel.OnWhiz)
  
        # bang button ------------------

        bang_button = XRCCTRL(self.frame,"bang_button")
        EVT_BUTTON(bang_button, bang_button.GetId(),
                   self.OnBang)
  
        # final setup ------------------
        
        sizer = self.panel.GetSizer()
        self.frame.Show(1)

        self.SetTopWindow(self.frame)

        return True
        
    def OnBang(self,event):
        bang_count = XRCCTRL(self.frame,"bang_count")
        bangs = bang_count.GetValue()
        bangs = int(bangs)+1
        bang_count.SetValue(str(bangs))
        
if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()

