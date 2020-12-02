import scipy as sp
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt

def Find_Periodic_Points(t_data, y_data, tolerance = 0.95, step_size = 1, graphing = False):
    t_points = []
    y_points = []
    y_max = 0
    y_min = 0
    t_max = 0
    t_min = 0
    i_max = 0
    i_min = 0
    wait = False

    half_range = (max(y_data) - min(y_data))/2
    y_midpoint = max(y_data) - half_range
    upper_lim = y_midpoint + half_range * tolerance
    lower_lim = y_midpoint - half_range * tolerance

    for i in range(0, len(t_data), step_size):
        if y_data[i] >= upper_lim:
            wait = False #allows process to restart
            y_max = y_data[i]
            t_max = t_data[i]
            i_max = i

        if y_data[i] >= lower_lim:
            y_min = y_data[i]
            t_min = t_data[i]
            i_min = i

        if y_data[i] <= lower_lim and wait == False or t_data[i] == t_data[-1]:
            #getting range of "tooth"
            tooth_x = t_data[i_max:i_min]
            tooth_y = y_data[i_max:i_min]

            #calculating lobf
            lobf, cov = np.polyfit(tooth_x, tooth_y, 1, cov=True)
            #print(cov, "covariance")
            saw_fit = np.poly1d(lobf)

            if graphing:
                plt.plot(tooth_x, saw_fit(tooth_x), color="red", zorder = 10)

            #calculating intersection
            lobf_grad = lobf[0]
            lobf_intercept = lobf[1]
            intersection = (y_data[0] - lobf_intercept) / lobf_grad  # intersection of best fit line with desired y value gives next t value
            if intersection <= t_data[-1]:
                if intersection not in t_points: #checks that last value isnt duplicate (situation can arise due to y[i] == y[-1] condition drawing same lobf twice
                    t_points.append(intersection)
                    y_points.append(lobf_grad * intersection + lobf_intercept)

            #resetting for next tooth
            wait = True #ensures plotting etc is not done again on rising edge

    return t_points, y_points

def Get_Average_Frequencies(filecount, graphing = False):

    #background_noise = np.loadtxt should add background noise subtraction
    avg_frequencies = []
    for file_no in range(2, filecount + 1):
        print(file_no)
        #t_data, y_data = np.loadtxt(f"Data\\Waveform_Data\\Saw\\Unfiltered\\WFM10.CSV", delimiter=",", skiprows=1, unpack=True) #runs 1 specific file
        t_data, y_data = np.loadtxt(f"Data\\Waveform_Data\\Saw\\Unfiltered\\WFM{file_no}.CSV", delimiter=",", skiprows=1, unpack=True) #runs all files (comment out as you see fit)
        #inter_x = t_data
        inter_x = np.linspace(t_data[0], t_data[-1], 100000)
        inter_f = sp.interpolate.interp1d(t_data, y_data, kind="linear")
        inter_y = inter_f(inter_x)
        t_points, y_points = Find_Periodic_Points(inter_x, inter_y, step_size=1, graphing = graphing)
        #t_points, y_points = Find_Periodic_Points(inter_x, inter_y, step_size=5)

        if graphing:
            #graphing
            plt.plot(inter_x, inter_y, "o", markersize=1)
            plt.plot(t_points, y_points, "x", zorder = 20)
            plt.plot(t_points, y_points)
            plt.xlabel("Time /s")
            plt.ylabel("Voltage /V")
            plt.grid()
            plt.show()
            #pass

        # calculate avg frequency
        frequencies = []
        for i in range(1, len(t_points)):
            freq = 1 / (t_points[i] - t_points[i - 1])
            frequencies.append(freq)
        avg_freq = sum(frequencies) / len(frequencies)
        avg_frequencies.append(avg_freq)
        # print(avg_freq, "Hz")

    return avg_frequencies

#main code
musical_frequencies = [65.41, 69.30, 73.42, 77.78, 82.41, 87.31, 92.50, 98.00, 103.83, 110.00, 116.54, 123.47,
                       130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94,
                       261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88,
                       523.25, 554.37, 587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61, 880.00, 932.33, 987.77] #musical frequencies of notes played in range C2-B5

#avg_frequencies = Get_Average_Frequencies(2, True) #runs 1 iteration
avg_frequencies = Get_Average_Frequencies(49, False) #runs 49 iterations. does not display graphs. (comment out as you see fit)
frequency_errors = np.abs(np.array(musical_frequencies) - np.array(avg_frequencies))
print(avg_frequencies)

#graphing
fig1, (ax1, ax2) = plt.subplots(2,1)

#frequencies
ax1.plot(range(len(avg_frequencies)), avg_frequencies, label = "produced frequencies")
ax1.plot(range(len(avg_frequencies)), musical_frequencies, label = "true musical frequencies")
ax1.set_xlabel("Note number")
ax1.set_ylabel("Frequency [Hz]")
ax1.grid()
ax1.legend()

#errors
ax2.plot(range(len(avg_frequencies)), frequency_errors, label = "errors")
ax2.set_xlabel("Note number")
ax2.set_ylabel("Frequency [Hz]")
ax2.legend()
ax2.grid()

plt.subplots_adjust(hspace=0.5)

#octave errors
avg_produced_octave_factors = []
avg_true_octave_factors = []

for i in range(1, int(len(avg_frequencies)/12)): #octave number
    produced_factors = []
    true_factors = []

    for j in range(12): #note number
        trueC = musical_frequencies[j::12]
        producedC = avg_frequencies[j::12]
        true_factors.append(trueC[i]/trueC[i-1])
        produced_factors.append(producedC[i]/producedC[i-1])

    avg_true_octave_factors.append(sum(true_factors)/len(true_factors))
    avg_produced_octave_factors.append(sum(produced_factors)/len(produced_factors))


# true_octave_factors = []
# produced_octave_factors = []
# for i in range(1, len(trueC)):
#     true_octave_factors.append(trueC[i]/trueC[i-1])
#     produced_octave_factors.append(producedC[i]/producedC[i-1])

#graphing average octave factors
plt.figure()
plt.plot(np.array(range(len(avg_true_octave_factors))) + 2, avg_true_octave_factors, label = "true average octave factors")
plt.plot(np.array(range(len(avg_true_octave_factors))) + 2, avg_produced_octave_factors, label = "produced average octave factors")
plt.locator_params(axis = "x", nbins = 4)
plt.xlabel("Octave number")
plt.ylabel("Factor increase from last octave")
plt.grid()
plt.legend()
plt.show()


