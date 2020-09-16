import pylab
import matplotlib.pyplot as plt
import numpy
import pylab as pyl
import numpy as np
import scipy as sx
import scipy.fftpack as syfp
from scipy import signal
from scipy.fftpack import fft, ifft, rfft
import matplotlib.pyplot as plt
import pandas as pd
import os
from scipy.signal import find_peaks_cwt
import csv
import heapq
import timeit
import collections
import time

df =pd.read_csv(r'D:\Vegam_all_csv_files_sensor_data\ATestData_Hemang_Sir\CSv_from_Mat\CSv_from_MatH-A-1.csv')
df=df.dropna()
windowsize=1
windowsize1=1024
samplewindow=1024
howmanywindows=8
for row in range(0,len(df),samplewindow):
    df1=df.loc[windowsize:windowsize1]

    Fs = 200000.0
    T = 1 / Fs
    # v = df1['Value']
    v = df1['Channel_1']

    # print(v)
    N = len(v)
    z = signal.detrend(v)
    yf=fft(z)

    
    plt.figure()
    y=abs(yf[0:N // 2])
    x = pylab.linspace(0.0, 1.0 / (2.0 * T), N // 2)
    plt.xlabel('Frequency(Hz)')
    plt.ylabel('Amplitude()')
    plt.plot(x,y)
    plt.savefig(r'D:\Vegam_all_csv_files_sensor_data\ATestData_Hemang_Sir\HA1_fft_plots\one {0}.jpg'.format(row))
    # plt.close()
    windowsize+=samplewindow
    windowsize1+=samplewindow

# for i in range(0,244):
#     plt.figure()
#     y = numpy.array(Data_EMG[i,:])
#     x = pylab.linspace(EMG_start, EMG_stop, Amount_samples)
#     plt.xlabel('Time(ms)')
#     plt.ylabel('EMG voltage(microV)')
#     plt.savefig('EMG {0}.jpg'.format(i))
#     plt.close()