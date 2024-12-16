import os
import time

from stage_control.stage_abc import *
import logging
logger = logging.getLogger(__name__)

from msl.equipment import (
    EquipmentRecord,
    ConnectionRecord,
    Backend,
    exceptions,
)
from msl.equipment.resources.thorlabs import MotionControl

# ensure that the Kinesis folder is available on PATH
os.environ['PATH'] += os.pathsep + 'C:/Program Files/Thorlabs/Kinesis'

record = EquipmentRecord(
    manufacturer='Thorlabs',
    model='BSC202',  # update for your device
    serial='70162954',  # update for your device
    connection=ConnectionRecord(
        address='SDK::Thorlabs.MotionControl.Benchtop.StepperMotor.dll',
        backend=Backend.MSL,
    )
)


class Stage_Thorlabs(Stage_ABC):
    def __init__(self, *args, **kw):
        # avoid the FT_DeviceNotFound error
        logging.info("Building device list")
        MotionControl.build_device_list()

        # connect to the Benchtop Stepper Motor
        self.motor = record.connect()
        self.home = None
        self.sync = True
        logger.info('Connected to {}'.format(self.motor))
        logger.info("Channels: {}".format(kw["channels"]) if "channels" in kw else "Channel: 1")
        self.channels = kw["channels"] if "channels" in kw else [1]
        # load the configuration settings, so that we can call  
        # the get_real_value_from_device_unit() method
        for channel in self.channels:
            self.motor.load_settings(channel)

            # the SBC_Open(serialNo) function in Kinesis is non-blocking and therefore we
            # should add a delay for Kinesis to establish communication with the serial port
            time.sleep(1)

            # start polling at 200 ms
            self.motor.start_polling(channel, 200)
        # self.motor.home(1)    
        # # self.wait_settled(channel=1, value=0.0)
        # self.motor.home(2)    
        # self.wait_settled(channel=2, value=0.0)
        
        self.stage_limits = self.get_travel_range()
        print("Limits: ", self.stage_limits)
        # print("Position: ", self.get_position())
        # self.move_by(1, 1000)
        print("Finished")
        

    def get_travel_range(self):
        ranges = {}
        for channel in self.channels:
            print("Channel type", type(channel))
            try:
                min, max = self.motor.get_motor_travel_limits(channel) # Returns values in mm
            except exceptions.ThorlabsError as e:
                print("Error")
                logger.error(e)
                min, max = 0, 0
            ranges[channel] = [min, max] # Convert to um
        return ranges

    def assert_stage_limits(self, axis, value):
        axis = int(axis)
        if value > self.stage_limits[axis][0] and value < self.stage_limits[axis][1]:
            return True
        else:
            return False

    def wait_settled(self, channel=1, value = 0.0):
        channel = int(channel)
        self.motor.clear_message_queue(channel)
        message_type, message_id, _ = self.motor.wait_for_message(channel)
        while message_type != 2 or message_id != value:
            position = self.motor.get_position(channel)
            real = self.motor.get_real_value_from_device_unit(channel, position, 'DISTANCE')
            print('  at position {} [device units] {:.3f} [real-world units]'.format(position, real))
            message_type, message_id, _ = self.motor.wait_for_message(channel)
        

    def get_position(self): # in mm (inverted real units: upper limit is 50 mm, lower limit is 0)
        pos = {}
        for channel in self.channels:
            # self.wait_settled(channel=channel, value=0.0)
            position = self.motor.get_position(channel)
            pos[channel] = 50 - self.motor.get_real_value_from_device_unit(channel, position, 'DISTANCE')
            print("CHannle: ", pos[ channel ])
        return  pos

    def move_to(self, axis, position):
        axis = int(axis)
        if self.assert_stage_limits(axis, position):
            channel = axis
            self.motor.move_to_position(channel, int(position))
            self.wait_settled(channel=channel, value=1.0)
            return True
        else:
            return False
        
    def move_by(self, axis, d_pos):
        channel = int(axis)
        pos = self.motor.get_device_unit_from_real_value(channel, d_pos*1e-3, 'DISTANCE')
        print("Axis: {}, int(d_pos): {}".format(axis, pos))
        if self.sync:
            for channel in self.channels:
                self.motor.move_relative(channel, pos)
        else:
            self.motor.move_relative(channel, pos)
        self.wait_settled(channel=channel, value=1.0)
        # axis = int(axis)
        # pos = self.get_position()
        # pos_new = pos[axis] + d_pos
        # print("Moving to ", pos_new, "from ", pos[axis])
        # channel = axis
        # if self.assert_stage_limits(axis, pos_new):
        #     self.motor.move_to_position(channel, int(pos_new * 100))
        #     self.wait_settled(channel=channel, value=1.0)
        #     return True
        # else:
        #     return False

    def close_stage(self):
        # stop polling and close the connection
        for channel in self.channels:
            self.motor.stop_polling(channel)
        self.motor.disconnect()

       
    def open_stage(self):
        pass

   
    def is_connected(self):
        pass
   
    def set_velocity(self, velocity):
        pass

   
    def get_velocity(self):
        pass

   
    def set_acceleration(self, acceleration):
        pass

   
    def get_acceleration(self):
        pass

   
    def set_home(self): # This is not for setting home, but for moving relative zero to current position
        print("Setting home!")
        self.home = self.get_position() # in mm
        print("Home: ", self.home)

   
    def get_home(self): # This is not for getting home, but for getting the relative zero position
        if self.home is not None:
            return self.home
        else:
            return None
        
    def go_home(self): # This is not for going home, but for moving to the relative zero position
        print("Homing!")
        chn = self.channels[0]
        if self.home is not None:
            pos = self.motor.get_device_unit_from_real_value(chn, 0, 'DISTANCE')
            for key, value in self.home.items():
                pos = self.motor.get_device_unit_from_real_value(chn, value, 'DISTANCE')
                break
            for channel in self.channels:
                self.motor.move_to_position(channel, pos)
            self.wait_settled(channel=self.channels[0], value=1.0)

    def homming(self): # This is actual homming function
        for each in self.channels:
            self.motor.home(each)    
        self.wait_settled(channel=self.channels[0], value=0.0)