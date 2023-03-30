import RPi.GPIO as GPIO
import time

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DAC    = [26, 19, 13, 6, 5, 11, 9, 10]
COMP   = 4
TROYKA = 17

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MAX_VOLTAGE = 3.3

RANK = 8
MAX_VALUE = 2 ** RANK

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GPIO.setmode(GPIO.BCM)

GPIO.setup(DAC,    GPIO.OUT)
GPIO.setup(COMP,   GPIO.IN)
GPIO.setup(TROYKA, GPIO.OUT, initial = GPIO.HIGH)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def dec2bin (value, rank):
    assert(isinstance(value, int))
    assert(isinstance(rank,  int))

    return [int(element) for element in bin(value)[2:].zfill(rank)]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def adc ():
    for number in range(MAX_VALUE):
        GPIO.output(DAC, dec2bin(number, RANK))
        
        time.sleep(0.01)

        if GPIO.input(COMP) == 0:
            return number

    return MAX_VALUE

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

try:
    while True:
        value = adc()

        print(value, round(MAX_VOLTAGE / MAX_VALUE * value, 2))

except KeyboardInterrupt:
    print("\nHave a good day!")

finally:
    GPIO.output(DAC,    0)
    GPIO.output(TROYKA, 0)
    GPIO.cleanup()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
