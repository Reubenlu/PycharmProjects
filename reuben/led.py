import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
LED1 = 6
GPIO.cleanup()
GPIO.setup(LED1, GPIO.OUT)
while True:
    GPIO.output(LED1, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(LED1, GPIO.LOW)
    time.sleep(0.5)
