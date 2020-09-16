# import os
# import demjson
# import ast
# import json
# with open('D:\Vegam_all_csv_files_sensor_data\A_text_files_fft_data\Burst2_data_90B.txt','r') as  raw_fftdata:
#   fft_data = raw_fftdata.readlines()
#   # print((fft_data))
# one_obj = (fft_data[1])
# print(one_obj)
# new = ast.literal_eval(one_obj)
# print(one_obj)
# for i in one_obj:
#   print(type(i))
# for i in fft_data:
#   print(json.loads(i).read())
# dataform = str(one_obj).replace("Message Recieved: ",' ')
# struct = json.loads(dataform)

def xfcorrestoyf(listx1,listy2):
    listx1=list(listx1)
    listy2=list(listy2)
    listx3=list(map(int,listx1))
    listy4=list(map(int,listy2))
    largeinyf=heapq.nlargest(20,listy4)
    indexoflargeyf=[listy4.index(i) for i in largeinyf]
    indexofxfcorrestoyf=[listx3[j] for j in indexoflargeyf]
    print(indexofxfcorrestoyf)


# new_obj = json.loads(fft_data[1])

# ['Message Recieved: TestingPayload\n', 'Message Recieved: {"n":200.0,"f":[0.0,0.0042777087688614787,

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

# D:\Vegam_all_csv_files\Dynaspede_all_data\Dynaspede_misalignment\12.42.12.46.Y_8A4.xls
# D:\VEGAM__codes_Dont_delete__fork_repo\Condition_monitoring\Nidhi_files2\vegamtagdata.csv
df =pd.read_excel(r'D:\Vegam_all_csv_files_sensor_data\Dynaspede_all_data\Dynaspede_misalignment\12.42.12.46.X_8A4.xls')
df=df.dropna()
windowsize=1
windowsize1=1024
samplewindow=1024
howmanywindows=8

# print(end - start)xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
# queue = deque()
queue = collections.deque()
count=0
for row in range(0,len(df),samplewindow):
    df1=df.loc[windowsize:windowsize1]

    Fs = 200.0
    T = 1 / Fs
    v = df1['v']
    N = len(v)
    z = signal.detrend(v)
    yf=fft(z)
    queue.append(yf)
    normal_8_lists = []
    # if len(queue) == 8:
    #     queue = list(queue)
    #     average = [sum(e)/len(e) for e in zip(*queue)]
        
        
    #     yf=abs(np.array(average)[0:N // 2])
    #     xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
    #     rms = np.sqrt(np.mean(np.square(yf)))
    #     # print(rms)
    #     print((yf))
    #     plt.plot(xf,yf)
    #     plt.show()
    #     # print('length of queue is ',len(queue))
    #     queue.clear()
    # rms = np.sqrt(np.mean(np.square(yf)))
    # above_rms_ampl_values = [i for i in list(yf) if i>rms]
    yf=abs((yf[0:N // 2]))
    xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
    # xfcorrestoyf(xf,yf)
    # # average = [sum(e)/len(e) for e in zip(*fft_cleaned_list_is)]
    plt.plot(xf,yf)
    plt.show()
    windowsize+=samplewindow
    # print(windowsize)
    windowsize1+=samplewindow
    # print(windowsize1)
    count+=1
# print(count)
end = time.time()







