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

df =pd.read_csv(r'D:\VEGAM__codes_Dont_delete__fork_repo\Condition_monitoring\Nidhi_files2\vegamtagdata.csv')
df=df.dropna()
windowsize=1
windowsize1=512
samplewindow=512
howmanywindows=8

Fs = 1600.0
T = 1 / Fs
v = df['v']
N = len(v)
z = signal.detrend(v)
yf=fft(z)
yf=abs(yf[0:N // 2])
xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
# dd=xfcorrestoyf(xf,yf)
    # ee=multiples(dd)
# plt.plot(xf,yf)
# plt.show()

def xfcorrestoyf(listx1,listy2):
	listx1=list(listx1)
	listy2=list(listy2)
	listx3=list(map(int,listx1))
	listy4=list(map(int,listy2))
	largeinyf=heapq.nlargest(20,listy4)
	indexoflargeyf=[listy4.index(i) for i in largeinyf]
	indexofxfcorrestoyf=[listx3[j] for j in indexoflargeyf]
	# print('cooresponding to amplitude peak frequecnies',indexofxfcorrestoyf)
	# rpm=int(rpm/60)
	# limit1=int(0.8*rpm)
	# limit2=int(1*rpm)
	# rpmis=[int(j) for j in indexofxfcorrestoyf if j in range(limit1,(limit2+1))]
	print(indexofxfcorrestoyf)
	
	# return indexofxfcorrestoyf
def multiples(listis):
	start=1
	multiplevalues=[]
	for i in listis:
		for j in listis:
			if j in range((i*start)-2,(i*start)+3):
				
				start+=1
				multiplevalues.append(j)
				print(multiplevalues)
				return multiplevalues
def angleis(df1,df2):
	try:
		v1=df1['v']
		v2=df2['v']
		c = dot(v1,v2)/norm(v1)/norm(v2)
		angle = arccos(clip(c, -1, 1)) 
		print((angle*360)/(2*3.14))
		return (angle*360)/(2*3.14)
	except:
		return 'dimension error'
		
# for row in range(0,howmanywindows*windowsize1,samplewindow):
for row in range(0,len(df),samplewindow):
    df1=df.loc[windowsize:windowsize1]
    Fs = 1600.0
    T = 1 / Fs
    v = df1['v']
    N = len(v)
    z = signal.detrend(v)
    yf=fft(z)
    yf=abs(yf[0:N // 2])
    # yf=abs(z[0:N // 2])
    xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
    dd=xfcorrestoyf(xf,yf)
    
    # ee=multiples(dd)

    # f=np.fft.fftshift(np.fft.fft(yf))
    # filter=np.exp(- yf**2/6)  # simple Gaussian filter in the frequency domain
    # filtered_spectrum=f*filter  # apply the filter to the spectrum
    # filtered_data =  np.fft.ifft(filtered_spectrum) 
    # plt.plot(xf,filtered_spectrum)
    # plt.show()
    plt.plot(xf)
    plt.show()
    windowsize+=samplewindow
    windowsize1+=samplewindow
