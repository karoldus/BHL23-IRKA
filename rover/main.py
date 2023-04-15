#!/usr/bin/env python3

import threading
from hcsr04 import HCSR04
from time import sleep
import RPi.GPIO as GPIO
import sys
import signal
from mfrc522 import SimpleMFRC522
from TB6612FNG import TB6612FNG, Direction
from servo import Servo
from wall_detection import WallDetector
import requests

TRIG_PIN = 38
ECHO_PIN = 40
SERVO_PIN = 12
WALL_DETECTOR_PIN = 16
SERVER_HOST = "192.168.43.80"
SERVER_PORT = 8000

hcsr04_sensor = HCSR04(TRIG_PIN, ECHO_PIN)
# reader = SimpleMFRC522()
motor = TB6612FNG()
# servo = Servo(SERVO_PIN)
# wall_detector = WallDetector(16)
xor_it = 0

global_distance = 0
global_package_id = 0


def signal_handler(sig, frame):
    GPIO.cleanup()
    
    sys.exit(0)


# thread responsible for measuring the distance using hc-sr04
def thread_measure_distance():
    global global_distance
    while True:
        print("test")
        distance = hcsr04_sensor.get_distance()
        print("Distance: ", distance)
        if distance < 15:
            t_rfid = threading.Thread(target=thread_read_rfid)
            t_rfid.start()
            t_rfid.join()
            global_distance = distance
            print("returning from measure_distance")
            return
        sleep(1)


# thread responsible for controlling the motors
def thread_control_motors():
    print("thread control motors")
    global xor_it
    # while True:
    if xor_it:
        motor.motor_ride(1)
    else:
        motor.motor_ride(-1)

    xor_it ^= 1
    sleep(5)

    motor.motor_stop()


def servo_cycle():
    print(servo)
    servo.move(0)
    sleep(1)
    servo.move(90)
    sleep(1)
    servo.move(180)
    sleep(1)


# thread responsible for reading RFID, started by measure_distance
def thread_read_rfid():
    global global_package_id
    # package_id, text = reader.read()
    package_id = 1
    print(package_id)
    global_package_id = package_id


def send_package_id(package_id, height):
    r = requests.post(
        url=f"http://{SERVER_HOST}:{SERVER_PORT}/package",
        data={"package_id": package_id, "height": height},
    )

    wall_num = r.text
    print(wall_num)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    # t_distance = threading.Thread(target=thread_measure_distance)
    # t_distance.start()
    # t_distance.join()
    # send_package_id(global_package_id, global_distance)

    # t_wall_detector = threading.Thread(target=wall_detector.thread)
    # t_wall_detector.start()

    t_motor = threading.Thread(target=thread_control_motors)
    t_motor.start()
    t_motor.join()
    # t_wall_detector.join()

    servo_cycle()
    GPIO.cleanup()
