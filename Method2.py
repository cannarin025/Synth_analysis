import scipy as sp
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt

def Find_Periodic_Points(t_data, y_data, search_factor = 400, step_size = 1): #only step size 1 works until better "check rising edge" method is found
    t_points = [0]
    y_points = [0]
    t_step = (max(t_data) - min(t_data))/len(t_data) #timestep of datapoints
    check = True
    i = 100
    while check:
    #for i in range(1, len(t_data), step_size):
        if y_data[i] <= y_data[i - step_size] and y_data[i] >= y_data[i + step_size]: #avoid starting on rising edge
            if y_data[i] <= y_data[0]: #only consider values <= first value to avoid checking redundant values
                y0 = y_data[i]
                y_points[0] = y_data[i] #sets first value of array to suitable point
                t_points[0] = t_data[i] #sets first value of array to suitable point

                for j in range(i+1, len(t_data)-step_size-1, step_size):
                    if y_data[j] <= y_data[j - step_size] and y_data[j] >= y_data[j + step_size]:  # avoid checking rising edge
                        if t_data[j] > t_points[-1] + search_factor * t_step: #not sure if this will work properly
                            if y_data[j] > y0 and y_data[j + step_size] < y0:
                                y1 = y_data[j + step_size]
                                y2 = y_data[j]
                                t1 = t_data[j+step_size]
                                t2 = t_data[j]
                                line_gradient = (y_data[j + step_size] - y_data[j])/(t_data[j+step_size] - t_data[j]) #gradient of line joining points
                                intercept = y_data[j] - line_gradient*t_data[j] #intercept of line joining points
                                intersection = (y0 - intercept)/line_gradient #intersection of line joining points with desired y value gives next t value
                                t_points.append(intersection)
                                y_points.append(line_gradient*intersection + intercept)

                check = False
        if i < len(t_data) - 1:
            i += 1
        else:
            print("error: no periodicity found")

    return t_points, y_points #t_points is a list of all points where wave repeats. i.e. t_points[i] - t_points[i-1] = period

def Get_Average_Frequencies(filecount, graphing = False):
    avg_frequencies = []
    for file_no in range(2, filecount + 1):
        print(file_no)
        t_data, y_data = np.loadtxt(f"Data\\Waveform_Data\\WFM49.CSV", delimiter=",", skiprows=1, unpack=True) #runs 1 specific file
        t_data, y_data = np.loadtxt(f"Data\\Waveform_Data\\WFM{file_no}.CSV", delimiter=",", skiprows=1, unpack=True) #runs all files (comment out as you see fit)
        #inter_x = t_data
        inter_x = np.linspace(t_data[0], t_data[-1], 100000)
        inter_f = sp.interpolate.interp1d(t_data, y_data, kind="linear")
        inter_y = inter_f(inter_x)
        t_points, y_points = Find_Periodic_Points(inter_x, inter_y, step_size=1)
        #t_points, y_points = Find_Periodic_Points(inter_x, inter_y, step_size=5)

        if graphing:
            # graphing
            plt.plot(inter_x, inter_y, "o", markersize=2)
            plt.plot(t_points, y_points, "x")
            plt.plot(t_points, y_points)
            plt.grid()
            plt.show()

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
avg_frequencies = Get_Average_Frequencies(2, True) #runs 1 iteration
avg_frequencies = Get_Average_Frequencies(49, False) #runs 49 iterations (comment out as you see fit)
print(avg_frequencies)

