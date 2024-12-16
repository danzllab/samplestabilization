from cameras.camera_abc import *

import threading
import queue
import time
import numpy as np
from ids_peak import ids_peak as peak
from ids_peak_ipl import ids_peak_ipl
import logging
logger = logging.getLogger(__name__)


class Camera_IDS(Camera_ABC, threading.Thread):
    """
    A thread-based class for interfacing with IDS cameras using the IDS Peak library. This class
    provides mechanisms to control camera features such as exposure, gain, and region of interest (ROI),
    while also handling frame acquisition in a separate thread to maintain UI responsiveness.

    Attributes:
        command_queue (queue.Queue): A queue for processing commands sent to the camera.
        killswitch (threading.Event): An event that can be set to signal the camera thread to stop.
        event_catcher (wx.EvtHandler, optional): The event handler where camera events are reported.
        frame_queue (queue.Queue): A queue where acquired frames are placed.
        cam_count (int): A count of cameras connected or being managed (default is 1).
    """

    def __init__(self, *args, event_catcher=None, frame_queue=None, **kw):
        threading.Thread.__init__(self)
        self.command_queue = queue.Queue()
        self.killswitch = threading.Event()
        self.event_catcher = event_catcher
        self.frame_queue = frame_queue
        self.cam_count = 1

        peak.Library.Initialize()

    # Thread related methods
    def stop(self):
        self.killswitch.set()
        if self.is_alive():
            self.close_camera()
            self.join()

    def join(self, timeout=None):
        pass

    def run(self):
        """
        The method run by the thread. It opens the camera and handles frame acquisition.
        """

        self.open_camera()

    # -------------------------

    def open_camera(self):
        """
        Attempts to open the camera and configure it for frame acquisition. It prepares the
        camera, sets the ROI if necessary, allocates buffers, and begins acquiring frames.

        Raises:
            RuntimeError: If any step of the camera initialization fails.
        """
        
        if not self._open_camera(0):  # self.parameters.cam_id):
            # TODO what to do if failed?
            raise RuntimeError("Opening camera failed.")

        if not self._prepare_acquisition():
            raise RuntimeError("Preparing camera acquisition failed.")
        
        if not self._set_roi(init=True):
            raise RuntimeError("Initializing ROI failed.")

        # if self.parameters.roi is not None:
        #     if not self.set_roi(*self.parameters.roi):
        #         raise RuntimeError('Setting ROI failed.')
        # else:  # self._set_roi() calls self._alloc_and_announce_buffers(), so not necessary above
        #     if not self._alloc_and_announce_buffers():
        #         raise RuntimeError('Buffer allocation failed.')

        if not self._alloc_and_announce_buffers():
            raise RuntimeError("Buffer allocation failed.")

        if not self.start_acquisition():
            raise RuntimeError("Starting camera acquisition failed.")

        return True

    def close_camera(self):
        """
        Stops the frame acquisition, releases the camera resources, and closes the IDS Peak library.
        """

        self.stop_acquisition()
        peak.Library.Close()

    def is_connected(self):
        """
        Checks if there are any cameras connected by querying the device manager.

        Returns:
            bool: True if any camera is found, False otherwise.
        """

        # Create instance of the device manager
        device_manager = peak.DeviceManager.Instance()

        # Update the device manager
        device_manager.Update()

        # Return if no device was found
        if device_manager.Devices().empty():
            return False
        else:
            return True

    def start_acquisition(self) -> bool:
        """
        Starts the continuous acquisition of frames from the camera.

        Returns:
            bool: True if acquisition was successfully started, False otherwise.
        """

        self.__m_dataStream.StartAcquisition(
            peak.AcquisitionStartMode_Default, peak.DataStream.INFINITE_NUMBER
        )

        self.__m_node_map_remote_device.FindNode("TLParamsLocked").SetValue(1)
        self.__m_node_map_remote_device.FindNode("AcquisitionStart").Execute()
        self.__m_node_map_remote_device.FindNode("AcquisitionStart").WaitUntilDone()

        self._acquire_continuous(t_sleep=0.01)

        return True

    def stop_acquisition(self):
        """
        Stops the acquisition of frames from the camera by sending the appropriate commands to the camera.
        """

        self.__m_node_map_remote_device.FindNode("AcquisitionStop").Execute()
        self.__m_node_map_remote_device.FindNode("AcquisitionStop").WaitUntilDone()
        self.__m_node_map_remote_device.FindNode("TLParamsLocked").SetValue(0)
        self.__m_dataStream.StopAcquisition(peak.AcquisitionStopMode_Default)

    def set_roi(self, x=0, y=0, width=None, height=None):
        """
        Sets the region of interest (ROI) on the camera sensor to the specified coordinates and size.

        Args:
            x (int): The X-coordinate of the top-left corner of the ROI.
            y (int): The Y-coordinate of the top-left corner of the ROI.
            width (int, optional): The width of the ROI. If not specified, uses the maximum allowable width.
            height (int, optional): The height of the ROI. If not specified, uses the maximum allowable height.

        Returns:
            bool: True if the ROI was successfully set, False otherwise.
        """

        x_min = self.__m_node_map_remote_device.FindNode("OffsetX").Minimum()
        y_min = self.__m_node_map_remote_device.FindNode("OffsetY").Minimum()
        w_max = self.__m_node_map_remote_device.FindNode("Width").Maximum()
        h_max = self.__m_node_map_remote_device.FindNode("Height").Maximum()

        if (x < x_min) or (y < y_min) or (x > w_max) or (y > h_max):
            return False
        else:
            self.x_crop = x - x % 8
            self.y_crop = y - y % 8

            self.width_crop = width
            self.height_crop = height
            

    def _set_roi(self, x=0, y=0, width=None, height=None, init=False):
        """
        A helper function to set the region of interest (ROI) during initialization or adjustment.

        Args:
            x (int): X-coordinate of the ROI.
            y (int): Y-coordinate of the ROI.
            width (int, optional): Width of the ROI.
            height (int, optional): Height of the ROI.
            init (bool): If True, indicates the setting is part of initialization.

        Returns:
            bool: True if the ROI was successfully set, False otherwise.
        """

        if not init:
            self.__m_node_map_remote_device.FindNode("AcquisitionStop").Execute()
            self.__m_node_map_remote_device.FindNode("AcquisitionStop").WaitUntilDone()
            self.__m_node_map_remote_device.FindNode("TLParamsLocked").SetValue(0)
        # Get the minimum ROI and set it. After that there are no size restrictions anymore
        x_min = self.__m_node_map_remote_device.FindNode("OffsetX").Minimum()
        y_min = self.__m_node_map_remote_device.FindNode("OffsetY").Minimum()
        w_min = self.__m_node_map_remote_device.FindNode("Width").Minimum()
        h_min = self.__m_node_map_remote_device.FindNode("Height").Minimum()


        self.__m_node_map_remote_device.FindNode("OffsetX").SetValue(x_min)
        self.__m_node_map_remote_device.FindNode("OffsetY").SetValue(y_min)
        self.__m_node_map_remote_device.FindNode("Width").SetValue(w_min)
        self.__m_node_map_remote_device.FindNode("Height").SetValue(h_min)

        # Get the maximum ROI values
        x_max = self.__m_node_map_remote_device.FindNode("OffsetX").Maximum()
        y_max = self.__m_node_map_remote_device.FindNode("OffsetY").Maximum()
        w_max = self.__m_node_map_remote_device.FindNode("Width").Maximum()
        if width is None:
            width = w_max - 16
        h_max = self.__m_node_map_remote_device.FindNode("Height").Maximum()
        if height is None:
            height = h_max - 16


        if (x < x_min) or (y < y_min) or (x > x_max) or (y > y_max):
            return False
        elif (
            (width < w_min)
            or (height < h_min)
            or ((x + width) > w_max)
            or ((y + height) > h_max)
        ):
            return False
        else:
            # values passed to nodes must be divisible by 8
            x_roi = x - x % 8
            self.x_crop = x % 8
            y_roi = y - y % 8
            self.y_crop = y % 8
            # + 16: up to 8 subtracted from width%8, leave 8 more for cropping
            width_roi = width - width % 8 + 16
            self.width_crop = width
            height_roi = height - height % 8 + 16
            self.height_crop = height

            # Now, set final AOI
            try:
                self.__m_node_map_remote_device.FindNode("OffsetX").SetValue(int(x_roi))
                self.__m_node_map_remote_device.FindNode("OffsetY").SetValue(int(y_roi))
                self.__m_node_map_remote_device.FindNode("Width").SetValue(int(width_roi))
                self.__m_node_map_remote_device.FindNode("Height").SetValue(int(height_roi))
                
            except Exception as e:
                logger.error("Set ROI Error: %s", e)

                return False
            
            if not init:
                self.__m_node_map_remote_device.FindNode("TLParamsLocked").SetValue(1)
                self.__m_node_map_remote_device.FindNode("AcquisitionStart").Execute()
                self.__m_node_map_remote_device.FindNode("AcquisitionStart").WaitUntilDone()
            

            # re-allocate buffer for changed ROI
                self._alloc_and_announce_buffers()

            


            return True

    def get_roi(self):
        """
        Retrieves the current settings of the region of interest (ROI).

        Returns:
            tuple: The coordinates and size of the ROI as (x, y, width, height).
        """

        return self.x_crop, self.y_crop, self.width_crop, self.height_crop

    def _get_roi(self):
        x = self.__m_node_map_remote_device.FindNode("OffsetX").Value()
        y = self.__m_node_map_remote_device.FindNode("OffsetY").Value()
        width = self.__m_node_map_remote_device.FindNode("Width").Value()
        heigh = self.__m_node_map_remote_device.FindNode("Height").Value()

        return (x, y, width, heigh)

    def get_roi_range(self):
        """
        Retrieves the allowable range for setting the region of interest (ROI).

        Returns:
            tuple: The minimum and maximum values for the ROI coordinates and size as (x_min, x_max, y_min, y_max).
        """

        x_min = self.__m_node_map_remote_device.FindNode("OffsetX").Minimum()
        y_min = self.__m_node_map_remote_device.FindNode("OffsetY").Minimum()
        x_max = self.__m_node_map_remote_device.FindNode("Width").Maximum()
        y_max = self.__m_node_map_remote_device.FindNode("Height").Maximum()

        return (x_min, x_max, y_min, y_max)

    def set_exposure(self, exposure):
        """
        Sets the exposure time for the camera.

        Args:
            exposure (int): Desired exposure time in microseconds.
        """

        exposure = int(exposure * 1000000)  # convert to usec
        self.__m_node_map_remote_device.FindNode("ExposureTime").SetValue(
            exposure
        )

    def set_auto_exposure(self, auto):
        """
        Enables or disables automatic exposure control.

        Args:
            auto (bool): If True, enables automatic exposure; otherwise, disables it.
        """

        pass

    def get_exposure(self):
        """
        Retrieves the current exposure time setting.

        Returns:
            int: The current exposure time in microseconds.
        """

        logger.info(
            "Exposure Time units: %s",
            self.__m_node_map_remote_device.FindNode("ExposureTime").Unit(),
        )
        return self.__m_node_map_remote_device.FindNode("ExposureTime").Value()

    def get_exposure_range(self):
        """
        Provides the minimum, maximum, and step increment for exposure settings.

        Returns:
            tuple: A tuple containing the minimum exposure, maximum exposure, and increment.
        """

        min_exp = self.__m_node_map_remote_device.FindNode("ExposureTime").Minimum()
        max_exp = self.__m_node_map_remote_device.FindNode("ExposureTime").Maximum()
        increment = self.__m_node_map_remote_device.FindNode("ExposureTime").Increment()
        return (min_exp, max_exp, increment)

    def set_gain(self, gain):
        """
        Sets the gain level for the camera.

        Args:
            gain (float): The desired gain level.
        """

        self.__m_node_map_remote_device.FindNode("Gain").SetValue(gain)

    def set_auto_gain(self, auto: bool):
        """
        Enables or disables automatic gain control.

        Args:
            auto (bool): If True, enables automatic gain; otherwise, disables it.
        """

        self.__m_node_map_remote_device.FindNode("GainAuto").SetValue(auto)

    def get_gain(self):
        """
        Retrieves the current gain level setting.

        Returns:
            float: The current gain level.
        """

        return self.__m_node_map_remote_device.FindNode("Gain").Value()

    def get_gain_range(self):
        """
        Provides the minimum, maximum, and step increment for gain settings.

        Returns:
            tuple: A tuple containing the minimum gain, maximum gain, and increment.
        """
        
        min_gain = self.__m_node_map_remote_device.FindNode("Gain").Minimum()
        max_gain = self.__m_node_map_remote_device.FindNode("Gain").Maximum()
        increment = 1
        return (min_gain, max_gain, increment)

    # -------------------------

    # IDS specific methods
    def _open_camera(self, cam_id):
        # Create instance of the device manager
        device_manager = peak.DeviceManager.Instance()

        # Update the device manager
        device_manager.Update()

        # Return if no device was found
        if device_manager.Devices().empty():
            return False

        # open the device specified by cam_id in the device manager's device list
        device_count = device_manager.Devices().size()
        if cam_id >= device_count:  # not enough cameras found
            return False
        else:
            # sort by serial number, else order determined by which cam was plugged in first
            sn = []
            for m_dev in device_manager.Devices():
                # m_node_map.FindNode("DeviceSerialNumber").Value())
                sn.append(m_dev.SerialNumber())

            sort_ind = np.argsort(sn)
            self.__m_device = device_manager.Devices()[
                int(sort_ind[cam_id])
            ].OpenDevice(
                peak.DeviceAccessType_Control
            )  # can't use sort_ind of type np.int64 directly!!!
            self.__m_node_map_remote_device = self.__m_device.RemoteDevice().NodeMaps()[
                0
            ]

            return True

    def _prepare_acquisition(self):
        self.__m_node_map_remote_device.FindNode("AcquisitionMode").SetCurrentEntry(
            "Continuous"
        )
        self.__m_node_map_remote_device.FindNode("TriggerSelector").SetCurrentEntry(
            "ExposureStart"
        )
        self.__m_node_map_remote_device.FindNode("TriggerMode").SetCurrentEntry("On")
        self.__m_node_map_remote_device.FindNode("TriggerSource").SetCurrentEntry(
            "Software"
        )

        self.__m_node_map_remote_device.FindNode("ExposureTime").SetValue(
            300
        )  # self.parameters.t_exp*1000000)    # t_exp in sec but "ExposureTime" in usec

        data_streams = self.__m_device.DataStreams()
        if data_streams.empty():
            # no data streams available
            return False
        self.__m_dataStream = self.__m_device.DataStreams()[0].OpenDataStream()
        return True

    def _alloc_and_announce_buffers(self):
        if self.__m_dataStream:
            # Flush queue and prepare all buffers for revoking
            self.__m_dataStream.Flush(peak.DataStreamFlushMode_DiscardAll)

            # Clear all old buffers
            for buffer in self.__m_dataStream.AnnouncedBuffers():
                self.__m_dataStream.RevokeBuffer(buffer)

            payload_size = self.__m_node_map_remote_device.FindNode(
                "PayloadSize"
            ).Value()

            # Get number of minimum required buffers
            num_buffers_min_required = (
                self.__m_dataStream.NumBuffersAnnouncedMinRequired()
            )

            # Alloc buffers
            for count in range(num_buffers_min_required):
                buffer = self.__m_dataStream.AllocAndAnnounceBuffer(payload_size)
                self.__m_dataStream.QueueBuffer(buffer)

            return True

        else:
            return False

    def _acquire_continuous(self, t_sleep=0):
        while not self.killswitch.is_set():
            try:
                arr = self._get_frame()
                # arr *= (
                #     256  # _get_frame returns 8-bit image but frame_queue expects 16-bit
                # )
                self.frame_queue.put(arr)
                time.sleep(t_sleep)

                # with open('temperature_log.csv', "a") as file:
                #     file.write(str([time.time(), self.__m_node_map_remote_device.FindNode("DeviceTemperature").Value()])[1:-1])
                #     file.write("\n")

            except Exception as e:
                logger.error("Error: %s", e)
                break
        self.frame_queue.put(None)

    def _get_frame(self):
        # self.__alloc_and_announce_buffers()
        # self.__start_acquisition()
        self.__m_node_map_remote_device.FindNode("TriggerSoftware").Execute()

        # Get buffer from device's DataStream. Wait 5000 ms. The buffer is automatically locked until it is queued again.
        buffer = self.__m_dataStream.WaitForFinishedBuffer(5000)
        img = ids_peak_ipl.Image.CreateFromSizeAndBuffer(
            buffer.PixelFormat(),
            buffer.BasePtr(),
            buffer.Size(),
            buffer.Width(),
            buffer.Height(),
        )
        img = img.ConvertTo(
            ids_peak_ipl.PixelFormatName_Mono8, ids_peak_ipl.ConversionMode_Fast
        )
        img_arr = np.array(img.get_numpy_2D(), dtype=np.uint16)
        img_arr = self._crop_frame(img_arr)
        # img_arr = self._transform_frame(img_arr)

        # self.__stop_acquisition()
        # Queue buffer again
        self.__m_dataStream.QueueBuffer(buffer)

        self.latest_frame = img_arr
        return img_arr
    
    def _crop_frame(self, frame):
        # return frame[self.x_crop: self.x_crop + self.width_crop, self.y_crop: self.y_crop + self.height_crop]
        return frame[
            self.y_crop : self.y_crop + self.height_crop,
            self.x_crop : self.x_crop + self.width_crop,
        ]
