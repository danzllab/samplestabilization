import wx
import time
import cv2

import logging
logger = logging.getLogger(__name__)


WIDTH = 640
HEIGHT = 480
DEFAULT_BACKGROUND_COLOR = wx.BLACK


class ImageView(wx.Panel):
    """
    A panel for displaying images within a wxPython application, with capabilities for dynamic resizing,
    image updates, and basic interaction handling.

    Attributes:
        parent (wx.Window): The parent window for this panel.
        resize (bool): If True, allows dynamic resizing of images to fit the panel.
        size (tuple): Initial size of the panel.
        black (bool): If True, sets the panel background to black.
        style (int): Style flags for the wx.Panel.
    """

    def __init__(
        self,
        parent: wx.Window,
        resize: bool = True,
        size=(-1, -1),
        black: bool = False,
        style: int = wx.NO_BORDER,
    ):
        wx.Panel.__init__(self, parent, size=(-1, -1), style=style)

        self.x_offset = 0
        self.y_offset = 0
        self.fps = 0
        self.time_start = time.time()
        # self.dc = wx.BufferedPaintDC(self)

        self.default_image = wx.Image(WIDTH, HEIGHT, clear=True)
        self.image = self.default_image
        self.image_size = self.image.GetSize()
        self.best_size = self.get_best_size()
        # self.bitmap = wx.BitmapFromImage(self.default_image)
        self.bitmap = wx.Bitmap(self.default_image)

        if black:
            self.SetBackgroundColour(DEFAULT_BACKGROUND_COLOR)

        self.backBrush = wx.Brush(DEFAULT_BACKGROUND_COLOR, wx.SOLID)

        # self.SetDoubleBuffered(True)  # This is the key to stop flicker (!!!)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background) # Second solution to stop flicker (!!!)

        self.Bind(wx.EVT_SHOW, self.on_show)
        self.Bind(wx.EVT_PAINT, self.on_paint)

        # self.timer = wx.Timer(self)
        # self.Bind(wx.EVT_TIMER, self.on_paint)

        if resize:
            self.Bind(wx.EVT_SIZE, self.on_resize)

        self.hide = False
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_enter)

    def on_erase_background(self, event): # Second solution to stop flicker (!!!)
        """Overrides the background erase event to prevent flickering."""
        pass # Second solution to stop flicker (!!!)

    def on_enter(self, event):
        """Handles mouse entering the panel by changing the cursor to a hand.

        Args:
            event (wx.Event): The event instance triggered on cursor enter.
        """
        self.SetCursor(wx.Cursor(wx.CURSOR_HAND))

    def on_show(self, event):
        """Adjust layout on visibility changes.

        Args:
            event (wx.ShowEvent): Event triggered when the panel's visibility changes.
        """

        if event.IsShown():
            self.GetParent().Layout()
            self.Layout()

    def on_paint(self, event):
        """Handles the paint event to draw the image on the panel.

        Args:
            event (wx.PaintEvent): The event instance triggered by a repaint request.
        """

        if not self.hide:
            dc = wx.BufferedPaintDC(self)
            dc.SetBackground(self.backBrush)
            dc.Clear()
            dc.DrawBitmap(self.bitmap, self.x_offset, self.y_offset)

    def on_resize(self, size):
        """Handles resizing of the panel to adjust the bitmap size accordingly.

        Args:
            event (wx.SizeEvent): The event instance triggered by a resize action.
        """

        self.refresh_bitmap()

    def set_image(self, image):
        """Sets the image to be displayed on the panel.

        Args:
            image (wx.Image): The image to display.
        """

        if image is not None:
            if self.hide:
                self.hide = False
            self.image = image
            self.image_size = self.image.GetSize()
            self.refresh_bitmap()

    def set_default_image(self):
        """Resets the image displayed to a default blank image."""
        
        self.set_image(self.default_image)

    def set_frame(self, frame):
        """Converts a frame from a video capture into a wx.Image and displays it.

        Args:
            frame (np.array): A frame captured from a video source, in numpy array format.
        """

        if frame is not None:
            self.fps += 1
            height, width = frame.shape[:2]
            if height == 0 or width == 0:
                return
            if time.time() - self.time_start >= 1:
                self.time_start = time.time()
                # wx.PostEvent(self, PassFPS(self.fps))
                self.fps = 0
            self.set_image(
                wx.ImageFromBuffer(width, height, cv2.resize(frame, (width, height)))
            )

    def refresh_bitmap(self):
        """Refreshes the bitmap according to the current image and panel size."""

        self.best_size = self.get_best_size()
        (w, h, self.x_offset, self.y_offset) = self.best_size
        if w > 0 and h > 0:
            try:
                self.bitmap = wx.Bitmap(self.image.Scale(w, h))
            except Exception as e:
                logger.error("invalid new image size")
                logger.error(e)
                self.bitmap = wx.Bitmap(self.default_image)
        self.Refresh()

    def get_best_size(self):
        """Calculates the best fitting size for the image within the panel.

        Returns:
            tuple: A tuple containing the scaled width, height, and offsets (width, height, x_offset, y_offset).
        """

        (wwidth, wheight) = self.GetSize()
        (width, height) = self.image_size

        if height > 0 and wheight > 0:
            if float(width) / height > float(wwidth) / wheight:
                nwidth = wwidth
                nheight = float(wwidth * height) / width
                x_offset = 0
                y_offset = (wheight - nheight) / 2.0
            else:
                nwidth = float(wheight * width) / height
                nheight = wheight
                x_offset = (wwidth - nwidth) / 2.0
                y_offset = 0
            return (int(nwidth), int(nheight), int(x_offset), int(y_offset))
        else:
            return (0, 0, 0, 0)
