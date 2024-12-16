from abc import ABC, abstractmethod


def inheritors(klass):
    return {child.__name__: child for child in klass.__subclasses__()}


## Abstract camera class
class Camera_ABC(ABC):
    """
    An abstract base class for camera interactions, designed to standardize the interface for various camera backends.
    This class uses a factory pattern to dynamically create instances of derived classes based on the specified backend.

    Methods are defined as abstract, which must be implemented by subclasses to handle specific camera operations such as
    opening the camera, starting acquisition, setting region of interest (ROI), and adjusting camera settings like exposure and gain.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__()

    def __new__(cls, backend):
        subclasses = inheritors(cls)
        if not backend in subclasses.keys():
            raise ValueError("Invalid backend '{}'".format(backend))
        subclass = subclasses[backend]
        instance = super(Camera_ABC, subclass).__new__(subclass)
        return instance

    @abstractmethod
    def open_camera(self):
        pass

    @abstractmethod
    def close_camera(self):
        pass

    @abstractmethod
    def is_connected(self):
        pass

    @abstractmethod
    def start_acquisition(self):
        pass

    @abstractmethod
    def stop_acquisition(self):
        pass

    @abstractmethod
    def set_roi(self, x, y, width, height):
        pass

    @abstractmethod
    def get_roi(self):
        pass

    @abstractmethod
    def set_exposure(self, exposure):
        pass

    @abstractmethod
    def set_auto_exposure(self, auto):
        pass

    @abstractmethod
    def get_exposure(self):
        pass

    @abstractmethod
    def get_exposure_range(self):
        pass

    @abstractmethod
    def set_gain(self, gain):
        pass

    @abstractmethod
    def set_auto_gain(self, auto):
        pass

    @abstractmethod
    def get_gain(self):
        pass

    @abstractmethod
    def get_gain_range(self):
        pass
