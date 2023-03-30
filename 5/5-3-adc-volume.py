import RPi.GPIO as GPIO
import time
import math

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DAC    = [26, 19, 13, 6,  5, 11, 9,  10]
LEDS   = [21, 20, 16, 12, 7, 8,  25, 24]
COMP   = 4
TROYKA = 17

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MAX_VOLTAGE = 3.3

RANK = 8
MAX_VALUE = 2 ** RANK

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GPIO.setmode(GPIO.BCM)

GPIO.setup(DAC,    GPIO.OUT)
GPIO.setup(LEDS,   GPIO.OUT)
GPIO.setup(COMP,   GPIO.IN)
GPIO.setup(TROYKA, GPIO.OUT, initial = GPIO.HIGH)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def dec2bin (value, rank):
    assert(isinstance(value, int))
    assert(isinstance(rank,  int))

    return [int(element) for element in bin(value)[2:].zfill(rank)]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def adc ():
    left  = -1
    right = MAX_VALUE + 1

    while True:
        mid = int((left + right) / 2)

        GPIO.output(DAC, dec2bin(mid, RANK))

        time.sleep(0.05)

        if GPIO.input(COMP) == 0:
            right = mid
        else:
            left  = mid

        if right - left <= 1:
            return mid

def get_volume (number):
    percent = math.ceil(number * RANK / MAX_VALUE)
    print("PERCENTAGE:", percent / 8 * 100, '%')

    array = [0] * RANK
    for i in range(percent):
        array[i] = 1

    GPIO.output(LEDS, array)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

try:
    while True:
        value = adc()
        get_volume(value)

except KeyboardInterrupt:
    print("\nHave a good day!")

finally:
    GPIO.output(DAC,    0)
    GPIO.output(LEDS,   0)
    GPIO.output(TROYKA, 0)

    GPIO.cleanup()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
