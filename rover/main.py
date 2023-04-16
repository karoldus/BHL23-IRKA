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
import time
import json

TRIG_PIN = 38
ECHO_PIN = 40
SERVO_PIN = 12
WALL_DETECTOR_PIN = 13
SERVER_HOST = "192.168.43.80"
SERVER_PORT = 8000

hcsr04_sensor = HCSR04(TRIG_PIN, ECHO_PIN)
reader = SimpleMFRC522()
motor = TB6612FNG()
servo = Servo(SERVO_PIN)
wall_detector = WallDetector(WALL_DETECTOR_PIN)

global_distance = 0
global_package_id = 0


def signal_handler(sig, frame):
    motor.motor_stop(0)
    GPIO.cleanup()
    sys.exit(0)


# thread responsible for measuring the distance using hc-sr04
def thread_measure_distance():
    global global_distance
    while True:
        distance = hcsr04_sensor.get_distance()
        print("Distance: ", distance)
        if distance < 15:
            sleep(1)
            distance = hcsr04_sensor.get_distance()
            print("Distance: ", distance)
            if distance > 15:
                continue

            t_rfid = threading.Thread(target=thread_read_rfid)
            t_rfid.start()
            t_rfid.join()
            global_distance = distance
            print(f"returning from measure_distance ({distance})")
            return
        sleep(1)


# thread responsible for controlling the motors
def thread_control_motors_forward():
    motor.start_time = time.time()
    motor.motor_ride(-1)
    wall_detector.loop()
    motor.motor_stop(-1)
    motor.end_time = time.time()

def thread_control_motors_back():
    motor.motor_ride(1)
    sleep(motor.end_time - motor.start_time - 4 * 0.36)
    motor.motor_stop(1)


def servo_cycle():
    sleep(1)
    servo.move(180)
    sleep(1)
    servo.move(90)
    sleep(1)


# thread responsible for reading RFID, started by measure_distance
def thread_read_rfid():
    global global_package_id, wall_detector
    print("Reading RFID")
    package_id, text = reader.read()
    # package_id = 1
    print(package_id)
    global_package_id = package_id


def send_package_id(package_id, height):
    r = requests.post(
        url=f"http://{SERVER_HOST}:{SERVER_PORT}/package/{package_id}/{height}",
    )

    wall_num = json.loads(r.text)["destination"]
    wall_detector.target_wall = wall_num
    print(f"Target wall: {wall_num}")


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        t_distance = threading.Thread(target=thread_measure_distance)
        t_distance.start()
        t_distance.join()
        send_package_id(global_package_id, 18.5 - global_distance)
        t_motor = threading.Thread(target=thread_control_motors_forward)
        t_motor.start()
        t_motor.join()

        servo_cycle()

        t_motor = threading.Thread(target=thread_control_motors_back)
        t_motor.start()
        t_motor.join()
    GPIO.cleanup()
