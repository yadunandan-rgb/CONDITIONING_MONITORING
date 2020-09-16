# Note: In previous code I was taking rpm and finding peak with range 0.8*rpm and 1.2*rpm
# So if some values will be very less than RpM like 12 then values will become wrong 12*.8 =9.6 and
# my code was checking multiple harmonics corresponding to 9.6 so which becomes wrong.

# So in this code I have added rpm code and I'll modify only to take that RPM and check multiple 
# harmonics correspondingcorresponding to that.



# def unbalance5(fft_listX,fft_listY,fft_listZ,sampling_frequency,rpm,angle):

def rpm(xf,yf,max_rpm):
    maximum_rpm_hz = max_rpm/60
    amplitudesindex = [list(yf).index(i) for i in yf]
    amplitudesvalues = [i for i in yf]
    xf1 = list(xf)
    frequency = [xf1[i] for i in amplitudesindex ]#if i<=maximum_rpm
    indexfreqencylesthanrpm = [frequency.index(i) for i in frequency if i<=maximum_rpm_hz]
    indexfreqencylesthanrpmvalues = [frequency[i] for i in indexfreqencylesthanrpm ] #if i<=maximum_rpm
    amplitudesrpm25 = [amplitudesvalues[i] for i in indexfreqencylesthanrpm]
    maxoneamplitude = max(amplitudesrpm25)
    indexof25amplitude = amplitudesvalues.index(maxoneamplitude)
    freuencycorrestomaxampl = indexfreqencylesthanrpmvalues[indexof25amplitude]
    finalRPM = freuencycorrestomaxampl
    return finalRPM*60


def unbalance5(fft_listX,sampling_frequency,rpm,angle,max_rpm):
    N = sampling_frequency
    T = 1/N
    rpm = rpm//60               #to frequency
    limit_start1=int(0.9*rpm)            #CHANGE WITH RESPECT TO WINDOW BASED ON LOAD.
    limit_end1=int(1.1*(rpm))

    oneXend_limit = (max_rpm/60)*0.7
    
    averaged_fftX = fft_listX
    

    start_angle=int(90-30)
    end_angle=int(90+30)

    yf_X=abs(np.array(averaged_fftX)[0:N // 2])
    xf_X = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
    
    

    rms_fft_amplitude_X = np.sqrt(np.mean(np.square(yf_X)))
    above_rms_ampl_X = [list(yf_X).index(i) for i in yf_X if i>rms_fft_amplitude_X]
    above_rms_ampl_X_values = [i for i in yf_X if i>rms_fft_amplitude_X]
    frequencycorrestoaboveamp_X = [list(xf_X)[j] for j in above_rms_ampl_X]
    

    onexrangevaluesFreq_X = [i for i in frequencycorrestoaboveamp_X if limit_start1<= i <=limit_end1]
    

    oneXrangeAmplitude_X_index = [frequencycorrestoaboveamp_X.index(i) for i in onexrangevaluesFreq_X]
    oneXrangeAmplitude_X1 = [above_rms_ampl_X_values[i] for i in oneXrangeAmplitude_X_index]
    
    if onexrangevaluesFreq_X == []: #and onexrangevaluesFreq_Y == [] and onexrangevaluesFreq_Z==[]:
        print('1check for other faultssss')
        
    else:
        onexrpmvalue_X = float(np.mean(onexrangevaluesFreq_X))
       

        multi1xvalues_X = [i for i in frequencycorrestoaboveamp_X if ((onexrpmvalue_X*2)-2)<= i <= ((onexrpmvalue_X*2)+2) or ((onexrpmvalue_X*3)-2)<= i <= ((onexrpmvalue_X*3)+2)]
            
        multi1xvalueFrequeAmplitudes_for_ratioX =[frequencycorrestoaboveamp_X.index(i) for i in frequencycorrestoaboveamp_X if ((onexrpmvalue_X*2)-2)<= i <= ((onexrpmvalue_X*2)+2) or ((onexrpmvalue_X*3)-2)<= i <= ((onexrpmvalue_X*3)+2)]
        amplLessthanfiftypercent1xampl_X = [above_rms_ampl_X_values[i] for i in multi1xvalueFrequeAmplitudes_for_ratioX if i< (np.mean(oneXrangeAmplitude_X1)*0.7)]
        
        if amplLessthanfiftypercent1xampl_X!=[]:#or amplLessthanfiftypercent1xampl_Y!=[] or amplLessthanfiftypercent1xampl_Z!=[]:
            if  start_angle<= angle <=end_angle:
                print('2Unbalance')
                print('amplLessthanfiftypercent1xampl_X',amplLessthanfiftypercent1xampl_X)
                print('oneXrangeAmplitude_X1',oneXrangeAmplitude_X1)
            else:
                print('2Check for Misalignment or other faults ')

        else:
            print('3Check for misalignment')
        print('amplLessthanfiftypercent1xampl_X',amplLessthanfiftypercent1xampl_X)
        print('oneXrangeAmplitude_X1',oneXrangeAmplitude_X1)
        print('onexrpmvalue_X',onexrpmvalue_X)

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

df1 = pd.read_excel(r'D:\Vegam_all_csv_files_sensor_data\Dynaspede_all_data\Unbalance\8A4\8A4_3.10_3.16_x.xls')
df2 = pd.read_excel(r'D:\Vegam_all_csv_files_sensor_data\Dynaspede_all_data\Unbalance\8A4\8A4_3.10_3.16_z.xls')
# df3 =pd.read_excel(r'D:\Vegam_all_csv_files_sensor_data\Dynaspede_all_data\Unbalance\8A4\8A4_3.10_3.16_x.xls')

windowsize = 0
windowsize1 = 1024
samplewindow = 1024

max_rpm = 1450
max_rpm_hz = max_rpm/60
queue1 = collections.deque()
angle = 90
for row in range(0,len(df1),samplewindow):
    df4 = df1.loc[windowsize:windowsize1]
    df5 = df2.loc[windowsize:windowsize1]
    
    Fs = 200.0
    T = 1 / Fs
    v1 = df4['v']
    v2 = df5['v']
    # v1 = df4['Value']
    # v2 = df5['Value']

   

    N1 = len(v1)
    N2 = len(v2)
    
    z1 = signal.detrend(v1)
    z2 = signal.detrend(v2)

    yf1 = fft(z1)
    yf2 = fft(z2)
    
    yf=abs(yf1[0:N1 // 2])
    xf = np.linspace(0.0, 1.0 / (2.0 * T), N1 // 2)

    yf3 = abs(yf2[0:N1 // 2])
    xf3 = np.linspace(0.0, 1.0 / (2.0 * T), N2 // 2)
    

    maximum_rpm_hz = max_rpm/60
    rms_fft_amplitude_Xi = np.sqrt(np.mean(np.square(yf)))

    amplitudesindex = [list(yf).index(i) for i in yf if i>1.2*rms_fft_amplitude_Xi ] #taking amplitude above 1.5*rms
    amplitudesvalues = [i for i in yf if i>1.2*rms_fft_amplitude_Xi]
    xf1 = list(xf)
    frequency = [xf1[i] for i in amplitudesindex ]#if i<=maximum_rpm #frequency corres to 1.25*rms amplitudes
    
    indexfreqencylesthanrpm = [frequency.index(i) for i in frequency if i<=maximum_rpm_hz]
    freqencylesthanrpmvalues = [frequency[i] for i in indexfreqencylesthanrpm ] #if i<=maximum_rpm
    amplitudeslessthanmaxRPM = [amplitudesvalues[i] for i in indexfreqencylesthanrpm]
    if (amplitudeslessthanmaxRPM)!=[]:  #Only if not empty 
        maxoneamplitude = max(amplitudeslessthanmaxRPM)
        indexofRPMamplitude = amplitudesvalues.index(maxoneamplitude)
        freuencycorrestomaxampl = freqencylesthanrpmvalues[indexofRPMamplitude]
        finalRPM = freuencycorrestomaxampl
    oneXend_limit = (max_rpm/60)*0.6   #Setting Minimum RPM based on Maximum RPM like 15 to 24 hz.
    if finalRPM>oneXend_limit:
        currentRPM = finalRPM
        # print('currentRPM',currentRPM)
        start_angle = int(90-30)
        end_angle = int(90+30)

        multi1xvalueFrequeAmplitudes_for_ratioX =[frequency.index(i) for i in frequency if ((currentRPM*2)-2)<= i <= ((currentRPM*2)+2) or ((currentRPM*3)-2)<= i <= ((currentRPM*3)+2)]
        multi1xvalueFreque =[i for i in frequency if (((currentRPM*2)-2)<= i <= ((currentRPM*2)+2)) or ((currentRPM*3)-2)<= i <= ((currentRPM*3)+2)]
        twoXrpmfreq = [i for i in  frequency if ((currentRPM*2)-2)<= i <= ((currentRPM*2)+2)]
        if twoXrpmfreq!=[]:
            twoXmax_amplitude = max([amplitudesvalues[frequency.index(i)] for i in twoXrpmfreq])
            maxamplfreq1x = frequency[amplitudesvalues.index(twoXmax_amplitude)]
        threeXrpmfreq = [i for i in  frequency if ((currentRPM*3)-2)<= i <= ((currentRPM*3)+2)]
        if threeXrpmfreq != []:
            threeXmax_amplitude = max([amplitudesvalues[frequency.index(i)] for i in threeXrpmfreq])
######################Below is 1st unbalance condition######################################
        # if twoXmax_amplitude < (maxoneamplitude*0.3) and threeXmax_amplitude<(maxoneamplitude*0.3):
        #     if  start_angle <= angle <= end_angle:
        #         print('2Unbalance')
                # print(currentRPM,maxoneamplitude,twoXmax_amplitude,threeXmax_amplitude)
        ##########################Above one for Horizontal Axes######################
        horizontal1xRPM = currentRPM  
        horizontal1xrpmAmplitude = maxoneamplitude

        yf3 = yf3
        xf3 = xf3

        axial_rms_amplitude = np.sqrt(np.mean(np.square(yf3)))
        axialamplitudesindex = [list(yf3).index(i) for i in yf3 if i>1.2*axial_rms_amplitude ] #taking amplitude above 1.5*rms
        axialamplitudesvalues = [i for i in yf3 if i>1.2*axial_rms_amplitude]
        axialxf = list(xf3)
        axialfrequency = [axialxf[i] for i in axialamplitudesindex]
        axial1xrangefreq_correspond_Horizontal = [axialfrequency.index(i) for i in axialfrequency if (horizontal1xRPM-1) < i < (horizontal1xRPM+1)]
        axial1xrangeAmplitude = [axialamplitudesvalues[i] for i in axial1xrangefreq_correspond_Horizontal]
        if axial1xrangeAmplitude!=[]:
            axial1xAmplitudeMAx = max(axial1xrangeAmplitude)
            axialFreQ = axialfrequency[axialamplitudesvalues.index(axial1xAmplitudeMAx)]
        if twoXmax_amplitude < (maxoneamplitude*0.4) and threeXmax_amplitude<(maxoneamplitude*0.4):
            if horizontal1xrpmAmplitude > axial1xAmplitudeMAx:
                if  start_angle <= angle <= end_angle:
                    print('2Unbalance')
                    
        
    
    
    # unbalance5(yf1,200,int(rpmis),90)
    windowsize += samplewindow
    windowsize1 += samplewindow
    






# Currently I'm taking all 2x and 3x peak values so code becomes wrong sometimes, because if your 1x peak frequency 
# is 15 and you are giving +2 or -2 rang eto find 2x peak frequency so it will take all 4 values in that
# if suppose 30 frequency's amplitude is 40% less than 1x amplitude but 32 frequency's amplitude is higher
# than 1x amplitude, but your program will consider amplitude which has lesser amplitude compared to
# 1x which is 3o it will take so program logic will become wrong.
# Instead you need to take 4 values in 2x range and find one 2x amplitude which is maximum and compare it's 
# amplitude to 1x amplitude.

# Next step: I'll take 1x rpm from horizontal axes, I;ll take it for reference frequency and amplitude.
# corresponding to 1x frequency take +2 to -2 range frequency values from axial axes in  case of horizontal
# shaft.
# corresponding to these frequency values
# take amplitudes and in that amplitude take maximum amplitude and compare this with 1x amplitude of horizontal
# axes if 1x amplitude of horizontal axes greater than axial axes in horizontal shaft motor then there is imbalance.



# Again made some changes previously I was looking for 2x frequency in that finding maximum frequency taking
# corresponding amplitude of that, now I'm taking 2x frequencies corresponding to that get amplitude which is maximum.
