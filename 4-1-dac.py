import RPi.GPIO as GPIO
import sys

DAC  = [26, 19, 13, 6, 5, 11, 9, 10]
RANK = 8

MAX_VOLTAGE = 3.3

GPIO.setmode(GPIO.BCM)
GPIO.setup(DAC, GPIO.OUT)

def dec2bin(value, rank):
    assert(isinstance(value, int))
    assert(isinstance(rank,  int))

    return [int(element) for element in bin(value)[2:].zfill(rank)]

try:
    while True:
        value = input("Enter value to convert / (Q) to exit: ")

        if value == "Q":
            print("Have a good day!")
            sys.exit(0)

        try:
            value = int(value)
        except ValueError:
            print("Try to enter decimal value.")
            continue

        if not 0 <= value < 2 ** RANK:
            print("Your value must be in range 0 -", 2 ** RANK)
            continue

        GPIO.output(DAC, dec2bin(value, RANK))

        print("{:.3f}".format(value / (2 ** RANK) * MAX_VOLTAGE))

finally:
    GPIO.output(DAC, 0)
    GPIO.cleanup()
