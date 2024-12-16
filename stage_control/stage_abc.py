from abc import ABC, abstractmethod


def inheritors(klass):
    return {child.__name__: child for child in klass.__subclasses__()}


## Abstract camera class
class Stage_ABC(ABC):
    """
    Abstract base class for stage control.

    By naming convention, the stage axis should be a dictionary with strings of numbers starting with "1".
    """

    def __init__(self, backend, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __new__(cls, backend, *args, **kwargs):
        subclasses = inheritors(cls)
        if not backend in subclasses.keys():
            raise ValueError("Invalid backend '{}'".format(backend))
        subclass = subclasses[backend]
        instance = super(Stage_ABC, subclass).__new__(subclass)
        # instance.__init__(*args, **kwargs)
        return instance

    @abstractmethod
    def open_stage(self):
        pass

    @abstractmethod
    def close_stage(self):
        pass

    @abstractmethod
    def is_connected(self):
        pass

    @abstractmethod
    def get_travel_range(self, x, y):
        pass

    @abstractmethod
    def get_position(self):
        pass

    @abstractmethod
    def move_by(self, axis, dpos):
        pass

    @abstractmethod
    def move_to(self, axis, pos):
        pass

    @abstractmethod
    def set_velocity(self, velocity):
        pass

    @abstractmethod
    def get_velocity(self):
        pass

    @abstractmethod
    def set_acceleration(self, acceleration):
        pass

    @abstractmethod
    def get_acceleration(self):
        pass

    @abstractmethod
    def set_home(self):
        pass

    @abstractmethod
    def get_home(self):
        pass
