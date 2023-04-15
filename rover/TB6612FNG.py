from enum import Enum
from raspberry_i2c_tb6612fng import MotorDriverTB6612FNG, TB6612FNGMotors

class Direction(Enum):
    FORWARD = 1
    BACKWARD = -1

class TB6612FNG:
    motor_speed_left = 100
    motor_speed_right = 91

    def __init__(self):
        self.driver = MotorDriverTB6612FNG()
        self.start_time = 0
        self.end_time = 0

    def motor_ride(self, direction):
        self.driver.dc_motor_run(TB6612FNGMotors.MOTOR_CHA, TB6612FNG.motor_speed_left * direction)
        self.driver.dc_motor_run(TB6612FNGMotors.MOTOR_CHB, TB6612FNG.motor_speed_right * direction)

    def motor_stop(self):
        self.driver.dc_motor_break(TB6612FNGMotors.MOTOR_CHA)
        self.driver.dc_motor_break(TB6612FNGMotors.MOTOR_CHB)
