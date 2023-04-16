from enum import Enum
from raspberry_i2c_tb6612fng import MotorDriverTB6612FNG, TB6612FNGMotors
from time import sleep

class Direction(Enum):
    FORWARD = 1
    BACKWARD = -1

class TB6612FNG:
    motor_speed_right = 127
    motor_speed_left = 113

    def __init__(self):
        self.driver = MotorDriverTB6612FNG()
        self.start_time = 0
        self.end_time = 0

    def motor_ride(self, direction):
        self.driver.dc_motor_run(TB6612FNGMotors.MOTOR_CHA, 50 * direction)
        self.driver.dc_motor_run(TB6612FNGMotors.MOTOR_CHB, 49 * direction)
        sleep(0.12)
        self.driver.dc_motor_run(TB6612FNGMotors.MOTOR_CHA, 75 * direction)
        self.driver.dc_motor_run(TB6612FNGMotors.MOTOR_CHB, 72 * direction)
        sleep(0.12)
        self.driver.dc_motor_run(TB6612FNGMotors.MOTOR_CHA, 90 * direction)
        self.driver.dc_motor_run(TB6612FNGMotors.MOTOR_CHB, 87 * direction)
        sleep(0.12)
        self.driver.dc_motor_run(TB6612FNGMotors.MOTOR_CHA, TB6612FNG.motor_speed_right * direction)
        self.driver.dc_motor_run(TB6612FNGMotors.MOTOR_CHB, TB6612FNG.motor_speed_left * direction)

    def motor_stop(self, direction):
        self.driver.dc_motor_run(TB6612FNGMotors.MOTOR_CHA, 90 * direction)
        self.driver.dc_motor_run(TB6612FNGMotors.MOTOR_CHB, 86 * direction)
        sleep(0.12)
        self.driver.dc_motor_run(TB6612FNGMotors.MOTOR_CHA, 75 * direction)
        self.driver.dc_motor_run(TB6612FNGMotors.MOTOR_CHB, 71 * direction)
        sleep(0.12)
        self.driver.dc_motor_run(TB6612FNGMotors.MOTOR_CHA, 50 * direction)
        self.driver.dc_motor_run(TB6612FNGMotors.MOTOR_CHB, 48 * direction)
        sleep(0.12)
        self.driver.dc_motor_break(TB6612FNGMotors.MOTOR_CHA)
        self.driver.dc_motor_break(TB6612FNGMotors.MOTOR_CHB)
