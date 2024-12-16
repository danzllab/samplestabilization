# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 16:46:24 2023

@author: danzloptics_admin
"""


class CameraParameters:
    """
    camera parameters subclass; made sense for playing around with image transformations, might be discarded in the future
    """

    def __init__(
        self,
        cam_id,
        t_exp,
        roi=None,
        rotation_angle=0,
        flip_image=False,
        f_scale=1,
        bit_depth=8,
        gain=None,
    ):
        self.cam_id = cam_id  # sorted by serial number

        self.t_exp = t_exp
        self.roi = roi
        self.gain = gain

        self.M_affine = None
        self.rotation_angle = rotation_angle
        self.f_scale = f_scale
        self.flip_image = flip_image


class Parameters:
    def __init__(self, profile="default"):
        """


        Parameters
        ----------
        profile : which parameter profile to load'.

        Raises
        ------
        ValueError
            DESCRIPTION.

        Returns
        -------
        None.

        """
        if profile == "default":
            self.load_default_parameters()
        elif profile == "cryo":
            self.load_cryo_parameters()
        elif profile == "empty":
            self.create_empty_parameters()
        else:
            raise ValueError("Parameter profile not supported.")

    def load_default_parameters(self):
        self.camera_0 = CameraParameters(0, 0.1, roi=[590, 216, 700, 700])
        self.camera_1 = CameraParameters(
            1, 0.1, roi=[765, 332, 700, 700]
        )  # , f_scale=1.112,
        # rotation_angle=176.5, flip_image=True)
        # camera parameter ROI only compatible with certain values; crop to desired ones after readout
        self.roi_crop = [150, 200, 400, 350]

        self.init_range = (
            0.6  # range covered by calibration stacks (at present same for all axes)
        )
        self.init_step = (
            0.02  # step size for calibration stacks (at present same for all axes)
        )

        # options for different profiles of the reference position (step, triangle) to test performance of feedback
        self.reference_mode = "constant"
        self.reference_axis = "1"
        self.move_amplitude = 0.03
        self.move_time = 5

        # self.correlation_size = 300
        # self.correlation_steps = 10
        self.peak_fit = (
            "gauss"  # options to fit peak to Gauss or calculate position with centroid
        )

        self.sample_lock_active_axes = ["1", "2", "3"]  # ['1', '2', '3']
        self.scale_factors = [
            1,
            1.1,
            1.8,
        ]  # use same feedback parameters for all axes but multiply them with scale_factors to achieve suitable "strength" of feedback
        self.t_settle = 0.08  # time (in seconds) to wait for stage to settle after each step, before acquiring new camera frame and calculating new stage position
        self.kp = 0.2  # proportional feedback parameter
        self.ki = 2  # (first-order) integrator feedback parameter
        self.ki2 = 0.02  # (first-order) integrator feedback parameter

    def load_cryo_parameters(self):
        self.camera_0 = CameraParameters(0, 0.1, roi=[590, 216, 700, 700])

        self.camera_1 = CameraParameters(
            1, 0.1, roi=[765, 332, 700, 700]
        )  # , f_scale=1.112,
        # rotation_angle=176.5, flip_image=True)

        self.camera_andor = CameraParameters(
            0, 0.01, gain=10, roi=[400, 450, 300, 300])
        self.roi_crop = None  # [150, 200, 400, 350]

        self.init_range = 0.5*2
        self.init_step = 0.02*3

        self.reference_mode = "step"
        self.reference_axis = "3"

        self.move_amplitude = 0.05
        self.move_time = 5

        # self.correlation_size = 300
        # self.correlation_steps = 10
        self.peak_fit = "gauss"

        self.sample_lock_active_axes = []  # ['1', '2', '3']
        self.scale_factors = [1, 0.7, 0.4]
        self.t_settle = 0.08
        self.kp = 0.3
        self.ki = 1.5
        self.ki2 = 0.03

    def create_empty_parameters(self):
        self.t_exp_0 = None
        self.roi_0 = None
        self.t_exp_1 = None
        self.roi_1 = None

        self.init_range = None
        self.init_step = None

        self.setpoint = None
        self.move_amplitude = None
        self.move_period = None

        # self.correlation_size = None
        # self.correlation_steps = None

        self.sample_lock_active_axes = None
        self.scale_factors = None
        self.t_settle = None
        self.kp = None
        self.ki = None
        self.ki2 = None

    def save_all(self):
        """
        Save all parameters to file "sampleLock_params.txt".

        Returns
        -------
        None.

        """
        with open("..\\data\\sampleLock_params.txt", "w") as f:
            for param in self.__dict__:  # TODO save camera parameters properly!!
                f.write(f"{param}: {self.__dict__[param]}\n")
