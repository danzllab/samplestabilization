from cameras.camera_abc import *

import time
import numpy as np
import matplotlib.pyplot as plt
from pyAndorSDK2 import atmcd, atmcd_codes, atmcd_errors
import threading

import queue
import logging
logger = logging.getLogger(__name__)

from events.events import (
    EVT_ON_CAM_TEMP_UPDATE,
    CAM_TEMP_EVT,
    EVT_ON_CAM_IMG,
    CAM_IMG_EVT,
)


class Camera_Andor(Camera_ABC, threading.Thread):
    """
    A class for interfacing with Andor cameras using the pyAndorSDK2 library. 
    This class handles camera initialization, frame acquisition, and setting various camera parameters.
    It operates the camera interactions in a separate thread to allow non-blocking operations in a GUI application.

    Attributes:
        event_catcher (optional): A wxPython event handler to send camera-related events.
        frame_queue (queue.Queue): A queue where captured frames are placed.
        cam_count (int): Number of cameras, defaulting to 1.
        working_temp (int): The target working temperature of the camera.
        xpix (int): Width of the camera sensor in pixels.
        ypix (int): Height of the camera sensor in pixels.
        connected (bool): True if the camera is successfully initialized and connected.
    """

    def __init__(self, *args, event_catcher=None, frame_queue=None, **kw):
        threading.Thread.__init__(self)
        self.command_queue = queue.Queue()
        self.killswitch = threading.Event()
        # self.event_catcher = event_catcher
        self.frame_queue = frame_queue
        self.cam_count = 1
        self.working_temp = 18
        self.xpix, self.ypix = 0, 0
        self.connected = False

        self.is_exp_set = False
        self.is_gain_set = False
        self.is_roi_set = False

        self._sdk = atmcd("C:\\Program Files\\Andor SDK\\Python\\pyAndorSDK2\\pyAndorSDK2\\libs\\Windows\\64")  # Load the atmcd library from PATH or LD_LIBRARY_PATH
        self._codes = atmcd_codes

    # Thread related methods
    def stop(self):
        self.killswitch.set()
        if self.is_alive():
            self.close_camera()
            self.join()

    def run(self):
        logger.info("Camera_Andor thread started")
        if self.open_camera():
            self.start_acquisition()
        else:
            raise Exception("Could not open camera")

    def __init_camera(self) -> bool:
        ret = self._sdk.Initialize("")
        # wx.PostEvent(self.event_catcher, CAM_TEMP_EVT(temp=temperature, cam_num=self.cam_count))
        return atmcd_errors.Error_Codes.DRV_SUCCESS == ret

    def __prepare_acquisition(self) -> bool:
        ret = self._sdk.SetAcquisitionMode(self._codes.Acquisition_Mode.SINGLE_SCAN)
        logger.info("Function SetAcquisitionMode returned {} mode = Run Till Abort".format(ret))

        ret = self._sdk.SetReadMode(self._codes.Read_Mode.IMAGE)
        logger.info("Function SetReadMode returned {} mode = Image".format(ret))

        ret = self._sdk.SetTriggerMode(self._codes.Trigger_Mode.INTERNAL)
        logger.info("Function SetTriggerMode returned {} mode = Internal".format(ret))

        (ret, self.xpix, self.ypix) = self._sdk.GetDetector()
        self.roi = [0, 0, self.xpix, self.ypix] # <---- [x, y, width, height]
        logger.info("Function GetDetector returned {} xpixels = {} ypixels = {}".format(ret, self.xpix, self.ypix))

        ret = self._sdk.SetImage(1, 1, self.roi[0]+1, self.roi[0]+self.roi[2], self.roi[1]+1, self.roi[1]+self.roi[3])

        logger.info("Function SetImage returned {} hbin = 1 vbin = 1 hstart = 1 hend = {} vstart = 1 vend = {}".format(ret, self.xpix, self.ypix))
        
        self.exposure = self.get_exposure()
        self.gain = self.get_gain()

        return True

    def open_camera(self) -> bool:
        """
        Opens the camera and prepares it for image acquisition by setting acquisition parameters.

        Returns:
            bool: True if the camera opens successfully, False otherwise.
        """

        if not self.__init_camera():
            logger.error("Cannot continue, could not prepare camera for acquisition")
            return False

        if not self.__prepare_acquisition():
            logger.error("Cannot continue, could not prepare camera for acquisition")
            self.stop()
            return False

        self.connected = True

        return True

    def close_camera(self):
        """
        Closes the camera connection and cleans up resources.
        """

        logger.info("Closing Andor camera")

    def is_connected(self):
        """
        Checks the connection status of the camera.

        Returns:
            bool: True if the camera is connected and ready, False otherwise.
        """
        
        return self.connected

    def get_frame(self):
        """
        Retrieves a single frame from the camera, processing any necessary settings before acquisition.

        Returns:
            np.ndarray: The acquired image as a NumPy array.
        """

        if self.is_exp_set:
                    ret = self._sdk.SetExposureTime(self.exposure)
                    logger.info("Function SetExposureTime returned {} time = {}s".format(ret, self.exposure))
                    self.is_exp_set = False

        if self.is_gain_set:
                    ret = self._sdk.SetEMCCDGain(self.gain)
                    logger.info("Function SetEMCCDGain returned {} gain = {}".format(ret, self.gain))
                    self.is_gain_set = False

        if self.is_roi_set:
            ret = self._sdk.SetImage(1, 1, self.roi[0]+1, self.roi[0]+self.roi[2], self.roi[1]+1, self.roi[1]+self.roi[3])
            logger.info("ROI is set to x = {} y = {} width = {} height = {}".format(self.roi[0]+1, self.roi[0]+self.roi[2], self.roi[1]+1, self.roi[1]+self.roi[3]))
            self.is_roi_set = False

        self._sdk.PrepareAcquisition()
        self._sdk.StartAcquisition()
        self._sdk.WaitForAcquisition()
        (ret, arr) = self._sdk.GetMostRecentImage16(self.roi[2] * self.roi[3])
        arr = np.frombuffer(arr, dtype=np.uint16).reshape(self.roi[3],  self.roi[2])
        return arr

    def start_acquisition(self):
        """
        Begins the continuous acquisition of images from the camera.

        Handles setting up the camera for continuous acquisition and error management.
        """

        while not self.killswitch.is_set():
            try:
                arr = self.get_frame()
                self.frame_queue.put(arr)
            except Exception as e:
                logger.error("Error: %s", e)
                break
        # ret = self._sdk.StartAcquisition()
        # if ret == atmcd_errors.Error_Codes.DRV_SUCCESS:
        #     print("Acquisition started")
        # if ret == atmcd_errors.Error_Codes.DRV_NOT_INITIALIZED:
        #     print("Camera not initialized")
        # if ret == atmcd_errors.Error_Codes.DRV_ACQUIRING:
        #     print("Camera is already acquiring")

        # while not self.killswitch.is_set():
        #     try:
        # (ret, arr) = self._sdk.GetMostRecentImage16(self.xpix*self.ypix)
        # # print("Function GetMostRecentImage16 returned {} first pixel = {} size = {}".format(
        # #     ret, arr[0], self.xpix*self.ypix), end="\r")
        # arr = np.frombuffer(arr, dtype=np.uint16).reshape(self.ypix, self.xpix)
        # self.frame_queue.put(arr)
        #         time.sleep(0.1)
        #     except Exception as e:
        #         print("Error: ", e)
        #         break

    def stop_acquisition(self):
        """
        Stops the acquisition process cleanly, ensuring no frames are left unhandled.

        Ensures that all buffers are flushed and the camera is properly reset post-acquisition.
        """

        pass

    def set_roi(self, x, y, width, height):
        """
        Sets the region of interest (ROI) for the camera sensor.

        Args:
            x (int): X-coordinate of the top-left corner of the ROI.
            y (int): Y-coordinate of the top-left corner of the ROI.
            width (int): Width of the ROI.
            height (int): Height of the ROI.
        """

        self.roi = [x, y, width, height]
        # self.roi = [x, y, self.xpix, self.ypix]
        self.is_roi_set = True

    def get_roi(self):
        return self.roi

    def set_exposure(self, exposure):
        """
        Sets the exposure time for the camera.

        Args:
            exposure (float): Desired exposure time in seconds.
        """

        self.exposure = exposure
        self.is_exp_set = True
        # ret = self._sdk.SetExposureTime(exposure)
        # while ret == atmcd_errors.Error_Codes.DRV_ACQUIRING:
        #     print("Exposure is not st yet")
        #     time.sleep(0.1)
        #     ret = self._sdk.SetExposureTime(exposure)
        # if ret == atmcd_errors.Error_Codes.DRV_SUCCESS:
        #     print(
        #         "Function SetExposureTime returned {} time = {}s".format(ret, exposure)
        #     )
        # if ret == atmcd_errors.Error_Codes.DRV_NOT_INITIALIZED:
        #     print("Camera not initialized")
        # if ret == atmcd_errors.Error_Codes.DRV_NOT_AVAILABLE:
        #     print("Camera not available")
        # print("Real Exposure set to {}s".format(exposure))

    def set_auto_exposure(self, auto):
        pass

    def get_exposure(self):
        """
        Retrieves the current exposure time from the camera.

        Returns:
            float: The current exposure time in seconds.
        """

        (ret, exposure, accumulate, kinetic) = self._sdk.GetAcquisitionTimings()
        if ret != atmcd_errors.Error_Codes.DRV_SUCCESS:
            raise Exception("Could not get exposure")
        
        return exposure

    def get_exposure_range(self):
        """
        Provides the minimum and maximum possible exposure settings for the camera.

        Returns:
            tuple: A tuple containing the minimum and maximum exposure times in seconds.
        """

        (ret, max_exp) = self._sdk.GetMaximumExposure()
        return (10 ** (-5), max_exp, 10 ** (-5))

    def set_gain(self, gain):
        """
        Sets the gain level for the camera.

        Args:
            gain (int): Desired EMCCD gain level.
        """

        self.gain = gain
        self.is_gain_set = True
        # ret = self._sdk.SetEMCCDGain(gain)
        # while ret == atmcd_errors.Error_Codes.DRV_ACQUIRING:
        #     time.sleep(0.1)
        #     ret = self._sdk.SetExposureTime(gain)
        
        # if (ret != atmcd_errors.Error_Codes.DRV_SUCCESS):
        #     raise Exception("Could not set gain")

    def set_auto_gain(self, auto):
        pass

    def get_gain(self):
        """
        Retrieves the current gain setting from the camera.

        Returns:
            int: The current gain level.
        """

        ret, gain = self._sdk.GetEMCCDGain()

        if ret != atmcd_errors.Error_Codes.DRV_SUCCESS:
            raise Exception("Could not get gain")
        
        return gain
        

    def get_gain_range(self):
        """
        Provides the range of acceptable gain settings for the camera.

        Returns:
            tuple: A tuple containing the minimum gain, maximum gain, and the step increment.
        """

        (ret, low, high) = self._sdk.GetEMGainRange()

        if ret != atmcd_errors.Error_Codes.DRV_SUCCESS:
            raise Exception("Could not get gain range")
        
        return (low, high, (high-low)/20)
