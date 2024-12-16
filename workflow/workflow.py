from tifffile import imwrite
import numpy as np
import time
import threading
import queue
import traceback
import os
import wx

from events.events import PLOT_UPDATE
from utils.config_tool import update_config_by_dict

import numpy as np
from numpy.polynomial import polynomial as poly

from scipy.ndimage import center_of_mass
from scipy.signal import correlate2d
from scipy.optimize import curve_fit

from workflow.parameters import Parameters

import logging

logger = logging.getLogger(__name__)

DUMMY_FRAME_PIXEL_SIZE = 1000


class Workflow(threading.Thread):
    """Class implements initialization and run of sample lock procedure.

    Parameters
    ----------
    stage : object
        stage object
    n_points : int, optional
        number of points to be acquired per plot update (default: 1)
    save_parms : bool, optional
        whether to save parameters to file (default: False)
    parameters : dict, optional
        dictionary of parameters (default: None)
    data_params : dict, optional
        dictionary of data parameters (default: dict({'save_dat': True, 'save_frames': False, 'dir_path': os.path.join(os.getcwd(), 'data')}))
    frame_queue : queue, optional
        queue for frames (default: None)
    evt_catcher : object, optional
        event catcher object (default: None)
    """

    def __init__(
        self,
        *args,
        stage=None,
        n_points=1,
        save_parms=False,
        parameters=None,
        data_params=dict(
            {
                # "writing_mode": "append", # <----- Remove it                "save_dat": True,
                "save_frames": False,
                "dir_path": os.path.join(os.getcwd(), "data"),
            }
        ),
        frame_queue=None,
        evt_catcher=None,
        **kw,
    ):
        threading.Thread.__init__(self)
        self.killswitch = threading.Event()
        self.frame_queue = frame_queue
        self.evt_catcher = evt_catcher

        self.data_params = data_params
        self.file_name = "sampleLock_0"
        self.n_points = n_points
        self.save_parms = save_parms
        # self.warm_up = warm_up

        self.stage = stage
        try:
            self.n_cams = len(self.frame_queue)
        except:
            self.n_cams = 1

        self.parameters = Parameters(parameters)

        self.n_axes = len(self.stage.axes)

        self.pos_init = self.stage.get_position()
        self.pos_init_start = self.stage.get_position()

        self.drifts_init = None
        self.frames_init = None

        self.err_int = np.zeros(self.n_axes)
        self.err_int2 = np.zeros(self.n_axes)

    def stop(self):
        self.killswitch.set()
        if self.is_alive():
            self.join()

    def run(self):
        """run sample lock procedure"""

        logger.info("WORFLOW: Creating data directories")
        self.create_data_dirs()

        logger.info("WORFLOW: Calibrating sample lock")
        self.initialize()

        logger.info("WORFLOW: Starting sample lock")
        self.start_sample_lock()

    def create_data_dirs(self):  # <----- Should be moved to a different class
        path = self.data_params["dir_path"]

        if os.path.exists(path):
            new_dir_path = os.path.join(path, time.strftime("%Y-%m-%d_%H-%M-%S"))
        else:
            logger.warning(
                "Data directory does not exist. Creating new directory in current working directory."
            )
            new_dir_path = os.path.join(os.getcwd(), time.strftime("%Y-%m-%d_%H-%M-%S"))

        if not os.path.exists(new_dir_path):
            os.makedirs(new_dir_path)

        if self.save_parms:
            logger.info("WORFLOW: self.parameters.__dict__: ", self.parameters.param)
            print("Parameters dict:", self.parameters.param)
            update_config_by_dict(
                os.path.join(new_dir_path, "sample_lock_params.txt"),
                "sample_lock",
                self.parameters.param,
            )
        if self.data_params["save_frames"]:
            logger.info(
                "WORFLOW: Save frames parameter is set to True. Creating subdirectories for frames."
            )
            # Get list of all subdirectories in the current one and check if any of them is named  sampleLock_{number}_frames_reference
            subdirs = [f.path for f in os.scandir(new_dir_path) if f.is_dir()]
            subdirs = [
                f for f in subdirs if f.split("\\")[-1].startswith("sampleLock_")
            ]
            subdirs = [
                f for f in subdirs if f.split("\\")[-1].endswith("_frames_reference")
            ]
            if len(subdirs) > 0:
                # Get the number of the last subdirectory and increment it by 1
                last_subdir = subdirs[-1]
                last_subdir_num = int(last_subdir.split("\\")[-1].split("_")[1])
                self.file_name = "sampleLock_{}".format(last_subdir_num + 1)
            os.makedirs(
                os.path.join(new_dir_path, self.file_name + "_frames_reference")
            )
            os.makedirs(os.path.join(new_dir_path, self.file_name + "_frames_raw"))

        self.data_dir_root = new_dir_path

    def initialize(self):
        """initialize sample lock, i.e. acquire reference stacks for all axes (and potentially process frames for z-drift calculation)"""

        self.frames_init = (
            self._get_cam_frames()
        )  # acquire frames at user-selected locking position before reference stacks are acquired

        reference_stacks = []

        for ax in self.stage.axes:

            if hasattr(
                self.parameters.initial_range, "__iter__"
            ):  # could have different ranges for different axes

                initial_range = float(self.parameters.initial_range[int(ax) - 1])
            else:
                initial_range = float(self.parameters.initial_range)

            d_pos = np.linspace(
                -initial_range / 2,
                initial_range / 2,
                int(initial_range / self.parameters.initial_step),
            )

            cal_stack_ax = []

            current_directory = os.path.join(
                self.data_dir_root, self.file_name + "_frames_reference"
            )

            for pos in self.pos_init[ax] + d_pos:
                if self.stage.move_to(ax, pos):
                    self.stage.wait_settled(delay=0.1)
                    frames = self._get_cam_frames()
                    if self.data_params["save_frames"]:
                        ax_path = os.path.join(
                            current_directory, "axis_{}".format(ax)
                        )  # Create subdir in "sampleLock_{number}_frames_reference" for each axis

                        for i in range(self.n_cams):
                            cam_path = os.path.join(
                                ax_path, "camera{}".format(i)
                            )  # Create subdir for each camera

                            if not os.path.exists(cam_path):
                                os.makedirs(cam_path)
                            frame_path = os.path.join(
                                cam_path,
                                "stagePos_{:.0f}nm_camera{}.tiff".format(1000 * pos, i),
                            )  # Save frames with stage position in filename

                            imwrite(
                                frame_path, frames[i].astype(np.uint16)
                            )  # always save frames as uint16 regardless of camera data type

                    frames = [
                        self._normalize_array(f, mode="sum") for f in frames
                    ]  # normalization seems to be crucial for optimum performance!!
                    cal_stack_ax.append(frames)

                else:
                    logger.error(
                        "WORFLOW: Initialization failed. Stage limits reached."
                    )
                    return False

            self.stage.move_to(ax, self.pos_init[ax])
            self.stage.wait_settled(delay=0.1)

            cal_stack_ax = np.asarray(cal_stack_ax)
            if (
                ax == "3"
            ):  # might move this up to acquisition of stacks if post-acquisition proessing not required
                frames_sorted = [
                    [np.sort(cam.flatten()) for cam in plane] for plane in cal_stack_ax
                ]

                reference_stacks.append(np.array(frames_sorted))

            else:
                reference_stacks.append(cal_stack_ax)

        self.reference_stacks = reference_stacks  # don't convert to numpy array because length might be different along different axes
        return True

    def start_sample_lock(self):
        """to be called after self.initialize(); continuously acquires frames and updates stage position until stopped by user"""

        self.drifts_init = self._estimate_drifts(self.frames_init)

        ############################################ <----- Should be moved to a different class
        if self.data_params["save_frames"]:
            for i in range(self.n_cams):
                frame_dir = os.path.join(
                    self.data_dir_root,
                    self.file_name + "_frames_raw",
                    "frames_init",
                    "camera{}".format(i),
                )
                if not os.path.exists(frame_dir):
                    os.makedirs(frame_dir)
                frame_path = os.path.join(
                    frame_dir, "frame_init_camera{}.tiff".format(i)
                )

                imwrite(
                    frame_path,
                    self.frames_init[i].astype(np.uint16),
                )

        t_start = time.time()
        t_old = t_start
        stage_pos = np.zeros(self.n_axes)
        # sample_lock_active = True
        sample_lock_counter = 0

        cycle_counter = 1
        qstp, qerr, qdt = [], [], []

        if self.data_params["save_frames"]:
            for i in range(self.n_cams):
                os.path.join(
                    self.data_dir_root,
                    self.file_name + "_frames_raw",
                    "camera{}".format(i),
                )
        ############################################
        t_start = time.time()
        t_old = t_start
        stage_pos = np.zeros(self.n_axes)
        sample_lock_counter = (
            0  # counts the number of frames iterations since the start of sample lock
        )

        cycle_counter = 1  # this value tracks the number of data acquisition cycles that have been completed since the last plot update (plotting batch size is set by self.n_points)
        qstp, qerr, qdt = [], [], []

        while not self.killswitch.is_set():
            t_new = time.time()
            dt = t_new - t_old
            t_elapsed = t_new - t_start
            t_old = t_new

            frames = self._get_cam_frames() 


            if self.data_params["save_frames"]:

                for i in range(self.n_cams):
                    frame_dir = os.path.join(
                        self.data_dir_root,
                        self.file_name + "_frames_raw",
                        "camera{}".format(i),
                    )
                    if not os.path.exists(frame_dir):
                        os.makedirs(frame_dir)
                    frame_path = os.path.join(
                        frame_dir,
                        "frame_{:08d}_camera{}.tiff".format(sample_lock_counter, i),
                    )

                    imwrite(
                        frame_path,
                        frames[i].astype(np.uint16),
                    )  # always save frames as uint16 regardless of camera data type

            try:
                drifts = self._estimate_drifts(
                    frames
                )  # _estimate_drifts() contains algortihms for drift estimation
            except Exception:
                logger.error(traceback.format_exc())

            self._set_reference_pos(t_elapsed, dt)

            err = (
                np.array(self.parameters.scale_factors)
                * (self.drifts_init - drifts)
                * self.parameters.initial_step
            )  # might want to change signs along axes depending on relative orientation of stage and camera

            if hasattr(
                self, "d_err"
            ):  # d_err is defined for certain reference modes by _set_reference_pos() to generate offsets to error signals
                ind_ax_ref = (
                    int(self.parameters.reference_axis) - 1
                )  # stage axes are 1-indexed strings, err is 0-indexed array
                err[ind_ax_ref] += self.d_err * float(
                    self.parameters.scale_factors[ind_ax_ref]
                )

            self.err_int += err * dt  # integrate error
            self.err_int2 += self.err_int * dt  # second-order integrator

            for i, ax in enumerate(self.stage.axes):
                if ax in self.parameters.sample_lock_active_axes:
                    stage_pos[i] = (
                        self.pos_init[ax]
                        + self.parameters.kp * err[i]
                        + self.parameters.ki * self.err_int[i]
                        + self.parameters.ki2 * self.err_int2[i]
                    )
                else:
                    stage_pos[i] = self.pos_init[ax]

                # add feed-forward for improved tracking of error offsets
                # <----- evaluate if this will be used in paper, else remove
                if hasattr(self, "d_err") and ax == self.parameters.reference_axis:
                    kforward = 1
                    stage_pos[i] += self.d_err * kforward

                if not self.stage.move_to(ax, stage_pos[i]):
                    logger.warning(
                        "WORFLOW: Stage limits reached for axis {ax}: {stage_pos}".format(
                            ax=ax, stage_pos=stage_pos[i]
                        )
                    )
                    # warnings.warn("Sample lock hit stage limit.")
                    stage_pos[i] = (
                        self.stage.stage_limits[ax][0]
                        if stage_pos[i] < 0
                        else self.stage.stage_limits[ax][1]
                    )
                    # to prevent integrator windup
                    self.err_int2 -= self.err_int * dt
                    self.err_int -= err * dt

            # add data to queue for plotting
            qstp.append(np.copy(stage_pos))
            qerr.append(np.copy(err))
            qdt.append(t_elapsed)

            if cycle_counter >= self.n_points:
                cycle_counter = 1
                wx.QueueEvent(self.evt_catcher, PLOT_UPDATE(pos=qstp, err=qerr, dt=qdt))
                qstp, qerr, qdt = [], [], []
            cycle_counter += 1

            # format data for saving to csv file
            data = [*stage_pos, *err, t_elapsed]
            data_str = str(data)[1:-1]

            data_file_path = os.path.join(self.data_dir_root, self.file_name + ".csv")
            with open(data_file_path, "a") as file:
                file.write(data_str + "\n")

            time.sleep(self.parameters.t_settle)
            sample_lock_counter += 1

    def _get_cam_frames(
        self,
    ):  # <----- Should support any ammount of queues. Currently only supports 1 queue
        """return a list of arrays corresponding to frames of all active cameras, cropped to ROI"""

        frames = []

        for each in self.frame_queue:
            que, request_fn = each
            request_fn()  # <------ send signal to frame proccessor thread to get a frame
            try:
                frame = que.get(timeout=1)
                que.task_done()
            except queue.Empty:
                logger.error("WORFLOW: No frames received")
                self.killswitch.set()
                wx.PostEvent(self.evt_catcher, wx.PyCommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, self.evt_catcher.start_sl_btn.GetId()))
                frame = np.zeros((DUMMY_FRAME_PIXEL_SIZE, DUMMY_FRAME_PIXEL_SIZE))
                
            frames.append(frame)
        
        return frames

    def _set_reference_pos(self, t_elapsed, dt):
        """
        set reference position according to specified reference mode (for example to test step response or tracking of ramp etc.)

        Parameters
        ----------
        t_elapsed : float
            time elapsed since start of sample lock
        dt : float
            time elapsed since last iteration of sample lock

        Returns
        -------
        integer encoding reference mode
        """

        # reference position is not altered (stays the same as the initial position when engaging sample lock); default mode for sample stabilization (others just for evaluating performance)
        if self.parameters.reference_mode == "constant":
            return 0

        # reference position is altered by a step of specified amplitude and duration (to oberserve how the system responds to a step input)
        elif self.parameters.reference_mode == "step":
            if not hasattr(self, "step_counter"):
                self.step_counter = 0

            if t_elapsed // self.parameters.move_time != self.step_counter:
                if self.step_counter % 2 == 0:
                    self.pos_init[
                        self.parameters.reference_axis
                    ] += self.parameters.move_amplitude
                else:
                    self.pos_init[
                        self.parameters.reference_axis
                    ] -= self.parameters.move_amplitude
                self.step_counter += 1

            return 1

        # reference position is altered by a linear ramp of specified amplitude and duration
        elif self.parameters.reference_mode == "triangle":
            if not hasattr(self, "triangle_counter"):
                self.triangle_counter = 0

            if (
                t_elapsed + self.parameters.move_time / 2
            ) // self.parameters.move_time != self.triangle_counter:
                self.triangle_counter += 1

            if self.triangle_counter % 2 == 0:
                self.pos_init[self.parameters.reference_axis] += (
                    2 * self.parameters.move_amplitude * dt / self.parameters.move_time
                )  # pk-pk = 2 * amplitude!
            else:
                self.pos_init[self.parameters.reference_axis] -= (
                    2 * self.parameters.move_amplitude * dt / self.parameters.move_time
                )

            return 2

        elif self.parameters.reference_mode == "circle":
            assert (
                len(self.parameters.reference_axis) == 2
            ), "Circle reference mode requires two axes to be specified."

            self.pos_init[self.parameters.reference_axis[0]] = self.pos_init_start[
                self.parameters.reference_axis[0]
            ] + self.parameters.move_amplitude * np.cos(
                2 * np.pi * t_elapsed / self.parameters.move_time
            )
            self.pos_init[self.parameters.reference_axis[1]] = self.pos_init_start[
                self.parameters.reference_axis[1]
            ] + self.parameters.move_amplitude * np.sin(
                2 * np.pi * t_elapsed / self.parameters.move_time
            )

            return 3

        elif self.parameters.reference_mode == "sine":
            self.pos_init[self.parameters.reference_axis] = self.pos_init_start[
                self.parameters.reference_axis
            ] + self.parameters.move_amplitude * np.sin(
                2 * np.pi * t_elapsed / self.parameters.move_time
            )
            return 4

        # same as "step" mode, but change error instead of reference position
        elif self.parameters.reference_mode == "step_error":
            if not hasattr(self, "step_counter"):
                self.step_counter = 0
                self.d_err = 0

            if t_elapsed // self.parameters.move_time != self.step_counter:
                if self.step_counter % 2 == 0:
                    self.d_err += self.parameters.move_amplitude
                else:
                    self.d_err -= self.parameters.move_amplitude
                self.step_counter += 1

            return 5

        # same as "triangle" mode, but change error instead of reference position
        elif self.parameters.reference_mode == "triangle_error":
            if not hasattr(self, "triangle_counter"):
                self.triangle_counter = 0
                self.d_err = 0

            if (
                t_elapsed + self.parameters.move_time / 2
            ) // self.parameters.move_time != self.triangle_counter:
                self.triangle_counter += 1

            if self.triangle_counter % 2 == 0:
                self.d_err += (
                    2 * self.parameters.move_amplitude * dt / self.parameters.move_time
                )  # pk-pk = 2 * amplitude!
            else:
                self.d_err -= (
                    2 * self.parameters.move_amplitude * dt / self.parameters.move_time
                )

            return 6

    def _estimate_drifts(self, current_frames):
        """
        extract drifts from frames while sample lock is enabled

        Parameters
        ----------
        current_frames : TYPE
            camera frames as list of each camera's frame (as returned by self._get_cam_frames()).

        Raises
        ------
        ValueError
            DESCRIPTION.

        Returns
        -------
        calculated drifts to be converted to updated stage position by feedback loop (in units of reference stack indices)

        """
        drifts = np.zeros(self.n_axes)

        ### xy drift calculation
        for i in range(2):
            n_steps = len(self.reference_stacks[i])
            corr_stack_ax = np.zeros(n_steps)

            # calculate the correlation of the current frame(s) with each frame in the reference stack for x and y
            for j in range(n_steps):
                corr_plane = [
                    correlate2d(
                        current_frames[k],
                        self.reference_stacks[i][j, k],
                        mode="valid",
                    )  # since both frames are the same size, the result is a single value
                    for k in range(self.n_cams)
                ]
                corr_stack_ax[j] = np.average(
                    corr_plane
                )  # in case of multiple cameras, average correlation over all cameras

            corr_stack_ax = self._normalize_array(
                corr_stack_ax, mode="range"
            )  # normalize correlation stack to range (0, 1)

            # calculate drift by centroid or Gaussian fit as specified by user
            if self.parameters.peak_fit == "centroid":
                drifts[i] = center_of_mass(corr_stack_ax)[0]
            elif self.parameters.peak_fit == "gauss":
                drifts[i] = self._fit_gauss_1D(corr_stack_ax)
            else:
                raise ValueError('Wrong "peak_fit" parameter.')

        ### z drift calculation
        # process current frame(s) the same way as z reference stack frames (normalize and sort by pixel value)
        frames_normalized = [
            self._normalize_array(f, mode="sum") for f in current_frames
        ]
        frames_sorted_current = [np.sort(f.flatten()) for f in frames_normalized]

        # calculate mean squared error (MSE) between current frame(s) and each frame in the z reference stack asa measure of similarity
        n_steps_z = self.reference_stacks[2].shape[
            0
        ]  # shape of z reference stack is (n_step, n_cam, n_px)
        mse = np.zeros((n_steps_z, self.n_cams))
        for i in range(n_steps_z):
            for j in range(self.n_cams):
                d = self.reference_stacks[2][i, j] - frames_sorted_current[j]
                mse[i, j] = np.average(d**2)
        mse_avg = np.average(mse, axis=1)  # for multiple cameras, average over all
        mse_norm = self._normalize_array(
            -mse_avg, mode="range"
        )  # normalize to (0, 1) after multiplication by -1 to fit peak instead of dip

        # fit peak of MSE to get drift along z
        if self.parameters.peak_fit == "centroid":
            drifts[2] = center_of_mass(mse_norm)[0]
        elif self.parameters.peak_fit == "gauss":
            drifts[2] = self._fit_gauss_1D(mse_norm)

        return drifts

    def _normalize_array(self, array, mode="sum"):
        """normalize array
        Parameters
        ----------
        array : np.array
            array to be normalized
        mode : str, optional
            normalization mode, by default "sum"
            "sum" - normalize by dividing by sum of all pixel values
            "range" - normalize by scaling to range (0, 1)
        Returns
        -------
        np.array
            normalized array
        """
        if mode == "sum":
            arr_norm = array / np.sum(array)
        elif mode == "range":
            d_arr = np.max(array) - np.min(array)
            if d_arr != 0:
                arr_norm = (array - np.min(array)) / d_arr
            else:
                # warnings.warn("Array values all equal. Cannot normalize.")
                arr_norm = array
        else:
            raise ValueError(
                'Invalid mode in _normalize_array. Valid modes are "sum" and "range".'
            )
        return arr_norm

    def _fit_gauss_1D(self, data):
        """fit 1D array to Gaussian using scipy's curve_fit"""
        n = len(data)
        # fit parameters: x0 - peak position, s - standard deviation, a - amplitude
        f_gauss = (
            lambda x, x0, s, a: a / np.sqrt(s) * np.exp(-((x - x0) ** 2) / (2 * s**2))
        )
        # initial guess for fit parameters and bounds based on data (important for robustness of fit)
        p0 = [data.argmax(), n / 2, data.sum()]
        fit_lim = ([-1, n / 10, data.min()], [n + 1, 10 * n, n * data.max()])
        x = np.arange(n)
        try:
            fit_res = curve_fit(f_gauss, x, data, p0=p0, bounds=fit_lim)[0]
        except Exception as e:  # <----- implement proper exception handling
            logger.error(e)
            raise RuntimeError(e)

        return fit_res[0]  # return peak position
