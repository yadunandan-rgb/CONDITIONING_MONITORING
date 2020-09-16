def unbalance5(fft_listX,fft_listY,fft_listZ,sampling_frequency,rpm,angle):
    N = sampling_frequency
    T = 1/N
    rpm = rpm//60               #to frequency
    limit_start1=int(0.8*rpm)            #CHANGE WITH RESPECT TO WINDOW BASED ON LOAD.
    limit_end1=int(1.2*(rpm))
    
    averaged_fftX = fft_listX
    averaged_fftY = fft_listY
    averaged_fftZ = fft_listZ

    start_angle=int(90-30)
    end_angle=int(90+30)

    yf_X=abs(np.array(averaged_fftX)[0:N // 2])
    xf_X = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
    
    yf_Y=abs(np.array(averaged_fftY)[0:N // 2])
    xf_Y = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
    yf_Z=abs(np.array(averaged_fftZ)[0:N // 2])
    xf_Z = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)

    rms_fft_amplitude_X = np.sqrt(np.mean(np.square(yf_X)))
    above_rms_ampl_X = [list(yf_X).index(i) for i in yf_X if i>rms_fft_amplitude_X]
    above_rms_ampl_X_values = [i for i in yf_X if i>rms_fft_amplitude_X]
    frequencycorrestoaboveamp_X = [list(xf_X)[j] for j in above_rms_ampl_X]
    # print('frequencycorrestoaboveamp_X',len(yf_X),len(frequencycorrestoaboveamp_X))

    rms_fft_amplitude_Y = np.sqrt(np.mean(np.square(yf_Y)))
    above_rms_ampl_Y = [list(yf_Y).index(i) for i in yf_Y if i>rms_fft_amplitude_Y]
    above_rms_ampl_Y_values = [i for i in yf_Y if i>rms_fft_amplitude_Y]
    frequencycorrestoaboveamp_Y = [list(xf_Y)[j] for j in above_rms_ampl_Y]
    # print('frequencycorrestoaboveamp_X',len(yf_Y),len(frequencycorrestoaboveamp_Y))


    rms_fft_amplitude_Z = np.sqrt(np.mean(np.square(yf_Z)))
    above_rms_ampl_Z = [list(yf_Z).index(i) for i in yf_Z if i>rms_fft_amplitude_Z]
    above_rms_ampl_Z_values = [i for i in yf_Z if i>rms_fft_amplitude_Z]
    frequencycorrestoaboveamp_Z = [list(xf_Z)[j] for j in above_rms_ampl_Z]
    # print('frequencycorrestoaboveamp_X',len(yf_Z),len(frequencycorrestoaboveamp_Z))


    onexrangevaluesFreq_X = [i for i in frequencycorrestoaboveamp_X if limit_start1<= i <=limit_end1]
    onexrangevaluesFreq_Y = [i for i in frequencycorrestoaboveamp_Y if limit_start1<= i <=limit_end1]
    onexrangevaluesFreq_Z = [i for i in frequencycorrestoaboveamp_Z if limit_start1<= i <=limit_end1]



    oneXrangeAmplitude_X_index = [frequencycorrestoaboveamp_X.index(i) for i in onexrangevaluesFreq_X]
    oneXrangeAmplitude_X1 = [above_rms_ampl_X_values[i] for i in oneXrangeAmplitude_X_index]
    oneXrangeAmplitude_Y_index = [frequencycorrestoaboveamp_Y.index(i) for i in onexrangevaluesFreq_Y]
    oneXrangeAmplitude_Y1 = [above_rms_ampl_Y_values[i] for i in oneXrangeAmplitude_Y_index]
    oneXrangeAmplitude_Z_index = [frequencycorrestoaboveamp_Z.index(i) for i in onexrangevaluesFreq_Z]
    oneXrangeAmplitude_Z1 = [above_rms_ampl_Z_values[i] for i in oneXrangeAmplitude_Z_index]

    compareXand_Z = list(set([i for i in oneXrangeAmplitude_X1 for j in oneXrangeAmplitude_Z1 if i>j]))
    compareYand_Z = list(set([i for i in oneXrangeAmplitude_Y1 for j in oneXrangeAmplitude_Z1 if i>j]))
    # print('compareXand_Z',compareXand_Z)
    # print('compareand_Z',compareYand_Z)
    
    if onexrangevaluesFreq_X == [] and onexrangevaluesFreq_Y == [] and onexrangevaluesFreq_Z==[]:
        print('1check for other faultssss')
        # print('multi1xvalues_X',onexrangevaluesFreq_X)
        # print('multi1xvalues_Y',onexrangevaluesFreq_Y)
        # print('compareXand_Z',onexrangevaluesFreq_Z)
    else:
        onexrpmvalue_X = float(np.mean(onexrangevaluesFreq_X))
        onexrpmvalue_Y = float(np.mean(onexrangevaluesFreq_Y))
        onexrpmvalue_Z = float(np.mean(onexrangevaluesFreq_Z))



        multi1xvalues_X = [i for i in frequencycorrestoaboveamp_X if ((onexrpmvalue_X*2)-2)<= i <= ((onexrpmvalue_X*2)+2) or ((onexrpmvalue_X*3)-2)<= i <= ((onexrpmvalue_X*3)+2)]
        multi1xvalues_Y = [i for i in frequencycorrestoaboveamp_Y if ((onexrpmvalue_Y*2)-2)<= i <= ((onexrpmvalue_Y*2)+2) or ((onexrpmvalue_Y*3)-2)<= i <= ((onexrpmvalue_Y*3)+2)]
        multi1xvalues_Z = [i for i in frequencycorrestoaboveamp_Z if ((onexrpmvalue_Z*2)-2)<= i <= ((onexrpmvalue_Z*2)+2) or ((onexrpmvalue_Z*3)-2)<= i <= ((onexrpmvalue_Z*3)+2)]
            
        multi1xvalueFrequeAmplitudes_for_ratioX =[frequencycorrestoaboveamp_X.index(i) for i in frequencycorrestoaboveamp_X if ((onexrpmvalue_X*2)-2)<= i <= ((onexrpmvalue_X*2)+2) or ((onexrpmvalue_X*3)-2)<= i <= ((onexrpmvalue_X*3)+2)]
        amplLessthanfiftypercent1xampl_X = [above_rms_ampl_X_values[i] for i in multi1xvalueFrequeAmplitudes_for_ratioX if i< (np.mean(oneXrangeAmplitude_X1)*0.3)]
        multi1xvalueFrequeAmplitudes_for_ratioY =[frequencycorrestoaboveamp_Y.index(i) for i in frequencycorrestoaboveamp_Y if ((onexrpmvalue_Y*2)-2)<= i <= ((onexrpmvalue_Y*2)+2) or ((onexrpmvalue_Y*3)-2)<= i <= ((onexrpmvalue_Y*3)+2)]
        amplLessthanfiftypercent1xampl_Y = [above_rms_ampl_Y_values[i] for i in multi1xvalueFrequeAmplitudes_for_ratioY if i< (np.mean(oneXrangeAmplitude_Y1)*0.3)]
        multi1xvalueFrequeAmplitudes_for_ratioZ =[frequencycorrestoaboveamp_Z.index(i) for i in frequencycorrestoaboveamp_Z if ((onexrpmvalue_Z*2)-2)<= i <= ((onexrpmvalue_Z*2)+2) or ((onexrpmvalue_Z*3)-2)<= i <= ((onexrpmvalue_Z*3)+2)]
        amplLessthanfiftypercent1xampl_Z = [above_rms_ampl_Z_values[i] for i in multi1xvalueFrequeAmplitudes_for_ratioZ if i< (np.mean(oneXrangeAmplitude_Z1)*0.3)]

        # if amplLessthanfiftypercent1xampl_X!=[] or amplLessthanfiftypercent1xampl_Y!=[] or amplLessthanfiftypercent1xampl_Z!=[]:
        #     print('1Unbalance will be there')

        # if multi1xvalues_X == [] and multi1xvalues_Y==[]:
        if amplLessthanfiftypercent1xampl_X!=[] or amplLessthanfiftypercent1xampl_Y!=[] or amplLessthanfiftypercent1xampl_Z!=[]:
            if compareXand_Z!=[] and compareYand_Z!=[]:
                if  start_angle<= angle <=end_angle:
                    print('2Unbalance')
                else:
                    print('2Check for Misalignment or other faults ')
            else:
                print('3Check for misalignment')
        else:   
            print('4Check for Other faults')
        # print('amplLessthanfiftypercent1xampl_X',amplLessthanfiftypercent1xampl_X)
        # print('amplLessthanfiftypercent1xampl_Y',amplLessthanfiftypercent1xampl_Y)
        # print('amplLessthanfiftypercent1xampl_Z',amplLessthanfiftypercent1xampl_Z)
        # print('multi1xvalues_X',oneXrangeAmplitude_X1)
        # print('multi1xvalues_Y',oneXrangeAmplitude_Y1)
        # print('compareXand_Z',onexrangevaluesFreq_Z)
        # print('compareYand_Z',compareYand_Z)


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

df1 =pd.read_excel(r'D:\Vegam_all_csv_files_sensor_data\Dynaspede_all_data\Unbalance\8A4\8A4_3.10_3.16_x.xls')
df2 =pd.read_excel(r'D:\Vegam_all_csv_files_sensor_data\Dynaspede_all_data\Unbalance\8A4\8A4_3.10_3.16_y.xls')
df3 =pd.read_excel(r'D:\Vegam_all_csv_files_sensor_data\Dynaspede_all_data\Unbalance\8A4\8A4_3.10_3.16_z.xls')

windowsize=0
windowsize1=1024
samplewindow=1024

queue1 = collections.deque()
queue2 = collections.deque()
queue3 = collections.deque()
for row in range(0,len(df1),samplewindow):
    df4=df1.loc[windowsize:windowsize1]
    df5=df2.loc[windowsize:windowsize1]
    df6=df3.loc[windowsize:windowsize1]

    Fs = 200.0
    T = 1 / Fs
    v1 = df4['v']
    v2 = df5['v']
    v3 = df6['v']

    # v1 = df4['Value']
    # v2 = df5['Value']
    # v3 = df6['Value']

    N1 = len(v1)
    N2 = len(v2)
    N3 = len(v3)

    z1 = signal.detrend(v1)
    z2 = signal.detrend(v2)
    z3 = signal.detrend(v3)

    yf1=fft(z1)
    yf2=fft(z2)
    yf3=fft(z3)

    queue1.append(yf1)
    queue2.append(yf2)
    queue3.append(yf3)
    # if len(queue1) == 8 and len(queue2)==8 and len(queue3)==8:
    #     queue1list = list(queue1)
    #     queue2list = list(queue2)
    #     queue3list = list(queue3)

    #     average1 = [sum(e)/len(e) for e in zip(*queue1list)]
    #     average2 = [sum(e)/len(e) for e in zip(*queue2list)]
    #     average3 = [sum(e)/len(e) for e in zip(*queue3list)]

    #     unbalance5(average1,average2,average3,200,1200,90)
        
    #     yf=abs(yf1[0:N2 // 2])
    #     xf = np.linspace(0.0, 1.0 / (2.0 * T), N2 // 2)
    #     queue1.clear()
    #     queue2.clear()
    #     queue3.clear()
    unbalance5(yf1,yf2,yf3,200,1200,90)
    windowsize+=samplewindow
    windowsize1+=samplewindow
    





