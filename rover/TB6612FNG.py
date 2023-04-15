# import default libraries that are used in this example
import threading
from enum import Enum

# import the library
from raspberry_i2c_tb6612fng import MotorDriverTB6612FNG, TB6612FNGMotors

# # create an instance of the driver, connected to i2c
# driver = MotorDriverTB6612FNG()

# # drive both motors forward
# driver.dc_motor_run(TB6612FNGMotors.MOTOR_CHA, 100)
# driver.dc_motor_run(TB6612FNGMotors.MOTOR_CHB, 100)

# # pause for a second
# time.sleep(1)

# # stop the motors
# driver.dc_motor_break(TB6612FNGMotors.MOTOR_CHA)
# driver.dc_motor_break(TB6612FNGMotors.MOTOR_CHB)

class Direction(Enum):
    FORWARD = 1
    BACKWARD = -1

class TB6612FNG:
    motor_speed_left = 120
    motor_speed_right = 100

    def __init__(self):
        self.driver = MotorDriverTB6612FNG()

    def motor_ride(self, direction):
        self.driver.dc_motor_run(TB6612FNGMotors.MOTOR_CHA, TB6612FNG.motor_speed_left * direction)
        self.driver.dc_motor_run(TB6612FNGMotors.MOTOR_CHB, TB6612FNG.motor_speed_right * direction)

    def motor_stop(self):
        self.driver.dc_motor_break(TB6612FNGMotors.MOTOR_CHA)
        self.driver.dc_motor_break(TB6612FNGMotors.MOTOR_CHB)
