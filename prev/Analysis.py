import scipy as sp
import numpy as np
import matplotlib.pyplot as plt

data_array = []
datasets = 49

#data_array.append([np.loadtxt(f"Data\\Waveform_Data\\WFM1.CSV", delimiter = ",", skiprows=1)])
t_data, y_data = np.loadtxt(f"Data\\Waveform_Data\\WFM3.CSV", delimiter = ",", skiprows=1, unpack=True)

def Find_Periodic_Points(t_data, y_data, tolerance_factor = 2, t_search_step = 5, step_size = 1):
    points = []
    errors = []
    #get average y difference and timestep
    diff_list = [np.abs(y_data[1] - y_data[0])]
    avg_diff = 0
    for i in range(2,len(y_data)-1):
        diff = np.abs(y_data[i] - y_data[i-1])
        if diff <= 20*diff_list[-1]: #selection to reject big leaps as saw goes from min ==> max
            diff_list.append(diff)

    avg_diff = sum(diff_list)/len(diff_list) #avg difference between y values of datapoints
    y_tolerance = tolerance_factor * avg_diff

    #t_step = (max(t_data) - min(t_data))/len(t_data) #timestep of datapoints


    for i in range(0, len(t_data), step_size):
        if y_data[i] <= y_data[0]:
            y0 = y_data[i]
            most_accurate = 100
            for j in range(i + t_search_step,len(t_data), step_size):
                y1 = y_data[j]
                y_diff = np.abs(y1 - y0)
                if y_diff <= y_tolerance:
                    if y_diff < most_accurate: #hones in on closest coordinate to intial point
                        most_accurate = y_diff
                        accurate_j = j
                    points.append([i,accurate_j]) #t coords of adjacent periodic points
                    errors.append(most_accurate)
    return points, errors

#points, errors = Find_Periodic_Points(t_data, y_data, 10,50)
#print(errors, "errors")

#graphing
dataFFT = np.fft.fft(y_data)
plt.figure()
plt.plot(dataFFT)
plt.figure()
print(t_data)
print(len(t_data))
print(y_data)
plt.plot(t_data, y_data)
#plt.plot(t_data[points[0][0]],y_data[points[0][0]], "x")
#plt.plot(t_data[points[0][1]],y_data[points[0][1]], "x")
plt.grid()
plt.show()