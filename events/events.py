import wx
import wx.lib.newevent

EVT_ON_STAGE_UPDATE = wx.NewId()
EVT_ON_CAM_TEMP_UPDATE = wx.NewId()
EVT_ON_CAM_IMG = wx.NewId()

EVT_ON_CLOSE_DIPLAY = wx.NewId()
EVT_ON_PLOT_UPDATE = wx.NewId()

EVT_STOP_CAM = wx.NewId()

class STOP_CAM_EVT(wx.PyEvent):
    def __init__(self):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_STOP_CAM)


class STAGE_EVT(wx.PyEvent):
    def __init__(self, val):
        wx.PyEvent.__init__(self)
        self.val = val
        self.SetEventType(EVT_ON_STAGE_UPDATE)


class CAM_TEMP_EVT(wx.PyEvent):
    def __init__(self, temp, cam_num):
        wx.PyEvent.__init__(self)
        self.temp = temp
        self.cam_count = cam_num
        self.SetEventType(EVT_ON_CAM_TEMP_UPDATE)


class CAM_IMG_EVT(wx.PyEvent):
    def __init__(self, img, cam_num):
        wx.PyEvent.__init__(self)
        self.img = img
        self.cam_count = cam_num
        self.SetEventType(EVT_ON_CAM_IMG)

class PLOT_UPDATE(wx.PyEvent):
    def __init__(self, pos=[], err=[], dt=None):
        wx.PyEvent.__init__(self)
        self.pos = pos
        self.err = err
        self.dt = dt
        self.SetEventType(EVT_ON_PLOT_UPDATE)


class CLOSE_DISPLAY_EVT(wx.PyEvent):
    def __init__(self):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_ON_CLOSE_DIPLAY)
