class Parameters():
    def __init__(self, parameters=None) -> None:

        if parameters is None:
            self.create_empty()
        else:
            self.load(parameters)

    def create_empty(self):
        # self.roi_crop = None

        self.initial_range = (
            None # range covered by calibration stacks (at present same for all axes)
        )
        self.initial_step = (
            None # step size for calibration stacks (at present same for all axes)
        )

        # options for different profiles of the reference position (step, triangle) to test performance of feedback
        self.reference_mode = "constant"
        self.reference_axis = "1"

        # self.setpoint = None
        self.move_amplitude = None
        self.move_time = None

        # self.correlation_size = 300
        # self.correlation_steps = 10
        self.peak_fit = (
            "gauss"  # options to fit peak to Gauss or calculate position with centroid
        )

        self.sample_lock_active_axes = ["1", "2", "3"]  # ['1', '2', '3']
        self.scale_factors = [
            1,
            1,
            1,
        ]  # use same feedback parameters for all axes but multiply them with scale_factors to achieve suitable "strength" of feedback
        self.t_settle = None  # time (in seconds) to wait for stage to settle after each step, before acquiring new camera frame and calculating new stage position
        self.kp = None  # proportional feedback parameter
        self.ki = None  # (first-order) integrator feedback parameter
        self.ki2 = None  # (first-order) integrator feedback parameter

    def load(self, parameters):
        # self.roi_crop = None # <--- Do we actialy need this?

        # self.initial_range = parameters["initial_range"]
        # self.initial_step = parameters["initial_step"]

        # self.reference_mode = parameters["reference_mode"]
        # self.reference_axis = str(parameters["reference_axis"])[0]

        # # self.setpoint = None
        # self.move_amplitude = parameters["move_amplitude"]
        # self.move_time = parameters["move_time"]

        # self.peak_fit = parameters["peak_fit"]

        # self.sample_lock_active_axes = [str(each)[0] for each in parameters['sample_lock_active_axes']] if parameters['sample_lock_active_axes'] is not None else None  # ['1', '2', '3']
        # self.scale_factors = parameters["scale_factors"] 
        # self.t_settle = parameters["t_settle"]  
        # self.kp = parameters["kp"]
        # self.ki = parameters["ki"]
        # self.ki2 = parameters["ki2"]
        self.initial_range = parameters["reference_range_[um]"]
        self.initial_step = parameters["reference_step_size_[um]"]

        self.reference_mode = parameters["mode"]
        self.reference_axis = str(parameters["axis"])[0]

        # self.setpoint = None
        self.move_amplitude = parameters["move_amplitude_[um]"]
        self.move_time = parameters["move_time"]

        self.peak_fit = parameters["peak_fit"]

        self.sample_lock_active_axes = [str(each)[0] for each in parameters['sample_lock_active_axes']] if parameters['sample_lock_active_axes'] is not None else None  # ['1', '2', '3']
        self.scale_factors = parameters["scale_factors"] 
        self.t_settle = parameters["settling_time_[s]"]  
        self.kp = parameters["k_p"]
        self.ki = parameters["k_i"]
        self.ki2 = parameters["k_i2"]
        self.param = parameters