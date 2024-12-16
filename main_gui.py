from interface.gui_handlers import Frame_Handlers
import logging
import configparser
from datetime import datetime
import os
import sys
import wx

import cProfile, pstats, io
from pstats import SortKey

log_directory = "log"

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_on = True
log_level = logging.INFO

conf_path = "config/default_config.ini"

if os.path.exists(conf_path):
    config = configparser.ConfigParser()
    config.read(conf_path)

    log_level = getattr(logging, config['logging']['log_level'].upper())
    log_on = True if config['logging']['log_on'] == 'True' else False

if log_on:
    current_date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    filename=os.path.join(log_directory, f"{current_date}.log")

    logging.basicConfig(level=log_level, format=log_format, filename=filename)
else:
    logging.disable(logging.CRITICAL + 1)


class MyApp(wx.App):
    """Main application class."""

    def __init__(self):
        super().__init__(clearSigInt=True)

        self.mainFrame = Frame_Handlers(None)
        self.mainFrame.Show()


if __name__ == "__main__":
    # Open a file to redirect stderr
    file = open('log/stderr.log', 'w')

    # Save the current stderr so we can restore it later
    original_stderr = sys.stderr

    # Redirect stderr to the file
    sys.stderr = file
    
    app = MyApp()
    app.MainLoop()
    wx.Exit()
    file.close()
