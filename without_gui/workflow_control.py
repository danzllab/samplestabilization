# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 16:39:22 2023

@author: danzloptics_admin
"""

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import numpy as np
from numpy.polynomial import polynomial as poly

from scipy.ndimage import center_of_mass, gaussian_laplace
from scipy.signal import correlate2d
from scipy.optimize import curve_fit, least_squares
from scipy.interpolate import CubicSpline

from tifffile import imwrite
import time
import os
import shutil
import warnings

warnings.filterwarnings(
    "once", 'Invalid reference mode. Do nothing (same as "constant").'
)


class Workflow:
    def __init__(self, stage, cameras, parameters, file_write_mode="newfile"):
        self._create_file_name(file_write_mode)

        self.stage = stage
        self.cameras = cameras
        self.n_cams = len(self.cameras)
        self.parameters = parameters

        self.n_axes = len(self.stage.axes)
        self.pos_init = self.stage.get_position()

        self.err_int = np.zeros(self.n_axes)
        self.err_int2 = np.zeros(self.n_axes)

    def display_frames(self, frames, num=None, mode="split"):
        if mode == "overlay":
            fig, ax = plt.subplots(num=num, clear=True)

            frame_rgb = np.zeros((*frames[0].shape, 3), dtype=float)
            for i in range(self.n_cams):
                frame_rgb[:, :, i] = frames[i] / max(
                    1e-5, np.max(frames[0])
                )  # normalize camera frames (for float, range 0 to 1 in imshow), handle case where all pixels == 0

            plt.ion()
            plt.show()
            ax.imshow(frame_rgb)
            for i in range(self.n_cams):
                px_sat = np.argwhere(frames[i] == 255)
                ax.scatter(px_sat[:, 1], px_sat[:, 0], c=f"C{i}")
            plt.pause(0.2)

        elif mode == "difference":
            if len(frames) != 2:
                raise RuntimeError(
                    'Viewing frames in "difference" mode only enabled for 2 active cameras.'
                )
            fig, ax = plt.subplots(num=num, clear=True)
            plt.ion()
            plt.show()
            ax.imshow(frames[0] - frames[1], cmap="seismic")
            for i in range(2):
                px_sat = np.argwhere(frames[i] == 255)
                ax.scatter(px_sat[:, 1], px_sat[:, 0], c=f"C{i}")
            plt.pause(0.2)

        elif mode == "split":
            fig, ax = plt.subplots(1, self.n_cams, num=num, clear=True)
            if not hasattr(
                ax, "__iter__"
            ):  # want ax to be subsciptable even for single camera
                ax = [ax]

            plt.ion()
            plt.show()
            for i in range(self.n_cams):
                px_sat = np.argwhere(frames[i] == 255)

                h = ax[i].imshow(frames[i], cmap="inferno")  # , vmin=30, vmax=250)

                # add colorbar
                divider = make_axes_locatable(
                    ax[i]
                )  # this and next line needed for colorbar to match plot height
                cax = divider.append_axes("right", size="5%", pad=0.15)
                fig.colorbar(h, cax=cax)

                ax[i].scatter(px_sat[:, 1], px_sat[:, 0], c="r")

                ax[i].set_aspect("equal")

            plt.tight_layout()
            plt.pause(0.2)

    def position_stage(self, move_mode="absolute", show_cam_frames=True):
        """move stage to imaging position (i.e. find sample and focus); display updated frames every time after stage is moved"""
        if move_mode == "absolute":
            while True:
                ax = input(
                    'Enter axis ("c" to cancel without engaging sample lock, "i" to start initializing): '
                )
                if ax == "c":
                    return False
                elif ax == "i":
                    self.pos_init = self.stage.get_position()
                    return True

                if ax in self.stage.axes:
                    pos = input('Enter new position [um] ("c" to cancel): ')
                    if pos == "c":
                        pass
                    else:
                        try:
                            pos = float(pos)
                            if self.stage.assert_stage_limits(ax, pos):
                                self.stage.move(ax, pos)
                                if show_cam_frames:
                                    self.stage.wait_settled()
                                    frames = self._get_cam_frames()
                                    if not np.any([f is False for f in frames]):
                                       self.display_frames(frames, num=0)
                                    else:
                                       warnings.warn('Frame acqusition failed. Try again.')
                                       time.sleep(1)
                                       continue
                 else:
                                print(
                                    "Invalid value. Stage limits: ",
                                    self.stage.stage_limits[ax],
                                )
                        except ValueError:
                            print("Please enter a number.")
                else:
                    print("Invalid axis. Try again.")

        elif move_mode == "step":
            while True:
                d_step = input(
                    'Enter step size [um] ("c" to cancel without engaging sample lock, "i" to start initializing): '
                )
                if d_step == "c":
                    return False
                elif d_step == "i":
                    self.pos_init = self.stage.get_position()
                    return True

                try:
                    d_step = float(d_step)
                    print(
                        'Move stage ("q" to change step size/end stepping): \n \
                          "a"/"d" - move horizontal (x);\n \
                          "w"/"s" - move vertical (y);\n \
                          "e"/"r" - find focus (z);\n'
                    )
                    flag_step = True
                except ValueError:
                    flag_step = False
                    print("Step size must be number. Try again.")

                while flag_step:
                    print("Current postion: ", self.stage.get_position())
                    if show_cam_frames:
                        self.stage.wait_settled()
                        frames = self._get_cam_frames()
                        if not np.any([f is False for f in frames]):
                            self.display_frames(frames, num=0)
                        else:
                            warnings.warn('Frame acqusition failed. Try again.')
                            time.sleep(1)
                            continue

                    move_key = input("move key: ")
                    if move_key == "q":

                        flag_step = False
                    elif move_key == "a":
                        self.stage.step("2", -d_step)
                    elif move_key == "d":
                        self.stage.step("2", d_step)
                    elif move_key == "w":
                        self.stage.step("1", d_step)
                    elif move_key == "s":
                        self.stage.step("1", -d_step)
                    elif move_key == "e":
                        self.stage.step("3", -d_step)
                    elif move_key == "r":
                        self.stage.step("3", d_step)
                    else:
                        print("Invalid key. Try again.")

        else:
            raise ValueError(
                '"move_mode" must be "absolute" or "step". Stage positioning failed.'
            )
            return False

    # TODO evaluate if we can work without calibration
    def initialize(self, save_frames=False):
        """initialize sample lock, i.e. acquire calibration stacks for all axes (and potentially process frames for z-drift calculation)"""
        if save_frames:
            if os.path.exists(f"..\\data\\{self.file_name}_frames_calibration"):
                shutil.rmtree(f"..\\data\\{self.file_name}_frames_calibration")

        self.frames_init = (
            self._get_cam_frames()
        )  # acquire frames at user-selected locking position before calibration stacks are acquired
        calibration_stacks = []
        for ax in self.stage.axes:
            if hasattr(
                self.parameters.init_range, "__iter__"
            ):  # could have different ranges for different axes
                d_pos = np.linspace(
                    -self.parameters.init_range[ax] / 2,
                    self.parameters.init_range[ax] / 2,
                    int(self.parameters.init_range / self.parameters.init_step),
                )
            else:
                d_pos = np.linspace(
                    -self.parameters.init_range / 2,
                    self.parameters.init_range / 2,
                    int(self.parameters.init_range // self.parameters.init_step),
                )

            cal_stack_ax = []
            for pos in self.pos_init[ax] + d_pos:
                if self.stage.move(ax, pos):
                    self.stage.wait_settled(delay=0.1)
                    frames = self._get_cam_frames()
                    if save_frames:
                        if not os.path.exists(
                            f"..\\data\\{self.file_name}_frames_calibration\\axis_{ax}"
                        ):
                            for i in range(self.n_cams):
                                os.makedirs(
                                    f"..\\data\\{self.file_name}_frames_calibration\\axis_{ax}\\camera{i}"
                                )
                        for i in range(self.n_cams):
                            imwrite(
                                f"..\\data\\{self.file_name}_frames_calibration\\axis_{ax}\\camera{i}\\stagePos_{1000*pos:.0f}nm_camera{i}.tiff",
                                frames[i].astype(np.uint16),
                            )  # TODO make data type a camera parameter

                    # if ax != '3':
                    if True:
                        frames = [
                            self._normalize_array(f, mode="sum") for f in frames
                        ]  # seems to be crucial for optimum xy-performance!!
                    cal_stack_ax.append(frames)

                else:
                    print("Initialization failed. Stage limits reached.")
                    return False

            self.stage.move(ax, self.pos_init[ax])
            self.stage.wait_settled(delay=0.1)

            cal_stack_ax = np.asarray(cal_stack_ax)
            if (
                ax == "3"
            ):  # might move this up to acquisition of stacks if post-acquisition proessing not required
                frames_sorted = [
                    [np.sort(cam.flatten()) for cam in plane] for plane in cal_stack_ax
                ]

                calibration_stacks.append(np.array(frames_sorted))

            else:
                # stack_avg = np.average(cal_stack_ax, axis=1)    # might rethink this if cameras are not aligned; process both cams and average at the end might be superior
                calibration_stacks.append(cal_stack_ax)

        self.calibration_stacks = calibration_stacks  # don't convert to numpy array because  length might be different along different axes
        return True

    def run_sample_lock(self, auto_terminate=True, save_frames=False):
        """to be called after self.initialize(); continuously acquires frames and updates stage position until terminted with KeyboardInterrupt (Crtl + C)"""

        if hasattr(
            self, "frames_init"
        ):  # use frames at user-defined locking position (before acquisition of calibration stacks) as reference
            self.drifts_init = self._estimate_drifts(self.frames_init)
        elif not hasattr(
            self, "drifts_init"
        ):  # if no initial frames available, use acquire them now to be used as reference (not optimal because current position might slightly deviate from user-defined position)
            self.drifts_init = self._estimate_drifts(self._get_cam_frames())

        # M_crosstalk = np.array([[1, 0.4, 0],
        #                         [0.1, 1, 0],
        #                         [0, -1.3, 1]])

        if auto_terminate:
            err_abs_latest = np.zeros((self.n_axes, 100))
        t_start = time.time()
        t_old = t_start
        stage_pos = np.zeros(self.n_axes)
        sample_lock_active = True
        sample_lock_ctr = 0
        try:
            while sample_lock_active:

                frames = self._get_cam_frames()
                if np.any([f is False for f in frames]):  # skip iteration if frame acquisition failed
                    continue

                t_new = time.time()
                dt = t_new - t_old
                t_elapsed = t_new - t_start
                t_old = t_new

                plt.figure(3)
                for i in range(self.n_cams):
                    plt.plot(
                        t_elapsed,
                        np.sum(frames[i]) / np.sum(self.frames_init[i]),
                        color=f"C{i}",
                        alpha=0.5, 
                        linestyle='none', 
                        marker='o'
                    )
                    plt.plot(
                        t_elapsed,
                        np.min(frames[i]) / np.min(self.frames_init[i]),
                        color=f"C{i+5}",
                        alpha=0.5,
                        linestyle='none', 
                        marker='o'
                    )
                # print('frame grab time: ', time.time() - t_frame)

                if save_frames:
                    if sample_lock_ctr == 0:
                        if os.path.exists(f"..\\data\\{self.file_name}_frames_raw"):
                            shutil.rmtree(f"..\\data\\{self.file_name}_frames_raw")
                        for i in range(self.n_cams):
                            os.makedirs(
                                f"..\\data\\{self.file_name}_frames_raw\\camera{i}"
                            )
                    for i in range(self.n_cams):
                        imwrite(
                            f"..\\data\\{self.file_name}_frames_raw\\camera{i}\\frame_{sample_lock_ctr:08d}_camera{i}.tiff",
                            frames[i].astype(np.uint16),
                        )  # TODO make data type a camera parameter

                # t_est = time.time()
                drifts = self._estimate_drifts(frames)
                # print('estimation time: ', time.time() - t_est)

                err = (
                    np.array(self.parameters.scale_factors)
                    * (self.drifts_init - drifts)
                    * self.parameters.init_step
                )  # might want to change signs along axes depending on relative orientation of stage and camera
                if hasattr(self.parameters, "M_crosstalk"):
                    err = self.parameters.M_crosstalk @ err

                self.err_int += err * dt
                self.err_int2 += self.err_int * dt

                reference_state = self._set_reference_pos(t_elapsed, dt)

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
                    if not self.stage.move(ax, stage_pos[i]):
                        warnings.warn("Sample lock hit stage limit.")
                        stage_pos[i] = (
                            self.stage.stage_limits[ax][0]
                            if stage_pos[i] < 0
                            else self.stage.stage_limits[ax][1]
                        )
                        # to prevent integrator windup
                        self.err_int2 -= self.err_int * dt
                        self.err_int -= err * dt

                data = [*stage_pos, *err, t_elapsed]
                data_str = str(data)[1:-1]
                # file.write(data_str + '\n')
                # print(data_str)
                with open(f"..\\data\\{self.file_name}.csv", "a") as file:
                    file.write(data_str + "\n")

                if auto_terminate and (
                    reference_state == 0
                ):  # switch off auto_terminate for step response etc.
                    err_abs_latest[:, 1:] = err_abs_latest[:, :-1]
                    err_abs_latest[:, 0] = np.abs(err)
                    if err_abs_latest[:, -1].any() and np.median(
                        err_abs_latest[:, :50]
                    ) > 10 * np.median(
                        err_abs_latest[:, 50:]
                    ):  # err_abs_latest[:,-1].any() ensures that array has been filled
                        print(
                            "Auto-terminated sample lock because error increased too much."
                        )
                        sample_lock_active = False

                time.sleep(self.parameters.t_settle)
                sample_lock_ctr += 1

        except KeyboardInterrupt:
            sample_lock_active = False
            print("Sample lock terminated by KeyboardInterrupt.")
            print("Average sampling rate [Hz]: ", sample_lock_ctr / t_elapsed)
        except Exception as e:
            print(e)
        finally:
            frames_final = self._get_cam_frames()
            self.display_frames(frames_final, num=1)
            self.frames_final = frames_final
            # file.close()
            if sample_lock_active:
                return False
            else:
                return True

    # TODO parallelized acquisition would be optimal; look into multithreading or hardware trigger?
    def _get_cam_frames(self):
        """return a list of arrays corresponding to frames of all active cameras, cropped to ROI"""
        frames = [self.cameras[i].get_frame() for i in range(self.n_cams)]
        if self.parameters.roi_crop is None:
            return frames
        else:
            frames_cropped = []
            ind = self.parameters.roi_crop
            for f in frames:
                if f:
                    frames_cropped.append(f[ind[1]: ind[1] + ind[3], ind[0]: ind[0] + ind[2]])
                else:
                    frames_cropped.append(False)
            return frames_cropped

          
    def _create_file_name(self, write_mode="newfile"):
        """create file name to be used for saving data"""

        for i in range(10):
            file_name = f"sampleLock_{str(i)}"
            if os.path.exists(f"{file_name}.csv"):
                # file = open(file_name, 'a')
                if write_mode == "newfile":
                    pass
                elif write_mode == "overwrite":
                    os.remove(f"{file_name}.csv")
                    break
                elif write_mode == "append":
                    break
                else:
                    raise ValueError('Invalid "write_mode".')
            else:
                break
            if i == 9:
                warnings.warn("All available file names taken. Append to last one.")
                # file = open(file_name, 'a')
                break

        self.file_name = file_name

    def _set_reference_pos(self, t_elapsed, dt):
        """update reference position for using step and triangle shapes"""
        if self.parameters.reference_mode == "constant":
            return 0

        if self.parameters.reference_mode == "step":
            if not hasattr(self, "step_ctr"):
                self.step_ctr = 0

            if t_elapsed // self.parameters.move_time != self.step_ctr:
                if self.step_ctr % 2 == 0:
                    self.pos_init[
                        self.parameters.reference_axis
                    ] += self.parameters.move_amplitude
                else:
                    self.pos_init[
                        self.parameters.reference_axis
                    ] -= self.parameters.move_amplitude
                self.step_ctr += 1

            return 1

        elif self.parameters.reference_mode == "triangle":
            if not hasattr(self, "triangle_ctr"):
                self.triangle_ctr = 0

            if (
                t_elapsed + self.parameters.move_time / 2
            ) // self.parameters.move_time != self.triangle_ctr:
                self.triangle_ctr += 1

            if self.triangle_ctr % 2 == 0:
                self.pos_init[self.parameters.reference_axis] += (
                    2 * self.parameters.move_amplitude * dt / self.parameters.move_time
                )  # pk-pk = 2 * amplitude!
            else:
                self.pos_init[self.parameters.reference_axis] -= (
                    2 * self.parameters.move_amplitude * dt / self.parameters.move_time
                )

            return 2

        else:
            warnings.warn('Invalid reference mode. Do nothing (same as "constant").')

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
        calculated drifts to be converted to updated stage position by feedback loop

        """
        # TODO check if for 2 cams frames should be transformed; currently see settling in xy taking place over ca. 1000 sec and in different directions on the cameras

        # current_frames = self._normalize_array(current_frames)

        drifts = np.zeros(self.n_axes)
        # corr_stack = []
        # xy drift calculation
        for i in range(self.n_axes - 1):
            n_steps = len(self.calibration_stacks[i])
            corr_stack_ax = np.zeros(n_steps)

            for j in range(n_steps):
                corr_plane = [
                    correlate2d(
                        current_frames[k],
                        self.calibration_stacks[i][j, k],
                        mode="valid",
                    )
                    for k in range(self.n_cams)
                ]
                corr_stack_ax[j] = np.average(corr_plane)

            corr_stack_ax = self._normalize_array(corr_stack_ax, mode="range")

            if self.parameters.peak_fit == "centroid":
                # corr_stack_ax = self._normalize_array(corr_stack_ax)
                # corr_ax_max = corr_stack_ax.argmax()
                # corr_peak_rough = [max(0, corr_ax_max - 3), min(corr_ax_max + 4, len(corr_stack_ax))]
                # correlation_peak[i] = center_of_mass(corr_stack_ax[corr_peak_rough[0]:corr_peak_rough[1]])[0]
                drifts[i] = center_of_mass(corr_stack_ax)[0]
            elif self.parameters.peak_fit == "gauss":
                drifts[i] = self._fit_gauss_1D(corr_stack_ax)
            else:
                raise ValueError('Wrong "peak_fit" parameter.')

            # plt.figure(2)
            # plt.plot(corr_stack_ax, color=f'C{i}')
            # plt.vlines(drifts[i], 0, 1, color=f'C{i}')

            # corr_stack.append(corr_stack_ax)

        # z drift calculation
        frames_normalized = [
            self._normalize_array(f, mode="sum") for f in current_frames
        ]
        frames_sorted_current = [np.sort(f.flatten()) for f in frames_normalized]

        n_steps_z = self.calibration_stacks[2].shape[0]  # (n_step, n_cam, n_px)
        mse = np.zeros((n_steps_z, self.n_cams))
        for i in range(n_steps_z):
            for j in range(self.n_cams):
                d = self.calibration_stacks[2][i, j] - frames_sorted_current[j]
                mse[i, j] = np.average(d**2)
        mse_avg = np.average(mse, axis=1)
        mse_norm = self._normalize_array(
            -mse_avg, mode="range"
        )  # normalize to fit peak instead of dip
        # mse_norm = self._normalize_array(-mse)  # normalize to fit peak instead of dip
        self.mse = mse_norm

        if self.parameters.peak_fit == "centroid":
            drifts[2] = center_of_mass(mse_norm)[0]
        elif self.parameters.peak_fit == "gauss":
            drifts[2] = self._fit_gauss_1D(mse_norm)

        # =============================================================================
        #         n_steps_z = self.calibration_stacks[2].shape[1]    # (n_cam, n_step, n_px)
        #         d_cam0 = np.zeros(n_steps_z)
        #         d_cam1 = np.zeros(n_steps_z)
        #         for i in range(n_steps_z):
        #             d_cam0[i] = np.average(self.calibration_stacks[2][0, i] - laplace_sorted_current[0])
        #             d_cam1[i] = np.average(self.calibration_stacks[2][1, i] - laplace_sorted_current[1])
        #
        #         # d_cams = d_cam0 - d_cam1    # subtract deviations to reach maximum variation between focal planes of cams (here a movement lowering d_cam0 should increase d_cam1 and vice versa)
        #         # d_sq_norm = self._normalize_array(-d_cams**2)  # normalize to fit peak instead of dip
        #
        #         self.d_cam = d_cam0
        #
        #         if self.parameters.peak_fit == 'centroid':
        #             drifts[2] = center_of_mass(d_sq_norm)[0]
        #         elif self.parameters.peak_fit == 'gauss':
        #             drifts[2] = self._fit_gauss_1D(d_sq_norm)
        #
        # =============================================================================

        i = 0
        # color = f'C{self.step_ctr + 1}' if hasattr(self, 'step_ctr') else 'C0'
        color = (
            (0.5, (self.step_ctr % 10) / 10, 0, 0.5)
            if hasattr(self, "step_ctr")
            else "C0"
        )
        plt.figure(2)
        plt.plot(mse_norm, color=color)
        plt.vlines(drifts[i], 0, 1, color=color)

        # self.corr_stack = corr_stack
        return drifts

    def _normalize_array(self, array, mode="sum"):
        """normalize array to (0, 1)"""
        if mode == "sum":
            arr_norm = array / np.sum(array)
        elif mode == "range":
            d_arr = np.max(array) - np.min(array)
            if d_arr != 0:
                arr_norm = (array - np.min(array)) / d_arr
            else:
                warnings.warn("Array values all equal. Cannot normalize.")
                arr_norm = array
        else:
            raise ValueError(
                'Invalid mode in _normalize_array. Valid modes are "sum" and "range".'
            )
        return arr_norm

    def _fit_gauss_1D(self, data):
        """fit 1D array to Gaussian using scipy's curve_fit"""
        n = len(data)
        # f_gauss = lambda x, x0, s, a, b: a/np.sqrt(2*np.pi*s**2)*np.exp(-(x - x0)**2/(2*s**2)) + b
        # p0 = [data.argmax(), len(data)/2, 2*data.sum(), data.max()/20]
        f_gauss = (
            lambda x, x0, s, a: a / np.sqrt(s) * np.exp(-((x - x0) ** 2) / (2 * s**2))
        )
        p0 = [data.argmax(), n / 2, data.sum()]
        fit_lim = ([-1, n / 10, data.min()], [n + 1, 10 * n, n * data.max()])
        x = np.arange(n)
        try:
            fit_res = curve_fit(f_gauss, x, data, p0=p0, bounds=fit_lim)[0]
        except Exception as e:
            plt.figure()
            plt.plot(x, data)
            plt.plot(x, f_gauss(x, *p0))
            plt.show()
            raise RuntimeError(e)

        return fit_res[0]
