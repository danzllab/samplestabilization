from pipython import GCSDevice, pitools
from stage_control.stage_abc import *
import logging
logger = logging.getLogger(__name__)


DLL_PATH = "D:\\sampleLock_python\\PI_GCS2_DLL_x64.dll"
DEV_NAME = "E-727"

class Stage_PI(Stage_ABC):
    def __init__(self, *args, **kw):
        pidevice = GCSDevice(
            devname=DEV_NAME, gcsdll=DLL_PATH
        )  # relative path raises warning, disappears when using absolute: D:\\sampleLock_python\\PI_GCS2_DLL_x64.dll
        pidevice.ConnectUSB("120036307")

        self.pidevice = pidevice
        self.axes = pitools.getaxeslist(pidevice, None)
        self.stage_limits = self.get_travel_range()

        pitools.DeviceStartup(pidevice)
        pitools.enableaxes(pidevice, self.axes)
        pitools.setservo(pidevice, self.axes, [True, True, True])

        pidevice.ATZ()
        pitools.waitonautozero(pidevice)
        pitools.movetomiddle(pidevice, self.axes)

    def get_travel_range(self):
        range_min = pitools.getmintravelrange(self.pidevice, None)
        range_max = pitools.getmaxtravelrange(self.pidevice, None)
        ranges = {}
        for ax in self.axes:
            ranges[ax] = [range_min[ax], range_max[ax]]
        return ranges

    def assert_stage_limits(self, axis, value):
        if value > self.stage_limits[axis][0] and value < self.stage_limits[axis][1]:
            return True
        else:
            return False

    def wait_settled(self, delay=0.0):
        pitools.waitontarget(self.pidevice, postdelay=delay)

    def get_position(self):
        self.wait_settled(delay=0.1)
        pos = self.pidevice.qPOS()
        return pos

    def move_to(self, axis, position):
        if self.assert_stage_limits(axis, position):
            self.pidevice.MOV(axis, position)
            return True
        else:
            return False

    def move_by(self, axis, d_pos):
        pos = self.get_position()
        pos_new = pos[str(axis)] + d_pos
        if self.assert_stage_limits(axis, pos_new):
            self.pidevice.MOV(axis, pos_new)
            return True
        else:
            return False

    def close_stage(self):
        self.pidevice.ATZ()
        pitools.waitonautozero(self.pidevice)
        self.pidevice.CloseConnection()

       
    def open_stage(self):
        pass

   
    def is_connected(self):
        pass

   
    def set_velocity(self, velocity):
        pass

   
    def get_velocity(self):
        pass

   
    def set_acceleration(self, acceleration):
        pass

   
    def get_acceleration(self):
        pass

   
    def set_home(self):
        pass

   
    def get_home(self):
        pass