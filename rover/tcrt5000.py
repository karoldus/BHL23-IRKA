import RPi.GPIO as GPIO

class TCRT5000:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)

    def is_wall(self):
        return GPIO.input(self.pin) == GPIO.HIGH