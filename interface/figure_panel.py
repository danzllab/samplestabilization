import wx
from wx.lib import plot as wxplot
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas  # type: ignore
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np


class Figure_Panel(wx.Panel):
    """A wxPython panel that integrates matplotlib figures for real-time plotting of data.

    This class provides a graphical interface for displaying and dynamically updating plots of data such as positions and errors. 
    It includes capabilities for efficient redrawing using blitting for improved performance during updates.

    Attributes:
        figPanel (wx.Panel): Self reference for the figure panel.
        figure (Figure): Matplotlib figure object for plotting.
        ax (list): List of matplotlib axes objects.
        lines (list): List of line objects currently being plotted.
        canvas (FigureCanvas): Canvas on which the figure is drawn.
        background (list): List of backgrounds for blitting to improve redraw performance.
        
    """

    def __init__(self, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)
        self.figPanel = self
        self.figure = Figure(figsize=(4, 1.5), dpi=100, layout=None)
        self.ax = [self.figure.add_subplot(2, 1, 1), self.figure.add_subplot(2, 1, 2)]
        self.lines = []
        

        self.clear()

        self.canvas = FigureCanvas(self, -1, self.figure)
        # Init bliting
        self.update_background()

        # self.figure.tight_layout()
        
        # self.enlarged_canvas = FigureCanvas(self,-1,self.enlarged_figure)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.Bind(wx.EVT_SIZE, self.on_resize)
        # added wx.EXPAND so that the canvas can stretch vertically
        sizer.Add(self.canvas, 1, wx.ALL | wx.EXPAND, 0)
        self.SetSizer(sizer)
        self.Layout()
        self.Fit()

    def blit(self):
        """Blits the drawn area only, for fast updating of the plots without needing to redraw all elements."""
        
        for i in range(2):
            self.canvas.restore_region(self.background[i])
            self.ax[i].draw_artist(self.lines[i])
            self.canvas.blit(self.ax[i].bbox)

    def update(self, pos, err):
        """Update the plot data, adjusting axes limits if necessary, and trigger a redraw if needed.

        Args:
            pos (np.ndarray): Numpy array of position data.
            err (np.ndarray): Numpy array of error data.
        """

        redraw = False

        t = pos[:,0]
        idx_mid = None

        xmin, xmax = self.ax[0].get_xlim()


        if np.min(t) > xmin or np.max(t) > xmax:
            dt = t[1]-t[0]
            idx_mid = int(len(t)/2)
            mid = t[idx_mid]
            last = mid + 2*idx_mid*dt

            self.ax[0].set_xlim(mid, last)
            self.ax[1].set_xlim(mid, last)
            redraw = True

        # if np.min(t) > xmin:
        #     self.ax[0].set_xlim(np.min(t), np.max(t) + t[9]-t[0])
        #     self.ax[1].set_xlim(np.min(t), np.max(t) + t[9]-t[0])
        #     redraw = True
        
        
        for idx, data in enumerate([pos, err]):
            
            x = data[:,0] if idx_mid is None else data[idx_mid:,0]
            y = data[:,1] if idx_mid is None else data[idx_mid:,1]
            self.lines[idx].set_xdata(x)
            self.lines[idx].set_ydata(y)

            ymin, ymax = self.ax[idx].get_ylim()

            np_min = np.min(y)
            np_max = np.max(y)
            ampl = np_max-np_min

            if np_min < ymin or np_max > ymax:
                if np_min != np_max:
                    self.ax[idx].set_ylim(np_min - 0.1*np.abs(ampl), np.max(y) + 0.1*np.abs(ampl))
                else:
                    self.ax[idx].set_ylim(np_min - 0.01, np_max + 0.01)
                redraw = True

            if np_min > ymin + 0.1*np.abs(ampl) or np_max < ymax - 0.1*np.abs(ampl):
                self.ax[idx].set_ylim(np_min - 0.1*np.abs(ampl), np_max + 0.1*np.abs(ampl))
                redraw = True

        if redraw:
            self.redraw()
        self.blit()
        # else:
        #     self.blit()
        
            
    def draw(self, pos=None, err=None):
        """Draw new data on the plots.

        Args:
            pos (np.ndarray, optional): Numpy array of position data.
            err (np.ndarray, optional): Numpy array of error data.
        """

        if pos is not None and err is not None:
            self.update(pos, err)


    def redraw(self):
        """Redraws the entire canvas, a more resource-intensive operation used when necessary."""
        
        self.figure.canvas.draw()
        self.update_background()

    def update_background(self):
        """Update the stored background for blitting, to be called after any redraw."""
        
        self.background = [self.canvas.copy_from_bbox(ax.bbox) for ax in self.ax]

    def on_resize(self, event):
        """Handles resizing of the panel, updating canvas size and forcing a redraw.

        Args:
            event (wx.Event): Event object from the resize event.
        """

        event.Skip()
        self.canvas.SetSize(self.GetSize())
        self.redraw()
        self.Layout()
        self.Refresh()

    def clear(self):
        """Clears the plots, resetting them to a blank state with default settings."""
        
        x = np.linspace(0, 0.1, 1)
        b= 0
        col = 'blue'
        labels = ['Position (um)', 'Error']
        
        for axes in self.ax:
            axes.cla()
            axes.set_ylim(- 0.001, 0.001)
            axes.set_xlim(0, 10)
            for label in (axes.get_xticklabels() + axes.get_yticklabels()):
                label.set_fontsize(6)
            line = axes.plot(x, 0.001*np.sin(x*2*np.pi + b), color=col)[0]
            self.lines.append(line)
            axes.grid()
            # axes.set_xlabel('Time (s)')
            axes.set_ylabel(labels.pop(0))
            b += np.pi/2
            col = 'red'
        
        self.ax[1].set_xlabel('Time (s)')





        




# class Figure_Panel(wx.Panel):
#     def __init__(self, *args, **kw):
#         wx.Panel.__init__(self, *args, **kw)

#         mainSizer = wx.BoxSizer(wx.VERTICAL)

#         self.pos_canvas = wxplot.PlotCanvas(self)
#         self.reset_defaults(canvas=self.pos_canvas)
#         self.err_canvas = wxplot.PlotCanvas(self)
#         self.reset_defaults(canvas=self.err_canvas)
#         # self.reset_defaults()

#         mainSizer.Add(self.pos_canvas, 1, wx.EXPAND)
#         mainSizer.Add(self.err_canvas, 1, wx.EXPAND)
#         self.SetSizer(mainSizer)
#         # self.pos_canvas.Draw(self.drawBarGraph())
#         # self.err_canvas.Draw(self.drawBarGraph())
        
#     def drawBarGraph(self):
#         # Bar graph
#         points1=[(1,0), (1,10)]
#         line1 = wxplot.PolyLine(points1, colour='green', legend='Feb.', width=10)
#         points1g=[(2,0), (2,4)]
#         line1g = wxplot.PolyLine(points1g, colour='red', legend='Mar.', width=10)
#         points1b=[(3,0), (3,6)]
#         line1b = wxplot.PolyLine(points1b, colour='blue', legend='Apr.', width=10)

#         points2=[(4,0), (4,12)]
#         line2 = wxplot.PolyLine(points2, colour='Yellow', legend='May', width=10)
#         points2g=[(5,0), (5,8)]
#         line2g = wxplot.PolyLine(points2g, colour='orange', legend='June', width=10)
#         points2b=[(6,0), (6,4)]
#         line2b = wxplot.PolyLine(points2b, colour='brown', legend='July', width=10)

#         return wxplot.PlotGraphics([line1, line1g, line1b, line2, line2g, line2b],
#                             "", "Months", 
#                             "Number of Students")

#     def draw(self, canvas=None, xlim = (0, 10), title='', xlabel = 'Time', ylabel = 'Axis', ylim = (0,10), colour = 'red', data=None):
#         # self.reset_defaults(canvas=canvas)

#         if data is not None:
#             line = wxplot.PolyLine(data, colour=colour, width=2)
#             pg = wxplot.PlotGraphics([line], title, xlabel, ylabel)
#             canvas.Draw(pg, xAxis=xlim, yAxis=ylim)

#     def reset_defaults(self, canvas=None):
#         if canvas is not None:
#             canvas.SetFont(wx.Font(10,
#                                    wx.FONTFAMILY_SWISS,
#                                    wx.FONTSTYLE_NORMAL,
#                                    wx.FONTWEIGHT_NORMAL)
#                            )
#             canvas.fontSizeAxis = 10
#             canvas.fontSizeLegend = 7
#             # canvas.useScientificNotation = True
#             canvas.logScale = (False, False)
#             canvas.xSpec = 'auto'
#             canvas.ySpec = 'auto'

#     def draw_point_label(self, dc, mDataDict):
#         """
#         This is the function that defines how the pointLabels are plotted

#         :param dc: DC that will be passed
#         :param mDataDict: Dictionary of data that you want to use
#                           for the pointLabel

#         As an example I have decided I want a box at the curve point
#         with some text information about the curve plotted below.
#         Any wxDC method can be used.

#         """
#         dc.SetPen(wx.Pen(wx.BLACK))
#         dc.SetBrush(wx.Brush(wx.BLACK, wx.BRUSHSTYLE_SOLID))

#         sx, sy = mDataDict["scaledXY"]  # scaled x,y of closest point
#         # 10by10 square centered on point
#         dc.DrawRectangle(int(sx - 5), int(sy - 5), 1000, 10000)
#         px, py = mDataDict["pointXY"]
#         cNum = mDataDict["curveNum"]
#         pntIn = mDataDict["pIndex"]
#         legend = mDataDict["legend"]
#         # make a string to display
#         s = "Crv# %i, '%s', Pt. (%.2f,%.2f), PtInd %i" % (
#             cNum, legend, px, py, pntIn)
#         dc.DrawText(s, int(sx), int(sy + 1))


# class FigurePanel(wx.Panel):
# 	def __init__(self, *args, **kw):
# 		wx.Panel.__init__(self, *args, **kw)
# 		self.figPanel = self
# 		# self.sizer = wx.BoxSizer(wx.VERTICAL)
# 		# self.figure = Figure(figsize = (8,6.1), dpi =60)
# 		self.figure = Figure(figsize = (6.5,2.5), dpi =100)
# 		self.axes = self.figure.add_subplot()
# 		# self.ax.plot([1,2,3],[1,2,3])
# 		# self.enlarged_figure = Figure(figsize = (8,6.1), dpi = 60)
# 		# self.ax1 = self.enlarged_figure.add_subplot(2,1,1)
# 		# self.ax2 = self.enlarged_figure.add_subplot(2,1,2)
# 		# self.ax1.plot([1,2,3],[1,4,9])
# 		# self.ax2.plot([1,2,3],[1,4,9])
# 		self.canvas = FigureCanvas(self, -1, self.figure)
# 		# self.enlarged_canvas = FigureCanvas(self,-1,self.enlarged_figure)
# 		self.Layout()
# 		self.Fit()


# class HistPanel(wx.Panel):
# 	def __init__(self, *args, **kw):
# 		wx.Panel.__init__(self, *args, **kw)
# 		self.figPanel = self
# 		self.figure = Figure(figsize = (3,1.5), dpi =100)
# 		self.axes = self.figure.add_subplot()
# 		self.axes.set_ylim(0,1)
# 		self.axes.set_xlim(0,2)

# 		for label in (self.axes.get_xticklabels() + self.axes.get_yticklabels()):
# 			label.set_fontsize(6)

# 		self.figure.tight_layout()
# 		self.canvas = FigureCanvas(self, -1, self.figure)
# 		# self.enlarged_canvas = FigureCanvas(self,-1,self.enlarged_figure)
# 		sizer = wx.BoxSizer(wx.HORIZONTAL)
# 		# added wx.EXPAND so that the canvas can stretch vertically
# 		sizer.Add(self.canvas, 1, wx.ALL|wx.EXPAND, 0)
# 		self.SetSizer(sizer)
# 		self.Layout()
# 		self.Fit()
