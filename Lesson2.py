import RPi.GPIO as GPIO
import time

LEDS = [26, 19, 13, 6, 5, 11, 9, 10]

GPIO.setmode(GPIO.BCM)

GPIO.setup(LEDS, GPIO.OUT)

NUMBER = bin(int(input("INPUT: ")) % 256)[2:]
NUMBER = '0' * (8 - len(NUMBER)) + NUMBER

print("BINARY:", NUMBER)

try:
    for i in range(8):
        if NUMBER[i] == '1':
            GPIO.output(LEDS[i], 1)
    
    time.sleep(10)

finally:
    GPIO.output(LEDS, 0)
    GPIO.cleanup()