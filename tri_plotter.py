import scipy as sp
import numpy as np
import matplotlib.pyplot as plt

wavetype = "Triangle"
note = "C#1"

#unfiltered
t_data, y_data = np.loadtxt(f"Data\\Waveform_Data\\{wavetype}\\Unfiltered\\{note}.CSV", delimiter=",", skiprows=1, unpack=True) #runs all files (comment out as you see fit)

plt.figure()
plt.plot(t_data, y_data)

plt.xlabel("Time [s]")
plt.ylabel("Voltage [V]")
plt.title(f"Unfiltered {wavetype} Wave Playing Note {note}")
plt.grid()

#filtered
t_data, y_data = np.loadtxt(f"Data\\Waveform_Data\\{wavetype}\\Filtered\\{note}.CSV", delimiter=",", skiprows=1, unpack=True)

plt.figure()
plt.plot(t_data, y_data)

plt.xlabel("Time [s]")
plt.ylabel("Voltage [V]")
plt.title(f"Filtered {wavetype} Wave Playing Note {note}")
plt.grid()

plt.show()