

def xfcorrestoyf(listx1,listy2):
    listx1=list(listx1)
    listy2=list(listy2)
    listx3=list(map(int,listx1))
    listy4=list(map(int,listy2))
    largeinyf=heapq.nlargest(20,listy4)
    indexoflargeyf=[listy4.index(i) for i in largeinyf]
    indexofxfcorrestoyf=[listx3[j] for j in indexoflargeyf]
    print(indexofxfcorrestoyf)




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
start = time.time()

# D:\Vegam_all_csv_files_sensor_data\Nidhi files\BASF_good_and_bad\basfdata.csv
# D:\VEGAM__codes_Dont_delete__fork_repo\Condition_monitoring\Nidhi_files2\vegamtagdata.csv
# D:\Vegam_all_csv_files_sensor_data\Dynaspede_all_data\Unbalance\478_x_2.50_3.xls
# D:\Vegam_all_csv_files_sensor_data\New folder (2)\fan_our_room_x.csv
# D:\Vegam_all_csv_files_sensor_data\Nidhi files\BASF_good_and_bad\basfdata.csv
# D:\Vegam_all_csv_files_sensor_data\Dynaspede_all_data\Dynaspede_misalignment\9.25.10.11.Y_90B.xls
df =pd.read_excel(r'D:\Vegam_all_csv_files_sensor_data\Dynaspede_all_data\Unbalance\478_x_2.50_3.xls')
df=df.dropna()
windowsize=1
windowsize1=512
samplewindow=512
howmanywindows=8


df = pd.DataFrame()
queue = collections.deque()
count=0
for row in range(0,len(df),samplewindow):
    df1=df.loc[windowsize:windowsize1]

    Fs = 1600.0
    T = 1 / Fs
    v = df1['v']
    N = len(v)
    z = signal.detrend(v)
    yf=(fft(z))
    queue.append(yf)
    normal_8_lists = []
#     if len(queue) == 8:
#         queue = list(queue)
#         average = [sum(e)/len(e) for e in zip(*queue)]
        

#         yf=abs(np.array(average)[0:N // 2])
#         xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
#         rms = np.sqrt(np.mean(np.square(yf)))
#         # print('rms is',((rms)))
#         greaterAmplitudes = ([(i) for i in yf if i>rms])

#         print(list(yf))
#         plt.plot(xf,yf)
#         # plt.show()
#         print(df1)
#         # print('length of queue is ',len(queue))
#         queue.clear()
    yf=abs(yf[0:N // 2])
    xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)

    
    plt.plot(xf,yf)
    plt.show()
    
    windowsize+=samplewindow
    windowsize1+=samplewindow
    count+=1




