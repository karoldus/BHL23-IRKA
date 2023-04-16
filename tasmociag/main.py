import RPi.GPIO as GPIO
import signal
import sys

def signal_handler(signal, frame):
    GPIO.cleanup()
    sys.exit(0)

BUTTON_PIN = 12
SERVO_PIN = 35

GPIO.setmode(GPIO.BOARD)
button_pressed = False

GPIO.setup(SERVO_PIN, GPIO.OUT, initial=False)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
pwm = GPIO.PWM(SERVO_PIN, 50)

def button_cb(channel):
    global button_pressed, pwm
    if button_pressed == False:
        pwm.start(0)
        pwm.ChangeDutyCycle(8.1)

        button_pressed = True
        return
    pwm.stop()
    button_pressed = False


GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_cb, bouncetime=50)
signal.signal(signal.SIGINT, signal_handler)

while True:
    pass
