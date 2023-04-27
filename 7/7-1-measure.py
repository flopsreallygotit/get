import RPi.GPIO as GPIO
import numpy as np
import matplotlib.pyplot as plt
import time

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DAC    = [26, 19, 13, 6,  5, 11, 9,  10]
LEDS   = [21, 20, 16, 12, 7, 8,  25, 24]
COMP   = 4
TROYKA = 17

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MAX_VOLTAGE = 3.3

MAX_PERCENTAGE = 0.97
MIN_PERCENTAGE = 0.25

RANK = 8
MAX_VALUE = 2 ** RANK

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GPIO.setmode(GPIO.BCM)

GPIO.setup(LEDS,   GPIO.OUT)
GPIO.setup(DAC,    GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(TROYKA, GPIO.OUT, initial = GPIO.LOW)

GPIO.setup(COMP,   GPIO.IN)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def dec2bin (value, rank):
    assert(isinstance(value, int))
    assert(isinstance(rank,  int))

    return [int(element) for element in bin(value)[2:].zfill(rank)]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def adc (rank):
    number = 0

    for i in range(rank - 1, -1, -1):
        number += 2 ** i

        GPIO.output(DAC, dec2bin(number, rank))
        time.sleep(0.01)

        if GPIO.input(COMP) == 0:
            number -= 2 ** i

    return number

    # left  = -1
    # right = MAX_VALUE + 1

    # while True:
    #     mid = int((left + right) / 2)

    #     GPIO.output(DAC, dec2bin(mid, RANK))

    #     time.sleep(0.005)

    #     if GPIO.input(COMP) == 0:
    #         right = mid
    #     else:
    #         left  = mid

    #     if right - left <= 1:
    #         return mid

def vizualise (x, y, label, xlabel, ylabel):
    plt.plot(x, y, "-", label = label)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.grid(True)
    plt.legend()

    plt.show()

    return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

try:
    current_voltage = 0
    current_time = time.time()
    voltages = []

    # Сapacitor charging
    while current_voltage < MAX_VALUE * MAX_PERCENTAGE:
        current_voltage = adc(RANK)
        voltages.append(current_voltage)
        time.sleep(0.05)
        GPIO.output(LEDS, dec2bin(current_voltage, RANK))

    GPIO.setup(TROYKA, GPIO.OUT, initial = GPIO.HIGH)

    # Capacitor discharging
    while current_voltage > MAX_VALUE * MIN_PERCENTAGE:
        current_voltage = adc(RANK)
        voltages.append(current_voltage)
        time.sleep(0.05)
        GPIO.output(LEDS, dec2bin(current_voltage, RANK))

    current_time = time.time() - current_time

    # Data storing
    data = open("data.txt", "w")

    for voltage in voltages:
        data.write(str(voltage) + '\n')

    data.close()

    settings = open("settings.txt", "w")

    settings.write(str(1 / (current_time * len(voltages))) + '\n')
    settings.write(str(MAX_VOLTAGE / MAX_VALUE) + '\n')

    settings.close()

    # Data vizualising
    voltages = np.array(voltages) * MAX_VOLTAGE / MAX_VALUE
    time     = np.array(range(len(voltages))) * current_time / len(voltages)

    vizualise(time, voltages, "U(T)", "Время, с", "Напряжение, В")

    # Experiment parameters
    print("Experiment total time (sec):   ", current_time)
    print("Single measure time (sec):     ", current_time / len(voltages))
    print("Discretization frequency (Hz): ", 1 / 0.05)
    print("Quantization step (V):         ", MAX_VOLTAGE / MAX_VALUE)

except KeyboardInterrupt:
    print("\nHave a good day!")

finally:
    GPIO.output(DAC,    0)
    GPIO.output(LEDS,   0)
    GPIO.output(TROYKA, 0)

    GPIO.cleanup()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
