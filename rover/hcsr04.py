import RPi.GPIO as GPIO
import time
import threading

class HCSR04:
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.hc_sr04_irq = False
        self.hc_sr04_start = 0
        self.hc_sr04_end = 0
        self.cv = threading.Condition()
        self.sensor_init()

    def sensor_init(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def irq_cb(self, channel):
        if self.hc_sr04_irq == False:
            self.hc_sr04_irq = True
            self.hc_sr04_start = time.time()
        else:
            with self.cv:
                self.hc_sr04_irq = False
                self.hc_sr04_end = time.time()
                GPIO.remove_event_detect(self.echo_pin)
                self.cv.notify()

    def get_distance(self):
        with self.cv:
            GPIO.add_event_detect(self.echo_pin, GPIO.BOTH, callback=self.irq_cb)
            GPIO.output(self.trig_pin, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(self.trig_pin, GPIO.LOW)
            self.cv.wait()

        return (self.hc_sr04_end - self.hc_sr04_start) * 34000 / 2
