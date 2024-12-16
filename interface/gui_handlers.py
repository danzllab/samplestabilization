import wx
import time
import logging
import numpy as np

from interface.interface import Main_Frame
from interface.camera_handler import Camera_Handler

# from stage_control.stage_thorlabs import *
from stage_control.stage_mockup import *
# from stage_control.stage_pi import *

from utils.plotting_utils import *
from utils.config_tool import *

from events.events import *
from workflow.workflow import *

logger = logging.getLogger(__name__)

DEFAULT_NUMBER_OF_NOTEBOOK_PAGES = 2

def list_hardwares(file_path):
    try:
        config = read_config(file_path)
    except Exception as e:
        logger.error(e)
        wx.MessageBox(
            "Error reading config file. Please make sure that the file exists and is not corrupted.",
            "Error",
            wx.OK | wx.ICON_ERROR,
        )
        return ["Camera_MOCKUP"], ["Stage_MOCKUP"]
    cameras = []

    for each in config["cameras"].items():
        logger.info(f"Camera: {each[1]}")
        if each[1] not in cameras or each[1] == "Camera_MOCKUP":
            cameras.append(each[1])

    stages_fine = []
    stages_coarse = []

    for each in config["stages_fine"].items():
        stages_fine.append(each[1])
    for each in config["stages_coarse"].items():
        stages_coarse.append(each[1])

    return cameras, stages_fine, stages_coarse


class Frame_Handlers(Main_Frame):
    def __init__(self, *args, **kw):
        Main_Frame.__init__(self, *args, **kw)

        # Helper arrays for stage movement
        self.stage_btns_id = {
            str(self.x_down_btn.GetId()): ["1", -1],
            str(self.x_up_btn.GetId()): ["1", 1],
            str(self.y_left_btn.GetId()): ["2", -1],
            str(self.y_right_btn.GetId()): ["2", 1],
            str(self.z_down_btn.GetId()): ["3", -1],
            str(self.z_up_btn.GetId()): ["3", 1],
        }
        self.stage_step_btns_id = {
            str(self.dxy_frac.GetId()): 1,
            str(self.dz_frac.GetId()): 0,
            str(self.dxy_sngl.GetId()): 1,
            str(self.dz_sngl.GetId()): 0,
            str(self.dxy_dec.GetId()): 1,
            str(self.dz_dec.GetId()): 0,
            str(self.dxy_huge.GetId()): 1,
            str(self.dz_huge.GetId()): 0,
        }
        #-----------------------------------

        # Helper arrays for coarse stage movement
        self.coarse_stage_btns_id = {
            str(self.ls_down_btn.GetId()): ["1", 1],
            str(self.ls_up_btn.GetId()): ["1", -1],
            str(self.rs_down_btn.GetId()): ["2", 1],
            str(self.rs_up_btn.GetId()): ["2", -1],
        }

        self.stage = None
        self.stage_coarse = None
        self.wf = None
        self.lock_params_dict = None

        self.data_len = 100
        self.sv_prms_ckb = True

        self.daya_pos = []
        self.daya_err = []
        self.data_dt = []

        self.cam_handlers = []
        self.camera_notebook.DeletePage(0)
        self.settings_notebook.DeletePage(
            DEFAULT_NUMBER_OF_NOTEBOOK_PAGES
        )  # Numeration starts from 0, so this command removes camera settings page
        self.lock_param_fpath = os.path.join(os.getcwd(), "sampleLock_parameters.txt")
        self.working_dir_path = os.path.join(os.getcwd(), 'data')
        self.writing_data_mode = "append"
        self.fl_save_frm_sl = False
        self.fl_save_sl_data = False

        cameras_backends_list, stages_fine, stages_coarse = list_hardwares("config/default_config.ini")

        # Init cameras and add them to the notebook
        dlg = wx.ProgressDialog(
            "Initializing",
            "Initializing cameras...",
            maximum=100,
            parent=self,
            style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE,
        )

        cam_list_len = int(100 / len(cameras_backends_list))
        progress = 0
        dlg.Update(progress)

        for backend in cameras_backends_list:
            logger.info(f"Initializing {backend}")
            handler = Camera_Handler(parent=self, camera_backend=backend)
            self.cam_handlers.append(handler)
            progress += cam_list_len
            dlg.Update(progress, "Initializing {}".format(backend))
            time.sleep(1)
        # ---------------------------------------------

        # Init stages

        for each in stages_fine:
            try:
                self.stage = Stage_ABC(backend=each)
                pos = self.stage.get_position()
                self.update_stage_statusbar()

            except Exception as e:
                logger.error(e)
                wx.MessageBox(
                    "Missing {} class. Please make sure that the stage is connected and that the correct driver is installed.".format(
                        each
                    ),
                    "Error",
                    wx.OK | wx.ICON_ERROR,
                )
                return False
            
        if stages_coarse != []:
            for each in stages_coarse:
                try:
                    self.stage_coarse = Stage_ABC(backend=each, channels=[1,2])

                except Exception as e:
                    logger.error(e)
                    wx.MessageBox(
                        "Missing {} class. Please make sure that the coarse (single axis) stage is connected and that the correct driver is installed.".format(
                            each
                        ),
                        "Error",
                        wx.OK | wx.ICON_ERROR,
                    )
                    return False

        self.graph_panels = {
            "{}".format(self.x_pos_panel.GetId()): 0,
            "{}".format(self.y_pos_panel.GetId()): 1,
            "{}".format(self.z_pos_panel.GetId()): 2,
        }
        self.curr_graph_page = 0
        self.init_graphs()

        self.Connect(-1, -1, EVT_ON_CAM_TEMP_UPDATE, self.on_cam_temp_update)
        self.Connect(-1, -1, EVT_ON_PLOT_UPDATE, self.on_plots_update)

        self.lock_param_grid.Bind(wx.EVT_SIZE, self.on_lockin_setting_resize)

    def on_stage_coar_sync(self, event):
        if self.stage_coarse is not None:
            if event.IsChecked():
                self.stage_coarse.sync = True
                self.rs_down_btn.Disable()
                self.rs_up_btn.Disable()
            else:
                self.stage_coarse.sync = False
                self.rs_down_btn.Enable()
                self.rs_up_btn.Enable()
        

    def on_cam_temp_update(self, evt):
        temp = evt.temp
        cam_num = evt.cam_count
        self.statusbar.SetStatusText(
            f"Camera {cam_num} temperature: {temp} C", i=cam_num
        )

    def on_pick_lock_stp_load_file(self, event):
        path = event.GetPath()
        config = read_config(path)
        self.lock_params_dict = dict(config["sample_lock"])
        params = self.lock_params_dict.values()
        for idx, key in enumerate(SAMPLE_LOCK_PARAMS_KEYS):
            if self.lock_params_dict[key] is not None:
                self.lock_param_grid.SetCellValue(idx + 1, 0, str(self.lock_params_dict[key]))
            else:
                self.lock_param_grid.SetCellValue(idx + 1, 0, "")

    def on_pick_lock_stp_save_file(self, event):
        path = event.GetPath()
        params = {}
        for i in range(self.lock_param_grid.GetNumberRows() - 1):
            params[
                self.lock_param_grid.GetRowLabelValue(i + 1).replace(" ", "_")
            ] = self.lock_param_grid.GetCellValue(i + 1, 0)

        params = read_lock_params_from_grid(self.lock_param_grid)
        if params is not None:
            update_config_by_section(path, "sample_lock", params)
        else:
            wx.MessageBox(
                "Please make sure that all parameters are set.",
                "Error",
                wx.OK | wx.ICON_ERROR,
            )

    def on_working_dir(self, event):
        path = event.GetPath()

        if os.path.exists(path):
            self.working_dir_path = path

    def on_save_frm_sl(self, event):
        if event.IsChecked():
            logger.info("Save Checked ")
            self.fl_save_frm_sl = True
            logger.info("Save frames marker set to: {}".format(self.fl_save_frm_sl))
        else:
            logger.info("Save Unchecked ")
            self.fl_save_frm_sl = False

    def on_save_sl_data(self, event):
        if event.IsChecked():
            print("Save Checked ")
            self.fl_save_sl_data = True
        else:
            print("Save Unchecked ")
            self.fl_save_sl_data = False

    def on_writing_modes_list(self, event):
        selected = event.GetString()
        logger.info("Writing mode selected: {}".format(selected))
        self.writing_data_mode = selected

    def on_save_params_ckb(self, event):
        if event.IsChecked():
            self.sv_prms_ckb = True
        else:
            self.sv_prms_ckb = False

    def on_start_sl_btn(self, event):
        params = read_lock_params_from_grid(self.lock_param_grid)
        if params is None:
            wx.MessageBox(
                "Please make sure that all parameters are set.",
                "Error",
                wx.OK | wx.ICON_ERROR,
            )
            return False
        
        print("Params: ", params)
        self.lock_params_dict = convert_dict_str2float(params)
        if self.lock_params_dict is None:
            dlg = wx.MessageDialog(
                None,
                "Would you like to proceed without sample lock parameters?",
                "Attention!",
                wx.YES_NO | wx.ICON_QUESTION,
            )
            result = dlg.ShowModal()
            if result == wx.ID_NO:
                return False
        
        data_params = dict(
            {
                "writing_mode": self.writing_data_mode,
                "save_dat": self.fl_save_sl_data,
                "save_frames": self.fl_save_frm_sl,
                "dir_path": self.working_dir_path,
            }
        )

        queue_list = []
        for each in self.cam_handlers:
            que = each.display.video_panel.workflow_pass_que
            request_fn = each.display.video_panel.proc.pass_frame
            if que is not None:
                queue_list.append([que, request_fn])
            else:
                wx.MessageBox(
                    "Please make sure that all cameras are started.",
                    "Error",
                    wx.OK | wx.ICON_ERROR,
                )
                return False

        self.daya_pos = []
        self.daya_err = []
        self.data_dt = []

        n_points = int(self.n_points.GetValue())
        self.data_len = int(self.data_n_points.GetValue())

        #----Clearing the graphs----
        for panel in [self.x_pos_panel, self.y_pos_panel, self.z_pos_panel]:
            panel.clear()
            panel.update_background()
        #---------------------------

        self.wf = Workflow(
            stage=self.stage,
            n_points=n_points,
            save_parms=self.sv_prms_ckb,
            parameters=self.lock_params_dict,
            data_params=data_params,
            frame_queue=queue_list,
            evt_catcher=self,
        )
        self.wf.start()

        self.last_frame_time = time.time()
        self.frame_counter = 0
        self.fps = 0

        self.stop_sl_btn.Enable()
        self.start_sl_btn.Disable()

    def on_stop_sl_btn(self, event):
        if self.wf is not None:
            self.wf.stop()
            self.wf = None
        self.start_sl_btn.Enable()
        self.stop_sl_btn.Disable()

    # -------------------------------------------------------------------

    def on_plots_update(self, evt):
        self.daya_pos += [*evt.pos]
        self.daya_err += [*evt.err]
        self.data_dt += [*evt.dt]

        if len(self.data_dt) > self.data_len:
            self.daya_pos = self.daya_pos[-self.data_len:]
            self.daya_err = self.daya_err[-self.data_len:]
            self.data_dt = self.data_dt[-self.data_len:]

        last = evt.pos[-1]

        self.update_stage_statusbar(pos={"1": last[0], "2": last[1], "3": last[2]})
        self.draw_data()

    def on_page_changing(self, event):
        if self.daya_pos != []:
            self.draw_data()

    def draw_data(self):
        page = self.positions_notebook.GetCurrentPage()

        idx = self.graph_panels[str(page.GetId())]

        pos_y = np.array(self.daya_pos)[:, idx]
        err_y = np.array(self.daya_err)[:, idx]

        page.draw(pos = np.stack((self.data_dt, pos_y), axis=1), err = np.stack((self.data_dt, err_y), axis=1))

        current_time = time.time()
        self.frame_counter += 1
        if current_time - self.last_frame_time >= 1.0:
            self.fps = self.frame_counter / (current_time - self.last_frame_time)
            self.last_frame_time = current_time
            self.frame_counter = 0
            self.statusbar.SetStatusText("Points/Sec: {:.2f}".format(self.fps),2)

    def init_graphs(self):
        
        pass

    def on_camera_notebook_page_close(self, event):
        self.camera_notebook.GetCurrentPage().on_close()

    def update_stage_statusbar(self, fine_stage=True, pos=None):
        if fine_stage:
            stage = self.stage
        else:
            stage = self.stage_coarse
        if pos is None:
            try:
                pos = stage.get_position()
            except Exception as e:
                logger.error(e)
        if pos is not None:
            if len(pos) > 2:
                self.statusbar.SetStatusText(
                    "Abs. fine stage pos.: [{}, {}, {}]".format(
                        round(pos["1"], 3), round(pos["2"], 3), round(pos["3"], 3)
                    ),
                    i=3,
                )
            else:
                self.statusbar.SetStatusText(
                    "Rel. coarse stage pos.: [{}, {}, {}]".format(
                        0.0, 0.0, round(pos[1]*1000, 3) #   Convert to um
                    ),
                    i=2,
                )

    def on_step_size_btn(self, event):
        btn = event.GetEventObject()
        id = str(btn.GetId())
        step = float(btn.GetLabel())

        if self.stage_step_btns_id[id] == 1:
            self.xy_step_size.SetIncrement(step)
            self.xy_step_size.SetValue(step)
        else:
            self.z_step_size.SetIncrement(step)
            self.z_step_size.SetValue(step)

    def on_step_size_btn_coar(self, event):
        btn = event.GetEventObject()
        id = str(btn.GetId())
        step = float(btn.GetLabel())

        self.z_step_size_coar.SetIncrement(step)
        self.z_step_size_coar.SetValue(step)

    def on_move_btn(self, event):
        id = event.GetEventObject().GetId()
        step_size = 0.1
        axis, direction = self.stage_btns_id[str(id)]

        if axis == "1" or axis == "2":
            step_size = self.xy_step_size.GetValue()
        if axis == "3":
            step_size = self.z_step_size.GetValue()

        self.stage.move_by(axis, direction * step_size)
        self.update_stage_statusbar()

    def on_move_btn_coar(self, event): ## Coarse Platform. Axis == Channel (Right or Left Motor)
        id = event.GetEventObject().GetId()
        step_size = 0.1
        axis, direction = self.coarse_stage_btns_id[str(id)]
        print("Axis: ", axis, "Direction: ", direction)

        step_size = self.z_step_size_coar.GetValue()
        print("Step Size: ", step_size)
        print("Axis: ", axis, "Direction * step_zie: ", direction * step_size)
        self.stage_coarse.move_by(axis, direction * step_size)
        self.update_stage_statusbar(fine_stage=False)

    def on_travel_btn(self, event):
        x = self.x_field.GetValue()
        z = self.z_field.GetValue()
        y = self.y_field.GetValue()

        if x != "":
            self.stage.move_to("1", float(x))
        if y != "":
            self.stage.move_to("2", float(y))
        if z != "":
            self.stage.move_to("3", float(z))

        self.update_stage_statusbar()

    def on_set_home_btn(self, event):
        
        pos = self.stage.get_position()
        if pos is not None:
            self.home = {"1": pos["1"], "2": pos["2"], "3": pos["3"]}
        else:
            self.home = self.home = {"1": 0.0, "2": 0.0, "3": 0.0}
        
        self.home_coord_txt.SetLabel("( {:.4f}, {:.4f}, {:.4f})".format(self.home["1"], self.home["2"], self.home["3"]))
        self.rtrn_home_btn.Enable()

    def on_rtrn_home_btn(self, event):
        self.stage.move_to("1", float(self.home["1"]))
        self.stage.move_to("2", float(self.home["2"]))
        self.stage.move_to("3", float(self.home["3"]))

        self.update_stage_statusbar()

    def on_set_home_btn_coar(self, event):
        self.stage_coarse.set_home()
        pos = None
        pos = self.stage_coarse.get_home()
        if pos is not None:
            for key in pos.keys():
                self.home_coord_txt_coar.SetLabel("( 0.0, 0.0, {:.2f})".format(pos[key] * 1e3)) #Convert to um
                break
        
        self.rtrn_home_btn_coar.Enable()

    def on_rtrn_home_btn_coar(self, event):
        self.stage_coarse.go_home()
        self.update_stage_statusbar(fine_stage=False)

    def on_go_home_btn_coar(self, event):
        dlg = wx.MessageDialog(
                None,
                "You are about to move the coarse stage to the home position. It could collide with the optics. Are you sure you want to proceed?",
                "Attention!",
                wx.YES_NO | wx.ICON_QUESTION,
            )
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            self.stage_coarse.homming()
            self.update_stage_statusbar(fine_stage=False, pos={1 : self.stage_coarse.get_travel_range()[1][1]})
        


    # -------------------------------------------------------------------
    
    def on_lockin_setting_resize(self, event):
        
        width = self.lockin_setting.GetClientSize().width
        label_width = self.lock_param_grid.GetRowLabelSize()
        col_num = self.lock_param_grid.GetNumberCols()

        for each in range(col_num):
            self.lock_param_grid.SetColSize(each, int(width)-label_width-10)
        
        event.Skip()



    def on_close(self, evt):
        dlg = wx.ProgressDialog(
            "Closing",
            "Closing all devices...",
            maximum=100,
            parent=self,
            style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE,
        )
        dlg.Update(20, "Closing cameras...")
        time.sleep(1)
        for page in self.cam_handlers:
            try:
                page.display.on_close()
            except RuntimeError:
                pass
        dlg.Update(50, "Closing stage...")
        time.sleep(1)
        if self.stage is not None:
            try:
                self.stage.close_stage()
            except Exception as e:
                logger.error(e)
                wx.MessageBox(
                    "Error closing stage. Please make sure that the stage is connected and that the correct driver is installed.",
                    "Error",
                    wx.OK | wx.ICON_ERROR,
                )
                return False
            
        if self.stage_coarse is not None:
            try:
                self.stage_coarse.close_stage()
            except Exception as e:
                logger.error(e)
                wx.MessageBox(
                    "Error closing coarse stage. Please make sure that the stage is connected and that the correct driver is installed.",
                    "Error",
                    wx.OK | wx.ICON_ERROR,
                )
                return False

        if self.wf is not None:
            self.wf.stop()
        dlg.Update(100)
        self.Destroy()


# ----------------------GUI Utils-------------------------------------
def read_lock_params_from_grid(grid):
    all_set = True
    params = {}
    for i in range(grid.GetNumberRows() - 1):
        val = grid.GetCellValue(
            i + 1, 0
        )
        if val == "":
            all_set = False
        params[grid.GetRowLabelValue(i + 1).replace(" ", "_")] = val

    return params if all_set else None
