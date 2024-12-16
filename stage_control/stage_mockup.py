from stage_control.stage_abc import *
from events.events import *

import threading
import time
import numpy as np
import os
import logging
logger = logging.getLogger(__name__)

import csv
import wx

DATA_MOCKUP_PATH = "data/sampleLock_0.csv"


def read_data(file_path):
    if os.path.exists(file_path):
        return np.genfromtxt(file_path, delimiter=",")
    else:
        logger.error(f"File {file_path} does not exist")

        return None

class Stage_MOCKUP(Stage_ABC):
    def __init__(self, *args, **kw):
        self.axes = ["1", "2", "3"]
        self.stage_limits = dict({"1": [-10.0, 10.0], "2": [-10.0, 10.0], "3": [-10., 10.0]})
        self.position = dict({"1": 0, "2": 0, "3": 0})
    
    def open_stage(self):
        pass

    def close_stage(self):
        pass

    
    def is_connected(self):
        pass

    
    def get_travel_range(self, x, y):
        pass

    def assert_stage_limits(self, axis, value):
        if value > self.stage_limits[axis][0] and value < self.stage_limits[axis][1]:
            return True
        else:
            return False

    
    def get_position(self):
        return self.position
    
    def wait_settled(self, delay=0.0):
        time.sleep(delay)
        pass

    
    def move_by(self, axis, d_pos):
        pos = self.get_position()
        pos_new = pos[str(axis)] + d_pos
        if self.assert_stage_limits(axis, pos_new):
            self.position[axis] = pos_new
            return True
        else:
            return False

    
    def move_to(self, axis, pos):
        # time.sleep(0.2)
        if self.assert_stage_limits(axis, pos):
            self.position[axis] = pos
            return True
        else:
            return False

    
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
