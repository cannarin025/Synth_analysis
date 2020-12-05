import numpy as np

def get_n(f, fosc, oscl, pscl, s):
    n = fosc / (f*oscl*pscl*s)
    return n

def get_freq(n, fosc, oscl, pscl, s):
    f = fosc/(n*oscl*pscl*s)
    return f

musical_frequencies = [65.41, 69.30, 73.42, 77.78, 82.41, 87.31, 92.50, 98.00, 103.83, 110.00, 116.54, 123.47,
                       130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94,
                       261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88,
                       523.25, 554.37, 587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61, 880.00, 932.33, 987.77] #musical frequencies of notes played in range C2-B5

#params
fosc = 16e6
oscl = 4
pscl = 2
s = 256

n = [] #true N values
n_rd = [] #rounded N values
freq_rd = [] #frequency result of rounding
freq_err = [] #frequency error due to rounding
percent_freq_err = [] #fractional error

for freq in musical_frequencies:
    n.append(get_n(freq, fosc, oscl, pscl, s))
    n_rd.append(round(n[-1]))
    freq_rd.append(get_freq(n_rd[-1], fosc, oscl, pscl, s))
    freq_err.append(np.abs(freq_rd[-1] - freq))
    percent_freq_err.append(100 * freq_err[-1]/freq)

print("Done!")

