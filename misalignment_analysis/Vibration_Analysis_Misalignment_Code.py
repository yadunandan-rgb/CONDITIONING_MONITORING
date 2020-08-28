# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 00:46:48 2020

@author: lenovo
"""


import numpy as np
import pandas as pd
import os
from scipy import signal
import matplotlib
matplotlib.style.use('ggplot')
import matplotlib.pyplot as plt
import scipy as sy
import scipy.fftpack as syfp
from scipy.fftpack import fft, ifft
#import pandas as pd
import csv
import math

data = pd.read_csv("F:/VEGAM/Homework/basfdata.csv")
data.info()
data.shape

data["v"] = pd.to_numeric(data["v"], errors='coerce')

data["DateTime"] = pd.to_datetime(data["DateTime"], errors = 'ignore')
data[['Date','Time']] = data.DateTime.str.split(n=1,expand=True) 

### Plotting Line Plot Time vs Acceleration 
# lines = data.plot.line(x='Time', y='v')
# plt.xticks(rotation=90)
# plt.ylabel("Acceleration (g)")

# ### Histogram of data["v"]
# data.plot.hist("v")
# plt.xlabel("Acceleration (g)")

df =data
df=df.dropna()
df.columns
df=df.dropna()
windowsize=0
windowsize1=1024
samplewindow=1024

Results = []
for row in range(0,len(df),1024):
    df1=df.loc[windowsize:windowsize1]
    Fs = 1600.0
    T = 1 / Fs
    m = df1['v']
    N = len(m)
    z = signal.detrend(m)
    
    yf=fft(z)
    
    xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
    x =xf 
    y = abs(yf[0:N//2])
    # plt.plot(x,y)
    # plt.show()
    windowsize = windowsize + 1024
    windowsize1=windowsize1+1024
    RPM = 17
       
    ''' Misalignment Condition '''
    
    def Misalignment_Cond(fft_data,RPM):
        fft_series = pd.Series(yf, name='value')
        fft_DF = pd.DataFrame(abs(fft_series))
        Top_10 = fft_DF.nlargest(10,'value')
        # Top_10 = fft_DF.sort_values("value", ascending = True, inplace = True)
        Max_amplitude = Top_10.sort_index(axis=0)
        sort_freq = pd.DataFrame((Max_amplitude.index), columns=['freq'])
        amp_list = list(Max_amplitude["value"][0:4])
        freqlimit = 0.2
        
        ####  Frequency Limit ####
        start_1, end_1 = RPM-(freqlimit*RPM), RPM+(freqlimit*RPM)
        rpm_2 = RPM*2
        start_2, end_2 = end_1, rpm_2+(freqlimit*RPM)
        rpm_3 = RPM*3
        start_3, end_3 = end_2, rpm_3+(freqlimit*RPM)
        
        #### Frequency Values ####
        freq_1 = sort_freq.freq[0]
        freq_2 = sort_freq.freq[1]
        freq_3 = sort_freq.freq[2]
        
        #### Frequency Values in List ####
        frequency = [freq_1,freq_2,freq_3]
        
        # check for threshold
        threshold = 15
        FirstSecondThird_thrsld = 15*0.35
        fourth_thrsld = 15*0.25
    
        if frequency[0] > int(start_1) and frequency[0] < int(end_1) and amp_list[0] > FirstSecondThird_thrsld:
            # print("Spike in first harmonic")
            if frequency[1] > int(start_2) and frequency[1] < int(end_2) and amp_list[1] > FirstSecondThird_thrsld:
                def phaseDifference(data_1, data_2):
                    # Cross-correlate the signals, a(t) & b(t)
                    ab_corr = np.correlate(data_1, data_2, "full")
                    dt = np.linspace(-t[-1], t[-1], (2 * num_samples) - 1)
                    # # Calculate time & phase shifts
                    # t_shift_alt = (1.0 / samples_per_second) * ab_corr.argmax() - t[-1]
                    t_shift = dt[ab_corr.argmax()]
                    # Limit phase_shift to [-pi, pi]
                    phase_shift = ((2.0 * np.pi) * ((t_shift / (1.0 / freq_Hz)) % 1.0)) - np.pi
                # print("Spike in second harmonic")
                    if phase_shift > 180:
                        print("Phase Difference: {}".format(phase_shift))
                        if frequency[2] > int(start_3) and frequency[2] < int(end_3) and amp_list[2] > fourth_thrsld:
                            result = print("Severe Misalignment")
                        else:
                            if amp_list[0] > amp_list[1]:
                                result = print("Parallel Misalignment")
                            else:
                                result = print("Angular Misalignment")
                    else:
                        presult = print("No Phase Difference")
                    return phase_shift
            else:
                result = print("No Problem, No Spike at 2RPM")
        else:
            result = print("No Problem, No Spike at 1RPM")
            Results.append(result)
        return 

Misalignment_Cond(yf,17)
print(Results)
