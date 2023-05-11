import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

XSPACE = 1
YSPACE = 0.2

STEP = 20

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# DATA

data = []

with open("data.txt") as file:
    data = [float(value) for value in file.readlines()]

data = np.array(data)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# SETTINGS

sampleRate = 0
quantizationStep = 0

with open("settings.txt") as file:
    quantizationStep = float(file.readline())
    sampleRate = float(file.readline())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# DATA PREPARATION

data *= quantizationStep
time = np.array(range(len(data))) * sampleRate

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# FIGURE AND AXIS PREPARATION

figure, axis = plt.subplots(figsize = (16, 10), dpi = 600)

axis.set_title("Процесс заряда и разряда конденсатора в RC-цепочке", \
               loc = "center", fontsize = 20)

axis.set_xlabel("Время $\\tau$, с",  fontsize = 20)
axis.set_ylabel("Напряжение $U$, В", fontsize = 20)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# AXIS SETUP

axis.set_xlim(time.min(), time.max() + XSPACE)
axis.xaxis.set_minor_locator(tkr.MultipleLocator(0.5))
axis.xaxis.set_major_locator(tkr.MultipleLocator(2))

axis.set_ylim(data.min(), data.max() + YSPACE)
axis.yaxis.set_minor_locator(tkr.MultipleLocator(0.1))
axis.yaxis.set_major_locator(tkr.MultipleLocator(0.5))

axis.minorticks_on()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# GRID SETUP

axis.grid(which = "minor", color = "gray", linestyle = "--")
axis.grid(which = "major", color = "k",    linestyle = "-")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# TEXT OUTPUT

chargeTime = time[np.argmax(data)]

axis.text(7, 2,   "Время зарядки:  " + \
          str(round(chargeTime, 3)), fontsize = 20)

axis.text(7, 1.5, "Время разрядки: " + \
          str(round(time.max() - chargeTime, 3)), fontsize = 20)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# PLOT

axis.plot(time, data, c = "blue", linewidth = 1, label = "$U(\\tau)$")

axis.scatter(time[0:len(time):STEP], data[0:len(data):STEP], \
             marker = "o", c = "blue", s = 15)

axis.legend(shadow = False, loc = "best", fontsize = 20)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# SAVING

figure.savefig("plot.svg")
figure.savefig("plot.png")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
