import RPi.GPIO as GPIO
import time
import sys

DAC  = [26, 19, 13, 6, 5, 11, 9, 10]
RANK = 8

MAX_VOLTAGE = 3.3
MAX_VALUE   = 2 ** RANK

GPIO.setmode(GPIO.BCM)
GPIO.setup(DAC, GPIO.OUT)

def dec2bin(value, rank):
    assert(isinstance(value, int))
    assert(isinstance(rank,  int))

    return [int(element) for element in bin(value)[2:].zfill(rank)]

try:
    period = input("Enter period of triangle sygnal: ")

    if period == 'Q':
        print("Have a good day!")
        sys.exit(0)

    try:
        period = float(period)
    except ValueError:
        print("Try to enter floating value.")
        sys.exit(1)

    period /= 2 * MAX_VALUE
        
    while True:
        for value in range(MAX_VALUE):
            GPIO.output(DAC, dec2bin(value, RANK))
            time.sleep(period)

        for value in range(MAX_VALUE - 1, -1, -1):
            GPIO.output(DAC, dec2bin(value, RANK))
            time.sleep(period)

finally:
    GPIO.output(DAC, 0)
    GPIO.cleanup()
