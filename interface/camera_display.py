import wx
from interface.video_view import VideoView
from events.events import CLOSE_DISPLAY_EVT, STOP_CAM_EVT


class Camera_Display(wx.Panel):
    """A panel within a UI to handle video display and control for a camera.

    This class manages the video display for a camera, including controls to start and stop the camera,
    take screenshots, and record videos. It also handles the interface interactions related to
    the camera's operations such as starting, stopping, and updating display parameters.

    Attributes:
        camera_backend (str): Identifier for the backend used by the camera, defining how the camera is managed.
        is_running (bool): Flag to indicate whether the camera is currently capturing video.
        related_settings_page (wx.Panel): A reference to the related settings panel for additional camera configurations.
        parent (wx.Window): The parent window for this panel.
        video_panel (VideoView): The video display component.
        toolbar (wx.ToolBar): A toolbar with controls for camera operations.
        start_stop_btn (wx.Tool): A toggle tool in the toolbar for starting and stopping the camera.
        scrshot_btn (wx.Tool): A tool in the toolbar for taking screenshots.
        vid_btn (wx.Tool): A tool in the toolbar for recording videos.
        min_max_disp (wx.StaticText): A display label in the toolbar showing minimum and maximum values for some parameter.

    Args:
        args: Variable length argument list.
        camera_backend (str): Identifier for the backend used by the camera.
        related_settings_page (wx.Panel): The associated settings panel for the camera.
        kw: Arbitrary keyword arguments.
    """

    def __init__(
        self, *args, camera_backend=None, related_settings_page=None, **kw
    ) -> None:
        wx.Panel.__init__(self, *args, **kw)

        self.camera_backend = camera_backend
        self.is_running = False
        self.related_settings_page = related_settings_page
        self.parent = kw["parent"]
        

        self.describe_ui()

    def on_start_cam(self, event):
        """Toggle the camera operation state between start and stop based on current status.

        Args:
            event (wx.Event): The event object triggered by clicking the start/stop tool.
        """

        if self.is_running:
            # wx.PostEvent(self.parent, STOP_CAM_EVT())
            self.video_panel.stop()
            self.is_running = False
        else:
            self.video_panel.start()
            self.is_running = True

    def on_close(self):
        """Stop the video panel and post a close event to the related settings page."""

        self.video_panel.stop()
        wx.PostEvent(self.related_settings_page, CLOSE_DISPLAY_EVT())

    def update_min_max(self, min, max):
        """Update the minimum and maximum display label with new values.

        Args:
            min (int): The new minimum value to display.
            max (int): The new maximum value to display.
        """

        self.min_max_disp.SetLabel("Min: {} Max: {}".format(min, max))

    def describe_ui(self):
        """Set up the UI components and layout for the camera display panel."""
        
        cam_page_sizer = wx.BoxSizer(wx.VERTICAL)

        self.video_panel = VideoView(
            self,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
            camera_backend=self.camera_backend,
            related_settings_page=self.related_settings_page,
        )

        cam_page_sizer.Add(self.video_panel, 1, wx.EXPAND | wx.ALL, 5)

        self.toolbar = wx.ToolBar(
            self,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TB_HORIZONTAL,
        )

        self.start_stop_btn = self.toolbar.AddTool(
            wx.ID_ANY,
            "Start/Stop Camera",
            wx.Bitmap("interface/icons/24px/003-play-button.png", wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            wx.EmptyString,
            wx.EmptyString,
            None,
        )

        self.scrshot_btn = self.toolbar.AddTool(
            wx.ID_ANY,
            "Take Screenshot",
            wx.Bitmap("interface/icons/24px/007-camera.png", wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            wx.EmptyString,
            wx.EmptyString,
            None,
        )

        self.vid_btn = self.toolbar.AddTool(
            wx.ID_ANY,
            "Record Video",
            wx.Bitmap("interface/icons/24px/002-camera.png", wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            wx.EmptyString,
            wx.EmptyString,
            None,
        )

        self.toolbar.AddSeparator()

        self.min_max_disp = wx.StaticText( self.toolbar, wx.ID_ANY, u"Min: Max: ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.min_max_disp.Wrap( -1 )

        self.toolbar.AddControl( self.min_max_disp )

        self.toolbar.Realize()
        self.Bind(wx.EVT_TOOL, self.on_start_cam, id=self.start_stop_btn.GetId())

        cam_page_sizer.Add(self.toolbar, 0, wx.EXPAND, 5)

        self.SetSizer(cam_page_sizer)
        self.Layout()
        cam_page_sizer.Fit(self)
