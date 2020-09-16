


import pylab as pyl
import numpy as np
import scipy as sy
import scipy.fftpack as syfp
from scipy import signal
from scipy.fftpack import fft, ifft
import matplotlib.pyplot as plt
import pandas as pd
import os
from scipy.signal import find_peaks_cwt
import csv
import heapq

def xfcorrestoyf(listx1,listy2):
    listx3=list(map(int,listx1))
    listy4=list(map(int,listy2))
    largeinyf=heapq.nlargest(15,listy4)
    indexoflargeyf=[listy4.index(i) for i in largeinyf]
    frequencyofxfcorrestoyf=[listx3[j] for j in indexoflargeyf]
    print(frequencyofxfcorrestoyf)
    print(indexoflargeyf)
    return frequencyofxfcorrestoyf

df =pd.read_excel(r'D:\Vegam_all_csv_files_sensor_data\Dynaspede_all_data\Unbalance\478_x_2.50_3.xls')

df=df.dropna()
count=0
arr=[]
arr1=[]
rpm=[]
rpm1=[]
windowsize=1
windowsize1=1024
samplewindow=1024
H=3

for row in range(0,len(df),samplewindow):
    df1=df.loc[windowsize:windowsize1]
    
    Fs = 200.0
    T = 1 / Fs
     
    v = df1['v']
   
    N = len(v)
     
    z = signal.detrend(v)
       
    yf=fft(z)
    yf=abs(yf[0:N // 2])
    yf1=list(yf)
    yf2=list(yf)
       
    xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
    xf1=list(xf)
    xf2=list(xf)
    
    xfcorrestoyf(xf,yf)
      
    plt.plot(xf, abs(yf[0:N // 2]))
    windowsize = windowsize + samplewindow
    windowsize1=windowsize1+samplewindow
    plt.show()
