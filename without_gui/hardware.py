# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 11:01:07 2023

@author: danzloptics_admin
"""

from ids_peak import ids_peak as peak
from ids_peak_ipl import ids_peak_ipl
from pyAndorSDK2 import atmcd, atmcd_codes, atmcd_errors

from pipython import GCSDevice, pitools

import numpy as np
from scipy.ndimage import rotate, zoom, shift, affine_transform
import time
from warnings import warn


class Camera_IDS:
    def __init__(self, camera_parameters):

        
        peak.Library.Initialize()

        self.parameters = camera_parameters
        # self.t_exp = t_exp
        # self.roi = roi
        # self.transform_parameters = [rotation_angle]

        if not self.__open_camera(self.parameters.cam_id):
            raise RuntimeError("Opening camera failed.")

        if not self.__prepare_acquisition():
            raise RuntimeError("Preparing camera acquisition failed.")

        if self.parameters.roi is not None:
            if not self.__set_roi(*self.parameters.roi):
                raise RuntimeError("Setting ROI failed.")

        if not self.__alloc_and_announce_buffers():
            raise RuntimeError("Buffer allocation failed.")

        if not self.__start_acquisition():
            raise RuntimeError("Starting camera acquisition failed.")

        self.__m_node_map_remote_device.FindNode("ExposureTime").SetValue(
            self.parameters.t_exp * 1000000
        )  # t_exp in sec but "ExposureTime" in usec

        print("Camera set up successfully.")

    # def __del__(self):
    #     peak.Library.Close()

    def __open_camera(self, cam_id):
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
                sn.append(
                    m_dev.SerialNumber()
                )  # m_node_map.FindNode("DeviceSerialNumber").Value())

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

    def __prepare_acquisition(self):
        # self.__m_node_map_remote_device.FindNode("AcquisitionMode").SetCurrentEntry("SingleFrame")
        # self.__m_node_map_remote_device.FindNode("TriggerSelector").SetCurrentEntry("ExposureStart")
        # self.__m_node_map_remote_device.FindNode("TriggerMode").SetCurrentEntry("Off")

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

        data_streams = self.__m_device.DataStreams()
        if data_streams.empty():
            # no data streams available
            return False
        self.__m_dataStream = self.__m_device.DataStreams()[0].OpenDataStream()
        return True

    def __set_roi(self, x, y, width, height):
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
        h_max = self.__m_node_map_remote_device.FindNode("Height").Maximum()

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
            width_roi = (
                width - width % 8 + 16
            )  # + 16: up to 8 subtracted from width%8, leave 8 more for cropping
            self.width_crop = width
            height_roi = height - height % 8 + 16
            self.height_crop = height

            # Now, set final AOI
            self.__m_node_map_remote_device.FindNode("OffsetX").SetValue(x_roi)
            self.__m_node_map_remote_device.FindNode("OffsetY").SetValue(y_roi)
            self.__m_node_map_remote_device.FindNode("Width").SetValue(width_roi)
            self.__m_node_map_remote_device.FindNode("Height").SetValue(height_roi)

            # re-allocate buffer for changed ROI
            self.__alloc_and_announce_buffers()

            return True

    def __alloc_and_announce_buffers(self):
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

    def __start_acquisition(self):
        self.__m_dataStream.StartAcquisition(
            peak.AcquisitionStartMode_Default
        )  # , 1)#peak.DataStream.INFINITE_NUMBER)

        self.__m_node_map_remote_device.FindNode("TLParamsLocked").SetValue(1)
        self.__m_node_map_remote_device.FindNode("AcquisitionStart").Execute()
        self.__m_node_map_remote_device.FindNode("AcquisitionStart").WaitUntilDone()

        return True

    def __stop_acquisition(self):
        self.__m_node_map_remote_device.FindNode("AcquisitionStop").Execute()
        self.__m_node_map_remote_device.FindNode("AcquisitionStop").WaitUntilDone()
        self.__m_node_map_remote_device.FindNode("TLParamsLocked").SetValue(0)
        self.__m_dataStream.StopAcquisition(peak.AcquisitionStopMode_Default)

    def _crop_frame(self, frame):
        # return frame[self.x_crop: self.x_crop + self.width_crop, self.y_crop: self.y_crop + self.height_crop]
        return frame[
            self.y_crop : self.y_crop + self.height_crop,
            self.x_crop : self.x_crop + self.width_crop,
        ]

    def _transform_frame(self, frame):
        if self.parameters.M_affine is not None:
            frame_trafo = affine_transform(frame, self.parameters.M_affine)
        else:
            frame_trafo = frame
            if (
                self.parameters.f_scale != 1
            ):  # could speed up by saving arrays instead of regenerating, decreasing zoom order
                frame_zoom = zoom(
                    frame_trafo, self.parameters.f_scale, output=float, order=3
                )
                if self.parameters.f_scale > 1:
                    dx = (frame_zoom.shape[0] - frame_trafo.shape[0]) // 2
                    dy = (frame_zoom.shape[1] - frame_trafo.shape[1]) // 2
                    frame_trafo = frame_zoom[
                        dx : dx + frame_trafo.shape[0], dy : dy + frame_trafo.shape[1]
                    ]
                else:
                    dx = (frame_trafo.shape[0] - frame_zoom.shape[0]) // 2
                    dy = (frame_trafo.shape[1] - frame_zoom.shape[1]) // 2
                    frame_trafo = np.median(frame_trafo) * np.ones(
                        frame_trafo.shape
                    )  # pad with constant values
                    frame_trafo[
                        dx : dx + frame_zoom.shape[0], dy : dy + frame_zoom.shape[1]
                    ] = frame_zoom

            if self.parameters.rotation_angle != 0:
                frame_trafo = rotate(
                    frame_trafo,
                    self.parameters.rotation_angle,
                    cval=np.median(frame_trafo),
                    reshape=False,
                )

            if self.parameters.flip_image:
                frame_trafo = frame_trafo[:, ::-1]

        return frame_trafo

    def get_frame(self):
        # self.__alloc_and_announce_buffers()
        # self.__start_acquisition()
        self.__m_node_map_remote_device.FindNode("TriggerSoftware").Execute()

        # Get buffer from device's DataStream. Wait 5000 ms. The buffer is automatically locked until it is queued again.
        buffer = self.__m_dataStream.WaitForFinishedBuffer(5000)
        img = ids_peak_ipl.Image_CreateFromSizeAndBuffer(
            buffer.PixelFormat(),
            buffer.BasePtr(),
            buffer.Size(),
            buffer.Width(),
            buffer.Height(),
        )
        img = img.ConvertTo(
            ids_peak_ipl.PixelFormatName_Mono8, ids_peak_ipl.ConversionMode_Fast
        )
        img_arr = np.array(img.get_numpy_2D(), dtype=np.float32)
        # img_arr = self._crop_frame(img_arr)
        # img_arr = self._transform_frame(img_arr)

        # self.__stop_acquisition()
        # Queue buffer again
        self.__m_dataStream.QueueBuffer(buffer)

        self.latest_frame = img_arr
        return img_arr

    def close(self):
        # if self.__m_dataStream is not None:
        #     for buffer in self.__m_dataStream.AnnouncedBuffers():
        #             self.__m_dataStream.RevokeBuffer(buffer)
           
        peak.Library.Close()



class Camera_Andor:
    def __init__(self, camera_parameters):
        self.parameters = camera_parameters
        self._sdk = atmcd(
            "C:\\Program Files\\Andor SDK\\Python\\pyAndorSDK2\\pyAndorSDK2\\libs\\Windows\\64"
        )
        self._sdk.Initialize("")

        self._prepare_acquisition()


    def __del__(self):
        self._sdk.CoolerOFF()
        self._sdk.ShutDown()

    def close(self):
        self._sdk.CoolerOFF()
        self._sdk.ShutDown()

    def get_frame(self):
        if self._sdk.SendSoftwareTrigger() != atmcd_errors.Error_Codes.DRV_SUCCESS:
            return False

        self._sdk.WaitForAcquisition()
        ret, img_arr = self._sdk.GetMostRecentImage16(self.n_px_x * self.n_px_y)
        img_arr = np.frombuffer(img_arr, dtype=np.uint16).reshape(
            self.n_px_y, self.n_px_x
        )

        self.latest_frame = img_arr
        return img_arr

    def _prepare_acquisition(self):
        if hasattr(self.parameters, "T_target"):
            T_target = self.parameters.T_target
        else:
            T_target = 0

        if not self.__camera_cooldown(T_target):
            raise RuntimeError("Camera cooldown failed.")

        if not self.__set_acquisition_parameters():
            raise RuntimeError("Setting up acquisition failed.")

        if self._sdk.StartAcquisition() != atmcd_errors.Error_Codes.DRV_SUCCESS:
            return RuntimeError('Acquisition could not be started.')

    def __camera_cooldown(self, T_target=-20, t_max=180):
        if T_target < -20:
            raise ValueError("camera cannot be cooled below -20 C")

        self._sdk.SetTemperature(T_target)
        ret = self._sdk.CoolerON()

        t0 = time.time()
        while ret != atmcd_errors.Error_Codes.DRV_TEMP_STABILIZED:
            time.sleep(2)
            ret, T = self._sdk.GetTemperature()
            if time.time() - t0 > t_max:
                return False

        return True

    def __set_acquisition_parameters(self):
        if (
            self._sdk.SetAcquisitionMode(atmcd_codes.Acquisition_Mode.RUN_TILL_ABORT)
            != atmcd_errors.Error_Codes.DRV_SUCCESS
        ):
            return False

        if (
            self._sdk.SetReadMode(atmcd_codes.Read_Mode.IMAGE)
            != atmcd_errors.Error_Codes.DRV_SUCCESS
        ):
            return False

        if (
            self._sdk.SetTriggerMode(atmcd_codes.Trigger_Mode.SOFTWARE_TRIGGER)
            != atmcd_errors.Error_Codes.DRV_SUCCESS
        ):
            return False

        roi = self.parameters.roi
        if roi is not None:
            self.n_px_x = roi[2]
            self.n_px_y = roi[3]
            if (
                self._sdk.SetImage(
                    1, 1, roi[0] + 1, roi[0] + roi[2], roi[1] + 1, roi[1] + roi[3]
                )
                != atmcd_errors.Error_Codes.DRV_SUCCESS
            ):
                return False
        else:
            ret, self.n_px_x, self.n_px_y = self._sdk.GetDetector()
            if (
                self._sdk.SetImage(1, 1, 1, self.n_px_x, 1, self.n_px_y)
                != atmcd_errors.Error_Codes.DRV_SUCCESS
            ):
                return False

        if (
            self._sdk.SetExposureTime(self.parameters.t_exp)
            != atmcd_errors.Error_Codes.DRV_SUCCESS
        ):
            return False

        if self.parameters.gain:
            if (
                self._sdk.SetEMCCDGain(self.parameters.gain)
                != atmcd_errors.Error_Codes.DRV_SUCCESS
            ):
                return False

        if self._sdk.PrepareAcquisition() != atmcd_errors.Error_Codes.DRV_SUCCESS:
            return False

        return True


class Stage:
    def __init__(self):
        pidevice = GCSDevice(
            devname="E-727", gcsdll="D:\\sampleLock_python\\PI_GCS2_DLL_x64.dll"
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

    def move(self, axis, position):
        if self.assert_stage_limits(axis, position):
            self.pidevice.MOV(axis, position)
            return True
        else:
            warn("Value outside range of stage. Movement not performed.")
            return False

    def step(self, axis, d_pos):
        pos = self.get_position()
        pos_new = pos[str(axis)] + d_pos
        if self.assert_stage_limits(axis, pos_new):
            self.pidevice.MOV(axis, pos_new)
            return True
        else:
            warn("Stage limit reached. Step not performed.")
            return False

    def close(self):
        self.pidevice.ATZ()
        pitools.waitonautozero(self.pidevice)
        self.pidevice.CloseConnection()
