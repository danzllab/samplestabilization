import wx
from events.events import EVT_ON_CLOSE_DIPLAY
from utils.config_tool import *

import time

import logging
logger = logging.getLogger(__name__)


class Camera_Settings_Page(wx.Panel):
    """A panel for managing camera settings within a graphical user interface.

    This class provides UI elements to control and configure camera settings such as exposure, gain, and region of interest (ROI).
    It also handles saving configurations to a file.

    Attributes:
        camera (Camera): An instance of a Camera object to interact with hardware.
        camera_backend (str): Identifier for the backend used to process camera settings.
        parent (wx.Window): The parent window for this panel.
        is_running (bool): Flag to track the running state of the camera.

    Args:
        args: Variable length argument list.
        camera (Camera): An optional camera instance.
        camera_backend (str): Backend identifier for the camera.
        kw: Arbitrary keyword arguments.
    """
    def __init__(self, *args, camera=None, camera_backend, **kw) -> None:

        wx.Panel.__init__(self, *args, **kw)

        self.camera = camera
        self.camera_backend = camera_backend
        self.parent = kw["parent"]
        self.is_running = False

        self.Connect(-1, -1, EVT_ON_CLOSE_DIPLAY, self.on_close)

        self.describe_ui()

    def on_set_exp(self, event):
        """Handle setting the camera exposure based on user input.

        Args:
            event (wx.Event): The event object, not used directly in the function.
        """

        exp = float(self.text_exp.GetValue())
        try:
            self.camera.set_exposure(exp)
        except Exception as e:
            logger.error(e)
            wx.MessageBox(
                "Error setting exposure time. Please make sure that the camera is connected and that the correct driver is installed.",
                "Error",
                wx.OK | wx.ICON_ERROR,
            )

    def on_set_gain(self, event):
        """Handle setting the camera gain based on user input.

        Args:
            event (wx.Event): The event object, not used directly in the function.
        """
        
        pass

    def on_cam_conf_save(self, event):
        """Save the current configuration to a file.

        Args:
            event (wx.Event): The event object containing information about the save action.
        """
        path = event.GetPath()

        update_config_by_section(
            path,
            self.camera_backend,
            {
                "roi_crop": "["
                + self.roi_x1.GetValue()
                + ","
                + self.roi_x2.GetValue()
                + ","
                + self.roi_y1.GetValue()
                + ","
                + self.roi_y2.GetValue()
                + "]",
                "exposure": self.text_exp.GetValue(),
                "gain": self.text_gain.GetValue(),
            },
        )

    def on_close(self, event):
        """Handle the closing event by removing this page from its parent.

        Args:
            event (wx.Event): The event object, not used directly in the function.
        """

        self.parent.DeletePage(self.parent.FindPage(self))

    def update_ui_settings(self):
        """Update the UI with the current camera settings, like exposure and gain."""

        time.sleep(5)
        if self.camera is not None:
            # Update Exposure
            exp_min, exp_max, increment = self.camera.get_exposure_range()
            self.sld_exp.SetRange(int(exp_min), int(exp_max))
            self.sld_exp.SetTickFreq(int(increment))
            self.text_exp.SetValue(str(int(self.camera.get_exposure())))

            # Update Gain
            gain_min, gain_max, increment = self.camera.get_gain_range()
            self.sld_gain.SetRange(int(gain_min), int(gain_max))
            self.sld_gain.SetTickFreq(int(increment))
            self.text_gain.SetValue(str(int(self.camera.get_gain())))

            # Update ROI
            # x_min, x_max, y_min, y_max = self.camera.get_roi_range()
            # self.x_roi_label.SetLabel("X Limits: [{}, {}]".format(x_min, x_max))
            # self.y_roi_label.SetLabel("Y Limits: [{}, {}]".format(y_min, y_max))

    def on_set_roi(self, event):
        """Set the region of interest (ROI) for the camera based on user input.

        Args:
            event (wx.Event): The event object containing ROI settings.
        """

        roi_x1 = int(self.roi_x1.GetValue())
        roi_x2 = int(self.roi_x2.GetValue())
        roi_y1 = int(self.roi_y1.GetValue())
        roi_y2 = int(self.roi_y2.GetValue())
        try:
            self.camera.set_roi(roi_x1, roi_y1, roi_x2, roi_y2)
        except Exception as e:
            logger.error(e)
            wx.MessageBox(
                "Error setting ROI. Please make sure that the camera is connected and that the correct driver is installed.",
                "Error",
                wx.OK | wx.ICON_ERROR,
            )


    def describe_ui(self):
        """Set up the UI components and layout."""
        
        bSizer17 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel26 = wx.Panel(
            self,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        self.m_panel26.SetMaxSize(wx.Size(-1, 500))

        bSizer55 = wx.BoxSizer(wx.VERTICAL)

        bSizer181 = wx.BoxSizer(wx.VERTICAL)

        bSizer25 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText12 = wx.StaticText(
            self.m_panel26, wx.ID_ANY, "ROI", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText12.Wrap(-1)

        bSizer25.Add(self.m_staticText12, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.y_roi_label = wx.StaticText(
            self.m_panel26,
            wx.ID_ANY,
            "Y Limits: [...]",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.y_roi_label.Wrap(-1)

        bSizer25.Add(self.y_roi_label, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer261 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer261.Add((0, 0), 1, wx.EXPAND, 5)

        self.m_staticText141 = wx.StaticText(
            self.m_panel26, wx.ID_ANY, "Y: ", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText141.Wrap(-1)

        bSizer261.Add(self.m_staticText141, 0, wx.ALL, 5)

        self.m_staticText151 = wx.StaticText(
            self.m_panel26, wx.ID_ANY, "[", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText151.Wrap(-1)

        bSizer261.Add(self.m_staticText151, 0, wx.ALL, 5)

        self.roi_y1 = wx.TextCtrl(
            self.m_panel26,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(40, -1),
            0,
        )
        bSizer261.Add(self.roi_y1, 0, wx.ALL, 5)

        self.m_staticText161 = wx.StaticText(
            self.m_panel26, wx.ID_ANY, ",", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText161.Wrap(-1)

        bSizer261.Add(self.m_staticText161, 0, wx.ALL, 5)

        self.roi_y2 = wx.TextCtrl(
            self.m_panel26,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(40, -1),
            0,
        )
        bSizer261.Add(self.roi_y2, 0, wx.ALL, 5)

        self.m_staticText171 = wx.StaticText(
            self.m_panel26, wx.ID_ANY, "]", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText171.Wrap(-1)

        bSizer261.Add(self.m_staticText171, 0, wx.ALL, 5)

        bSizer261.Add((0, 0), 1, wx.EXPAND, 5)

        bSizer25.Add(bSizer261, 1, wx.EXPAND, 5)

        bSizer181.Add(bSizer25, 1, wx.EXPAND, 5)

        bSizer34 = wx.BoxSizer(wx.VERTICAL)

        self.x_roi_label = wx.StaticText(
            self.m_panel26,
            wx.ID_ANY,
            "X Limits: [...]",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.x_roi_label.Wrap(-1)

        bSizer34.Add(self.x_roi_label, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer26 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer26.Add((0, 0), 1, wx.EXPAND, 5)

        self.m_staticText14 = wx.StaticText(
            self.m_panel26, wx.ID_ANY, "X: ", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText14.Wrap(-1)

        bSizer26.Add(self.m_staticText14, 0, wx.ALL, 5)

        self.m_staticText15 = wx.StaticText(
            self.m_panel26, wx.ID_ANY, "[", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText15.Wrap(-1)

        bSizer26.Add(self.m_staticText15, 0, wx.ALL, 5)

        self.roi_x1 = wx.TextCtrl(
            self.m_panel26,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(40, -1),
            0,
        )
        bSizer26.Add(self.roi_x1, 0, wx.ALL, 5)

        self.m_staticText16 = wx.StaticText(
            self.m_panel26, wx.ID_ANY, ",", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText16.Wrap(-1)

        bSizer26.Add(self.m_staticText16, 0, wx.ALL, 5)

        self.roi_x2 = wx.TextCtrl(
            self.m_panel26,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(40, -1),
            0,
        )
        bSizer26.Add(self.roi_x2, 0, wx.ALL, 5)

        self.m_staticText17 = wx.StaticText(
            self.m_panel26, wx.ID_ANY, "]", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText17.Wrap(-1)

        bSizer26.Add(self.m_staticText17, 0, wx.ALL, 5)

        bSizer26.Add((0, 0), 1, wx.EXPAND, 5)

        bSizer34.Add(bSizer26, 1, wx.EXPAND, 5)

        bSizer181.Add(bSizer34, 0, wx.EXPAND, 5)

        self.set_roi = wx.Button(
            self.m_panel26, wx.ID_ANY, "Set ROI", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.set_roi.Bind(wx.EVT_BUTTON, self.on_set_roi, id=self.set_roi.GetId())
        bSizer181.Add(self.set_roi, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer55.Add(bSizer181, 1, wx.EXPAND, 5)

        bSizer32 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText29 = wx.StaticText(
            self.m_panel26,
            wx.ID_ANY,
            "Exposure time [s]",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText29.Wrap(-1)

        bSizer32.Add(self.m_staticText29, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer33 = wx.BoxSizer(wx.HORIZONTAL)

        self.sld_exp = wx.Slider(
            self.m_panel26,
            wx.ID_ANY,
            50,
            0,
            100,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.SL_HORIZONTAL,
        )
        bSizer33.Add(self.sld_exp, 1, wx.ALL, 5)

        self.text_exp = wx.TextCtrl(
            self.m_panel26,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_PROCESS_ENTER,
        )
        self.text_exp.Bind(
            wx.EVT_TEXT_ENTER, self.on_set_exp, id=self.text_exp.GetId()
        )
        bSizer33.Add(self.text_exp, 0, wx.ALL, 5)

        bSizer32.Add(bSizer33, 0, wx.EXPAND, 5)

        self.set_exp = wx.Button(
            self.m_panel26, wx.ID_ANY, "Set", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.set_exp.Bind(wx.EVT_BUTTON, self.on_set_exp, id=self.set_exp.GetId())
        bSizer32.Add(self.set_exp, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer55.Add(bSizer32, 1, wx.EXPAND | wx.TOP, 5)

        bSizer321 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText291 = wx.StaticText(
            self.m_panel26, wx.ID_ANY, "Gain", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText291.Wrap(-1)

        bSizer321.Add(self.m_staticText291, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer331 = wx.BoxSizer(wx.HORIZONTAL)

        self.sld_gain = wx.Slider(
            self.m_panel26,
            wx.ID_ANY,
            1,
            0,
            20,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.SL_HORIZONTAL,
        )
        bSizer331.Add(self.sld_gain, 1, wx.ALL, 5)

        self.text_gain = wx.TextCtrl(
            self.m_panel26,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        bSizer331.Add(self.text_gain, 0, wx.ALL, 5)

        bSizer321.Add(bSizer331, 0, wx.EXPAND, 5)

        self.set_gain = wx.Button(
            self.m_panel26, wx.ID_ANY, "Set", wx.DefaultPosition, wx.DefaultSize, 0
        )

        self.set_gain.Bind(wx.EVT_BUTTON, self.on_set_gain, id=self.set_gain.GetId())
        bSizer321.Add(self.set_gain, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer55.Add(bSizer321, 1, wx.EXPAND, 5)

        bSizer20 = wx.BoxSizer(wx.VERTICAL)

        m_staticText91 = wx.StaticText(
            self.m_panel26,
            wx.ID_ANY,
            "Save configuration:",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        m_staticText91.Wrap(-1)

        bSizer20.Add(m_staticText91, 0, wx.ALL, 5)

        self.cam_conf_save = wx.FilePickerCtrl(
            self.m_panel26,
            wx.ID_ANY,
            wx.EmptyString,
            "Select a file",
            "TXT files (*.txt)|*.txt",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.FLP_SAVE | wx.FLP_USE_TEXTCTRL,
        )
        bSizer20.Add(self.cam_conf_save, 1, wx.ALL | wx.ALIGN_LEFT | wx.EXPAND, 5)
        self.cam_conf_save.Bind(
            wx.EVT_FILEPICKER_CHANGED,
            self.on_cam_conf_save,
            id=self.cam_conf_save.GetId(),
        )
        bSizer20.Add((0, 0), 1, wx.EXPAND, 5)

        bSizer55.Add(bSizer20, 1, wx.EXPAND, 5)

        self.m_panel26.SetSizer(bSizer55)
        self.m_panel26.Layout()
        bSizer55.Fit(self.m_panel26)
        bSizer17.Add(self.m_panel26, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer17)
        self.Layout()
        bSizer17.Fit(self)
