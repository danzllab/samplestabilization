import wx
from interface.camera_display import Camera_Display
from interface.camera_settings_page import Camera_Settings_Page


class Camera_Handler:
    """A class to handle the integration of camera display and settings pages in a UI notebook.

    This class manages the creation and setup of the camera display and settings pages, adding them to the
    corresponding notebook tabs in the main application window.

    Attributes:
        settings_page (Camera_Settings_Page): An instance of Camera_Settings_Page, representing the camera
            settings interface.
        display (Camera_Display): An instance of Camera_Display, which provides a UI for camera output display.

    Args:
        args: Variable length argument list, unused.
        parent (wx.Frame): The parent frame, which should contain the notebook panels where the pages will be added.
        camera_backend (str): Identifier for the camera backend to be used in display and settings.
        kw: Arbitrary keyword arguments, unused.
    """

    def __init__(self, *args, parent=None, camera_backend=None, **kw) -> None:
        self.settings_page = Camera_Settings_Page(
            parent=parent.settings_notebook, camera_backend=camera_backend
        )
        self.display = Camera_Display(
            parent=parent,
            related_settings_page=self.settings_page,
            camera_backend=camera_backend,
        )

        # Add the display and settings page to their respective notebook tabs
        parent.camera_notebook.AddPage(
            self.display,
            "{}".format(camera_backend),
            True,
            wx.NullBitmap,
        )

        parent.settings_notebook.AddPage(
            self.settings_page, "{}".format(camera_backend), True
        )
