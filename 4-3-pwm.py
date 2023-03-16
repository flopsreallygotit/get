import RPi.GPIO as GPIO
import sys

FREQUENCY   = 1000
MAX_VOLTAGE = 3.3
STEP        = 0.01

OUTPUT_PIN = 14
DAC  = [26, 19, 13, 6, 5, 11, 9, 10]

GPIO.setmode(GPIO.BCM)
GPIO.setup(DAC,        GPIO.OUT)
GPIO.setup(OUTPUT_PIN, GPIO.OUT)

pwm = GPIO.PWM(OUTPUT_PIN, FREQUENCY)
pwm.start(0)

try:
    while True:
        duty_cycle = input("Please enter duty cycle: ")

        if duty_cycle == 'Q':
            print("Have a good day!")
            sys.exit(0)

        try:
            duty_cycle = float(duty_cycle)
        except ValueError:
            print("Try to enter floating value.")
            continue

        pwm.ChangeDutyCycle(duty_cycle)
        
        print("{:.2f}".format(duty_cycle * MAX_VOLTAGE * STEP))

finally:
    GPIO.output(DAC,        0)
    GPIO.output(OUTPUT_PIN, 0)

    GPIO.cleanup()
