# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 14:55:22 2023

@author: danzloptics_admin
"""

import hardware
from workflow_control import Workflow
from parameters import Parameters

# from pipython import GCSDevice, pitools

import matplotlib.pyplot as plt
from scipy.optimize import minimize
import numpy as np
import time
import sys
import os


def calculate_transformation_matrix(xy_in, xy_out):
    """find matrix that minimizes xy_out = A xy_in
    coord with shape (n, 2)
    use homogeneous coordinates"""

    def f_opt(A_flat, xyhom_in, xyhom_out):
        A = A_flat.reshape(3, 3)
        res = np.zeros(xyhom_in.shape)
        for i in range(xyhom_in.shape[0]):
            res[i] = A @ xyhom_in[i] - xyhom_out[i]
        return np.sum(res**2)

    hom_ones = np.ones(xy_in.shape[0])[:, np.newaxis]
    xyhom_in = np.hstack([xy_in, hom_ones])
    xyhom_out = np.hstack([xy_out, hom_ones])
    A_0 = np.identity(3).flatten()
    min_res = minimize(f_opt, A_0, args=(xyhom_in, xyhom_out))
    A_out = min_res.x.reshape(3, 3)
    A_out[2] = 0, 0, 1  # required for consistency; should be small values in practice
    return A_out


def camera_warmup(cameras, frame_rate=4, k_avg=200, var_max=1e-4, verbose=True):
    f_sum = []

    t_print = time.time()
    t_start = time.time()
    active = True
    while active:
        t0 = time.time()

        f_sum.append([np.sum(c.get_frame()) for c in cameras])

        if len(f_sum) > k_avg:
            f_sum_last = np.array(f_sum[-k_avg:])
            f_var = max(
                abs(np.polyfit(np.arange(k_avg), f_sum_last / f_sum_last[-1], 1)[0])
            )
            # f_var = max(np.std(f_sum[-k_avg:], axis=0) / np.average(f_sum[-k_avg:], axis=0))
            if verbose and time.time() - t_print > 60:
                t_print = time.time()
                print(f"Current f_var: {f_var: .2e}")
            if (
                f_var < var_max
            ):  # target value has been reached, end camera warmup and start sample lock
                active = False
                if verbose:
                    t_elapsed = time.time() - t_start
                    print(
                        f"Camera warm-up finished after {t_elapsed: .1f} sec at frame rate {len(f_sum)/t_elapsed: .1f} Hz."
                    )
            elif (
                f_var < 5 * var_max
            ):  # if f_var is approaching the target value, run camera at target frame rate
                # wait till enough time has passed to reach target frame rate
                while time.time() - t0 < 1 / frame_rate:
                    pass

    return f_sum


# def _normalize_array(array):
#     arr_norm = (array - np.min(array))/(np.max(array) - np.min(array))
#     return arr_norm


if __name__ == "__main__":
    # TODOs
    # different algorithms: 3D cross-correlation
    # termination with KeyboardInterrupt not ideal; msvcrt not working with spyder IPython console but could run in different console or explore alternatives
    # (optional) could try to update to python 3.10 where match - case is implemented instead of ugly if - elif - else; would update to change camera library

    # xy_in = np.array([[333, 360],
    #                   [475, 491],
    #                   [524, 281],
    #                   [76, 341]])
    # xy_out = np.array([[367, 359],
    #                   [229, 468],
    #                   [194, 280],
    #                   [605, 355]])
    # xy_in = np.array(
    #     [[418, 416], [261, 267], [320, 174], [530, 479], [490, 237], [122, 329]]
    # )
    # xy_out = np.array(
    #     [[285, 405], [438, 280], [388, 193], [178, 455], [227, 242], [564, 342]]
    # )

    # A_trafo = calculate_transformation_matrix(xy_in, xy_out)
    # A_trafo = np.identity(3, dtype=float)

    try:
        plt.close(2)
        # plt.close(3)

        param = Parameters("cryo")
        # param.camera_1.M_affine = A_trafo
        # cams = [hardware.Camera_IDS(param.camera_0)]#, hardware.Camera(param.camera_1)]   # TODO for biplane test frame mirroring for camera_1
        cams = [hardware.Camera_Andor(param.camera_andor)]
        stage = hardware.Stage()
        wf = Workflow(stage, cams, param, file_write_mode="append")

        # wf.M_crosstalk = np.array()

        # while True:
        #     wf.display_frame(cam.get_frame())

        if not wf.position_stage(move_mode="step"):
            sys.exit(1)

        # warm up camera!
        f_sum = camera_warmup(cams, frame_rate=4, k_avg=500, var_max=1.2e-6)

        if not wf.initialize(save_frames=True):
            sys.exit(2)
        print("Initialized.")

        time.sleep(1)  # give stage time to settle
        if not wf.run_sample_lock(auto_terminate=False, save_frames=True):
            sys.exit(3)

    finally:
        if "cams" in locals():
            if hasattr(cams[0], "latest_frame"):
                last_frames = [c.latest_frame for c in cams]  # TODO return cropped ROI
            # close hardware
            for c in cams:
                c.close()
            del cams

        if "stage" in locals():
            stage.close()
            del stage

        if "wf" in locals():
            del wf.cameras

        if "param" in locals():
            param.save_all()

        # for img in imglist:
        #     plt.imshow(np.copy(img))
        #     plt.show(block=False)

        print("All done. Hardware closed.")
