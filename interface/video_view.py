import wx
import cv2
import os
import csv

from PIL import Image
from datetime import datetime


from interface.image_view import ImageView
from workflow.frame_processor import Frame_Processor

from cameras.camera_mockup import *
from cameras.camera_andor import *
from cameras.camera_ids import *

import queue

import logging
logger = logging.getLogger(__name__)


class VideoView(ImageView):
    """
    Extends ImageView to display video streams with interactive features such as zoom and rectangle drawing.

    Attributes:
        camera_backend (str): Identifier for the backend used by the camera.
        related_settings_page (wx.Window): Reference to the settings page associated with the camera.
        camera (Camera): Camera object used for capturing frames.
        proc (Frame_Processor): Processes frames from the camera.
        workflow_pass_que (queue.Queue): Queue for passing frames to the workflow.
        meas_on (bool): Flag to indicate whether measurement is ongoing.
        run_meas (bool): Flag to control the measurement process.
        startPos (tuple): Starting position for measurement drawing.
        recentPos (tuple): Most recent position for ongoing drawing.
        start_line (bool): Flag to start drawing lines.
        draw_rect (bool): Whether to draw rectangles.
        rect_crop (bool): Whether cropping mode is enabled.
        rect_end (tuple): End position of the rectangle.
        zoom_pipeline (list): Stores zoom levels and areas.
        rect_start (tuple): Starting position of the rectangle.
        make_screen_shot (bool): Flag to trigger screenshot.
        rec_path (str): Path to save screenshots or recordings.
    """

    def __init__(self, *args, camera_backend=None, related_settings_page=None, **kw):
        ImageView.__init__(self, *args, **kw)

        self.camera_backend = camera_backend
        self.related_settings_page = related_settings_page


        self.camera = None
        self.proc = None
        self.workflow_pass_que = None

        self.meas_on = False
        self.run_meas = False

        self.startPos = None
        self.recentPos = None
        self.start_line = False

        self.draw_rect = False
        self.rect_crop = False
        self.rect_end = None
        self.zoom_pipeline = []
        self.rect_start = None

        self.make_screen_shot = False
        self.rec_path = os.path.dirname(os.path.realpath(__file__))

        # Bind mouse events
        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.Bind(wx.EVT_LEFT_UP, self.on_release)
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_double_click)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_zoomout)
        self.Bind(wx.EVT_MOTION, self.on_mouse_move)

    def on_double_click(self, event):
        pass

    def on_click(self, event):
        """
        Captures mouse click events, initiating processes like drawing or selecting.

        Args:
            event (wx.MouseEvent): The mouse event capturing the click.
        """

        self.CaptureMouse()
        self.rect_start = recalculate_coord(
            coord=event.GetPosition(),
            best_size=self.best_size,
            img_size=self.image_size,
        )

    def on_mouse_move(self, event):
        """
        Responds to mouse movement events, used for features like dragging to draw or select regions.

        Args:
            event (wx.MouseEvent): The event capturing the mouse movement.
        """

        x, y = recalculate_coord(
            coord=event.GetPosition(),
            best_size=self.best_size,
            img_size=self.image_size,
        )
        if event.Dragging() and event.LeftIsDown():
            self.draw_rect = True
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if x > self.image_size[0]:
                x = self.image_size[0]
            if y > self.image_size[1]:
                y = self.image_size[1]
            self.rect_end = [x, y]
            #

    def on_release(self, event):
        """
        Handles mouse button release events, concluding dragging or drawing actions.

        Args:
            event (wx.MouseEvent): The event capturing the mouse button release.
        """

        self.draw_rect = False
        if self.HasCapture():
            self.ReleaseMouse()
            # self.draw_rect = False
            if self.rect_end is not None and self.rect_start is not None:
                if self.rect_end[0] == self.rect_start[0] and self.rect_end[1] == self.rect_start[1]:
                    self.rect_end = self.rect_start[0] + 1, self.rect_start[1] + 1
                self.zoom_pipeline.append([self.rect_start, self.rect_end])

    def on_zoomout(self, event):
        """
        Responds to right-click events to zoom out or reset the view.

        Args:
            event (wx.MouseEvent): The event capturing the right click.
        """

        self.draw_rect = False
        self.rect_end = None
        self.zoom_pipeline = []
        self.rect_start = None

    def make_screenshot(self, path):
        """
        Initiates the process to take a screenshot of the current view.

        Args:
            path (str): The file path where the screenshot will be saved.
        """

        self.make_screen_shot = True
        self.rec_path = path

    def start(self):
        """
        Starts the video stream and necessary processing.
        """

        que = queue.Queue()
        # self.camera = Camera_ABC(self.camera_backend)

        self.workflow_pass_que = queue.Queue()

        dlg = wx.ProgressDialog(
            "Starting camera...",
            "Please wait...",
            maximum=100,
            parent=self,
            style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE,
        )

        dlg.Update(10)

        try:
            logger.info("Video panel backend: %s", self.camera_backend)
            self.camera = Camera_ABC(self.camera_backend)
        except Exception as e:
            logger.error("Error: %s", e)
            wx.MessageBox(
                "Missing {} class. Please make sure that the camera is connected and that the correct driver is installed.".format(
                    self.camera_backend
                ),
                "Error",
                wx.OK | wx.ICON_ERROR,
            )
            return False
        
        dlg.Update(50)

        self.camera.frame_queue = que

        self.proc = Frame_Processor(frame_queue=que, working_func=self.player, workflow_pass_que=self.workflow_pass_que)
        self.related_settings_page.camera = self.camera

        self.proc.start()
        self.camera.start()

        self.related_settings_page.update_ui_settings()

        dlg.Update(100)

    def stop(self):
        """
        Stops the video stream and any associated processing.
        """

        self.Parent.parent.on_stop_sl_btn(None)
        if self.camera is not None:
            self.camera.stop()
            self.camera = None
            self.related_settings_page.camera = self.camera
        if self.proc is not None:
            self.proc.stop()
            self.proc = None

    def player(self, real_frame):
        """
        Processes each frame to apply zoom, draw rectangles, or other transformations.

        Args:
            real_frame (np.array): The frame received from the camera to be processed.
        """

        frame = real_frame

        if frame is not None:
            if self.zoom_pipeline != []:
                # if self.rect_start is not None and self.rect_end is not None:
                for each in self.zoom_pipeline:
                    if each[0] is not None and each[1] is not None:
                        frame = frame[
                            min(each[0][1], each[1][1]) : max(each[0][1], each[1][1]),
                            min(each[0][0], each[1][0]) : max(each[0][0], each[1][0]),
                        ]

            if self.draw_rect:
                frame = self.draw_rectangle(frame)

            if frame is not None:
                if frame.size > 0:
                    wx.CallAfter(self.set_frame, frame)
                    wx.CallAfter(self.Parent.update_min_max, frame.min(), frame.max())

    def draw_rectangle(self, frame):
        """
        Draws a rectangle on a given frame as specified by start and end coordinates.

        Args:
            frame (np.array): The frame on which to draw the rectangle.
        """

        if self.rect_start is not None and self.rect_end is not None:
            return cv2.rectangle(
                frame,
                self.rect_start,
                self.rect_end,
                (255, 0, 0),
                thickness=2,
            )

    def save_screenshot(self, frame):
        """
        Saves the current frame as an image file.

        Args:
            frame (np.array): The frame to save as an image.
        """

        if os.path.exists(self.rec_path):
            dt = datetime.now().strftime("%d%m%Y_%Hh%Mm%Ss")
            im = Image.fromarray(frame)
            im.save(os.path.join(self.rec_path, "{}.png".format(dt)))
        self.make_screen_shot = False


def recalculate_coord(coord, best_size, img_size):
    """
    Converts coordinates from GUI space to image space based on scaling.

    Args:
        coord (tuple): Coordinates in GUI space.
        best_size (tuple): The scaled dimensions and offsets of the image in the GUI.
        img_size (tuple): The original dimensions of the image.

    Returns:
        tuple: Coordinates recalculated to correspond to the original image space.
    """

    (circ_x, circ_y) = coord
    (i_w, i_h, x_of, y_of) = best_size
    (real_x, real_y) = img_size
    if x_of == 0:
        circ_y = circ_y - y_of
    if y_of == 0:
        circ_x = circ_x - x_of
    return int(circ_x * real_x / i_w), int(circ_y * real_y / i_h)
