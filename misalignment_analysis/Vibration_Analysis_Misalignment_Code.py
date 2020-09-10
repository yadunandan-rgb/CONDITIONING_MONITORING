# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 00:46:48 2020

@author: lenovo
"""

#Importing Libraries
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

#Reading the data
data = Mqtt
data.info()
data.shape
#converting the column to numeric
data["v"] = pd.to_numeric(data["v"], errors='coerce')
#Creating Datetime column
data["DateTime"] = pd.to_datetime(data["DateTime"], errors = 'ignore')
#Split the datetime column
data[['Date','Time']] = data.DateTime.str.split(n=1,expand=True) 

### Plotting Line Plot Time vs Acceleration 
# lines = data.plot.line(x='Time', y='v')
# plt.xticks(rotation=90)
# plt.ylabel("Acceleration (g)")

# ### Histogram of data["v"]
# data.plot.hist("v")
# plt.xlabel("Acceleration (g)")
#Assigning the new name for dataset
df =data
#Drop any non-value
df=df.dropna()
df.columns
#window size start
windowsize=0
#Window size end
windowsize1=1024
#Sample window 
samplewindow=1024

#Storing the results
Results = []


for row in range(0,len(df),1024):
    #selecting windows  
    df1=df.loc[windowsize:windowsize1]
    #Sampling Frequency
    Fs = 1600.0
    #Time
    T = 1 / Fs
    #Signal
    m = df1['v']
    #length of the signal
    N = len(m)
    #Detrend the signal (filtering)
    z = signal.detrend(m)
    #Calculate the FFT (Fast Fourier Transform)
    yf=fft(z)
    #X-axis 
    xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
    x =xf 
    #Y-axis
    y = abs(yf[0:N//2])
    # plt.plot(x,y)
    # plt.show()
    #Next window start
    windowsize = windowsize + 1024
    #Next window End
    windowsize1=windowsize1+1024
    #Refereance Rotational Speed
    RPM = 17
       
    ''' Misalignment Condition '''
    
    def Misalignment_Cond(fft_data,RPM):
        #FFT data
        fft_series = pd.Series(yf, name='value')
        #Absolute values of FFT
        fft_DF = pd.DataFrame(abs(fft_series))
        #Considering top 10 largest amplitude in a signal
        Top_10 = fft_DF.nlargest(10,'value')
        # Top_10 = fft_DF.sort_values("value", ascending = True, inplace = True)
        #Sort the index
        Max_amplitude = Top_10.sort_index(axis=0)
        #convert the lists into dataframe
        sort_freq = pd.DataFrame((Max_amplitude.index), columns=['freq'])
        #Taking only top 4 index 
        amp_list = list(Max_amplitude["value"][0:4])
        #Frequency ranges
        freqlimit = 0.2
        
        ####  Frequency Limit ####
        #start limit and End Limit at 1x RPM  
        start_1, end_1 = RPM-(freqlimit*RPM), RPM+(freqlimit*RPM)
        #RPM at 2x
        rpm_2 = RPM*2
        #start limit and End Limit at 1x RPM 
        start_2, end_2 = end_1, rpm_2+(freqlimit*RPM)
        #RPM at 3x
        rpm_3 = RPM*3
        #start limit and End Limit at 1x RPM 
        start_3, end_3 = end_2, rpm_3+(freqlimit*RPM)
        
        #### Frequency Values ####
        #High amplitude's and corresponding frequency within frequency range at 1x
        freq_1 = sort_freq.freq[0]
        #High amplitude's and corresponding frequency within frequency range at 2x
        freq_2 = sort_freq.freq[1]
        #High amplitude's and corresponding frequency within frequency range at 3x
        freq_3 = sort_freq.freq[2]
        
        #### Frequency Values in List ####
        frequency = [freq_1,freq_2,freq_3]
        
        # check for threshold
        #threshold at 1x
        threshold = 15
        #threshold at 2x
        FirstSecondThird_thrsld = 15*0.35
        #threshold at 3x
        fourth_thrsld = 15*0.25
        
        #Checking weather the spike is present within the frequency range (1x) and also crossing the threshold 
        if frequency[0] > int(start_1) and frequency[0] < int(end_1) and amp_list[0] > FirstSecondThird_thrsld:
            # print("Spike in first harmonic")
            #Checking weather the spike is present within the frequency range (2x) and also crossing the threshold
            if frequency[1] > int(start_2) and frequency[1] < int(end_2) and amp_list[1] > FirstSecondThird_thrsld:
                #Calculating the Phase difference
                #Input two datas
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
                    #Checking the Phase difference condition 
                    if phase_shift > 180:
                        print("Phase Difference: {}".format(phase_shift))
                        #Checking weather the spike is present within the frequency range (3x) and also crossing the threshold
                        if frequency[2] > int(start_3) and frequency[2] < int(end_3) and amp_list[2] > fourth_thrsld:
                            result = print("Severe Misalignment")
                        else:
                            # Checking the Parallel Misalignment or Angular Misalignment
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
