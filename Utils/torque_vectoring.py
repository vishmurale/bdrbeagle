# Test the values from the VN sensor

from vector_nav import VectorNav
import math

VN_PORT = 'COM3'
VN_BAUDRATE = 115200
SP_PORT = None
SP_BAUDRATE = None
PENALTY_RATE = 0.01


class TorqueVectoring:
    def __init__(self):
        self.vector_nav = VectorNav(VN_PORT, VN_BAUDRATE)
        self.steering_potentiometer = None

    def torque_vector(self):
        input_angle = self.avg_inputs()
        angle_abs = math.abs(input_angle)
        # Deadzone, to guard against the simple changes triggering torque vectoring.
        if(angle_abs < 5):
            return (1, 1)
        penalized_scalar = self.get_penalized_scalar(angle_abs)
        return (penalized_scalar, 1) if input_angle < 0 else (1, penalized_scalar)
    def get_penalized_scalar(self, angle:float):
        return 1 - (PENALTY_RATE * angle)

    def avg_inputs(self):
        vn_angle = self.vector_nav.get_angle()
        sp_angle = self.steering_potentiometer.get_angle()
        return (vn_angle + sp_angle) / 2


