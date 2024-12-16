from cameras.camera_abc import *

import time
import numpy as np
import threading

import queue
import wx

import logging
logger = logging.getLogger(__name__)

from events.events import (
    EVT_ON_CAM_TEMP_UPDATE,
    CAM_TEMP_EVT,
    EVT_ON_CAM_IMG,
    CAM_IMG_EVT,
)


class Camera_MOCKUP(Camera_ABC, threading.Thread):
    """
    A mockup implementation of a camera, simulating camera operations such as acquisition,
    exposure control, and gain adjustments. This class extends both the abstract camera base class
    and Python's threading.Thread class to operate the camera in a separate thread.

    Attributes:
        event_catcher (wx.EvtHandler): A reference to an event handler to which the camera sends events.
        frame_queue (queue.Queue): A queue to which frames are added after acquisition.
        command_queue (queue.Queue): A queue to handle incoming commands to the camera.
        killswitch (threading.Event): An event to stop the camera thread gracefully.
        xpix (int): Number of pixels in the X dimension of the camera sensor.
        ypix (int): Number of pixels in the Y dimension of the camera sensor.
        connected (bool): Status flag indicating if the camera is connected.
        current_exp (int): Current exposure time setting.
        current_gain (float): Current gain setting.
    """

    def __init__(self, *args, event_catcher=None, frame_queue=None, **kw):
        threading.Thread.__init__(self)
        self.command_queue = queue.Queue()
        self.killswitch = threading.Event()
        # self.event_catcher = event_catcher
        self.frame_queue = frame_queue
        self.xpix, self.ypix = 1920, 1080
        self.connected = False

        self.current_exp = 100
        self.current_gain = 1

    def run(self):
        """
        The entry point for the thread, initiating camera connection and acquisition.
        """

        self.open_camera()

    def open_camera(self) -> bool:
        """
        Simulates the process of connecting to a camera and starting data acquisition.

        Returns:
            bool: True if the camera is successfully 'connected' and acquisition starts, False otherwise.
        """

        self.start_acquisition()
        self.connected = True

        return True

    def close_camera(self):
        """
        Simulates closing the camera connection and stops data acquisition.
        """

        logger.info("Closing demo camera")
        self.stop_acquisition()
    
    def stop(self):
        """
        Stops the camera operations and the thread.
        """
        
        self.killswitch.set()
        if self.is_alive():
            self.close_camera()
            self.join()

    def is_connected(self):
        return self.connected

    def start_acquisition(self):
        """
        Simulates the data acquisition process of the camera, generating frames and adding them to the frame queue.
        """

        logger.info("Starting acquisition")

        while not self.killswitch.is_set():
            try:
                # Create a random square-shape array with random 16-bit values
                arr = np.random.randint(
                    0, 65535, size=(self.ypix, self.xpix), dtype=np.uint16
                )
                arr = np.frombuffer(arr, dtype=np.uint16).reshape(self.ypix, self.xpix)
                self.frame_queue.put(arr)
                time.sleep(0.5)
            except Exception as e:
                logger.error("Error: %s", e)
                break

    def stop_acquisition(self):
        """
        Simulates stopping the data acquisition of the camera.
        """

        pass

    def set_roi(self, x, y, width, height):
        """
        Sets the region of interest (ROI) on the simulated camera sensor.

        Args:
            x (int): The X coordinate of the top-left corner of the ROI.
            y (int): The Y coordinate of the top-left corner of the ROI.
            width (int): The width of the ROI.
            height (int): The height of the ROI.
        """

        self.xpix = width
        self.ypix = height

    def get_roi(self):
        """
        Retrieves the current region of interest (ROI) settings.

        Returns:
            tuple: A tuple containing the x and y coordinates, and the width and height of the ROI.
        """

        return (0, 0, self.xpix, self.ypix)

    def set_exposure(self, exposure):
        """
        Sets the exposure time of the camera.

        Args:
            exposure (int): The desired exposure time in milliseconds.
        """

        self.current_exp = exposure

    def set_auto_exposure(self, auto):
        pass

    def get_exposure(self):
        """
        Retrieves the current exposure setting of the camera.

        Returns:
            int: The current exposure time in milliseconds.
        """

        return self.current_exp

    def get_exposure_range(self):
        """
        Provides the range and increment step of possible exposure times.

        Returns:
            tuple: A tuple containing the minimum exposure, maximum exposure, and the increment step.
        """
        min_exp = 20
        max_exp = 1000
        increment = 1
        return (min_exp, max_exp, increment)

    def set_gain(self, gain):
        """
        Sets the gain level of the camera.

        Args:
            gain (float): The desired gain level.
        """

        self.current_gain = gain

    def set_auto_gain(self, auto):
        pass

    def get_gain(self):
        """
        Retrieves the current gain setting of the camera.

        Returns:
            float: The current gain level.
        """

        return self.current_gain

    def get_gain_range(self):
        """
        Provides the range and increment step of possible gain levels.

        Returns:
            tuple: A tuple containing the minimum gain, maximum gain, and the increment step.
        """
        
        min_gain = 1
        max_gain = 20
        increment = 1
        return (min_gain, max_gain, increment)
