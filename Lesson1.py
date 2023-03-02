import RPi.GPIO as GPIO

AUX  = [22, 23, 27, 18, 15, 14, 3,  2]
LEDS = [21, 20, 16, 12, 7,  8,  25, 24]

assert(len(AUX) == len(LEDS))

GPIO.setmode(GPIO.BCM)

GPIO.setup(AUX,  GPIO.IN)
GPIO.setup(LEDS, GPIO.OUT)

try:
    while True:
        for i in range(len(AUX)):
            GPIO.output(LEDS[i], GPIO.input(AUX[i]))

finally:
    GPIO.output(LEDS, 0)
    GPIO.cleanup()
