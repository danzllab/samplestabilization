import threading
import queue
import time
import numpy as np
import cv2
import logging
logger = logging.getLogger(__name__)

def camera_warmup(cam_queue, frame_rate=4, k_avg=200, var_max=1e-4, verbose=True):
    f_sum = []

    t_print = time.time()
    t_start = time.time()
    active = True
    while active:
        t0 = time.time()

        try:
            frame = cam_queue.get(timeout=3)
            f_sum.append(np.sum(frame))
        except queue.Empty:
            continue

        # f_sum.append([np.sum(c.get_frame()) for c in cameras])

        if len(f_sum) > k_avg:
            f_sum_last = np.array(f_sum[-k_avg:])
            f_var = max(
                abs(np.polyfit(np.arange(k_avg), f_sum_last / f_sum_last[-1], 1)[0])
            )
            # f_var = max(np.std(f_sum[-k_avg:], axis=0) / np.average(f_sum[-k_avg:], axis=0))
            if verbose and time.time() - t_print > 60:
                t_print = time.time()
            if (
                f_var < var_max
            ):  # target value has been reached, end camera warmup and start sample lock
                active = False
                if verbose:
                    t_elapsed = time.time() - t_start
            elif (
                f_var < 2 * var_max
            ):  # if f_var is approaching the target value, run camera at target frame rate
                # wait till enough time has passed to reach target frame rate
                while time.time() - t0 < 1 / frame_rate:
                    pass

    return f_sum

def create_colorbar(colormap, height=10, width=10, min_value=0, max_value=255, orig_min=0, orig_max=100, orig_val = 2**16-1, font_scale = 1):
    # Create a gradient image for the color bar
    colorbar = np.linspace(min_value, max_value, width, dtype=np.uint8)
    colorbar = np.repeat(colorbar[np.newaxis, :], height, axis=0)
    colorbar = cv2.applyColorMap(colorbar, colormap)

    font = cv2.FONT_HERSHEY_SIMPLEX

    x_coord = int(orig_min*width/orig_max) if orig_max != 0 else 0
    cv2.line(colorbar, (x_coord, 0), (x_coord, height), (255, 255, 255), 2)
    cv2.putText(colorbar, "{}".format(orig_min), (x_coord + 5, height), font, font_scale, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(colorbar, "{}".format(orig_max), (width - 100, height), font, font_scale, (0,0,0), 1, cv2.LINE_AA)

    return colorbar

    # Load your image
    image = cv2.imread('path_to_your_image.jpg', cv2.IMREAD_GRAYSCALE)

    # Apply a colormap to your image
    colored_image = cv2.applyColorMap(image, cv2.COLORMAP_JET)

    # Create a color bar
    height = colored_image.shape[0]
    width = 30  # Width of the color bar
    colorbar = create_colorbar(height, width, cv2.COLORMAP_JET)

    # Concatenate image and color bar
    combined_image = np.hstack((colored_image, colorbar))

class Frame_Processor(threading.Thread):
    def __init__(self, frame_queue, working_func, workflow_pass_que, warmup=False):
        threading.Thread.__init__(self)
        self.killswitch = threading.Event()
        self.pass2workflow = threading.Event()
        self.workflow_pass_que = workflow_pass_que
        self.frame_queue = frame_queue
        self.working_func = working_func
        self.warmup = warmup

    def stop(self):
        if self.is_alive():
            self.killswitch.set()
            self.join()

    def run(self):
        if self.warmup:
            camera_warmup(self.frame_queue)

        while not self.killswitch.is_set():
            try:
                frame = self.frame_queue.get(timeout=3)
            except queue.Empty:
                continue
            else:
                if self.pass2workflow.is_set():
                    self.workflow_pass_que.put(np.copy(frame))
                    self.pass2workflow.clear() 
                if frame is not None:
                    max_val = frame.max()
                    min_val = frame.min()          
                    prop = max_val / 255
                    frame = (frame / prop).astype("uint8") if prop != 0 else frame.astype("uint8")
                    frame = cv2.applyColorMap(frame, cv2.COLORMAP_OCEAN)

                    # --- Create a color bar ---
                    # frame_height = frame.shape[0]
                    height = 30
                    
                    width = frame.shape[1]  # Width of the color bar
                    colorbar = create_colorbar(cv2.COLORMAP_OCEAN, height, width, min_value=frame.min(), max_value=frame.max(), orig_min=min_val, orig_max=max_val)
                    real_frame = np.vstack((frame, colorbar))
                    # --- End of color bar creation ---

                    # real_frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
                    self.working_func(real_frame)

    def pass_frame(self):
        if self.is_alive():
            self.pass2workflow.set()

