import RPi.GPIO as GPIO
import threading
from time import sleep


class WallDetector:
    def __init__(self, pin):
        self.cv = threading.Condition()
        self.pin = pin
        self.walls_detected = 0
        self.target_wall = 1

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN)

    def irq_cb(self, channel):
        self.walls_detected += 1
        GPIO.remove_event_detect(self.pin)
        with self.cv:
            self.cv.notify()

    def loop(self):
        while True:
            GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.irq_cb)
            with self.cv:
                self.cv.wait()
            print(f"Wall {self.walls_detected} detected")
            if self.walls_detected == self.target_wall:
                self.walls_detected = 0
                return
            sleep(1)
