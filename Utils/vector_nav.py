

from vnpy import *


class VectorNav(VnSensor):
    def __init__(self, port: str, baudrate:int):
        super().__init__()
        self.connect(port, baudrate)
        assert(self.is_connected)

    def get_angle(self) -> float:
        return self.read_yaw_pitch_roll().x