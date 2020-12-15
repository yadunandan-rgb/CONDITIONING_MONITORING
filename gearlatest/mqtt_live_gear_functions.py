# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 10:59:41 2020

@author: User
"""

#### libraries ###############
import math 
import pandas as pd
import numpy as np
import heapq

#####to calculate bearing characteristic frequency #####
##BCF=bearing characteristic frequency
###NB=number of balls or rollers ,BD=ball or roller diameter 
###PD=Pitch Diameter 
##FTF=fundamental train frequency, BPFI=Ball Pass Frequency of Inner Race
##BPFO=Ball Pass Frequency of OuterRace , BSF=Ball Spin Frequency
def Rpm_version(fft_signal,sampling_freq, Max_rpm):
    maximum_rpm_hz = Max_rpm/60
    rpm_thresholdStart = 0.3* maximum_rpm_hz
    rpm_thresholdend = 1.2*maximum_rpm_hz
    sampling_fre = sampling_freq
    time = 1/sampling_fre
    fft = fft_signal
    no_of_samples = len(fft_signal)

    fft_y=(np.array(fft_signal[0:no_of_samples]))
    fft_x = np.linspace(0.0, 1.0 / (2.0 * time), no_of_samples)
    
    fft_x_list = list(fft_x)
    amplitudesindex = [list(fft_y).index(i) for i in fft_y]
    amplitudesvalues = [float(i) for i in fft_y]
    frequency = [fft_x_list[i] for i in amplitudesindex ]
    indexfreqencylesthanrpm = [frequency.index(i) for i in frequency if rpm_thresholdStart<=i<=rpm_thresholdend]
    indexfreqencylesthanrpmvalues = [frequency[i] for i in indexfreqencylesthanrpm ] #if i<=maximum_rpm
    

    amplitudesrpm = [amplitudesvalues[i] for i in indexfreqencylesthanrpm]
    largeinamplitud=heapq.nlargest(10,amplitudesrpm)
    indexofMaxAmplit = [amplitudesvalues.index(i) for i in largeinamplitud]
    frequencyforMaxamplit = [frequency[i] for i in indexofMaxAmplit]

    if amplitudesrpm!=[]:

        maxoneamplitude = max(amplitudesrpm)
        indexofamplitude = amplitudesvalues.index(maxoneamplitude)

        freuencycorrestomaxampl = frequency[indexofamplitude]
        rpmfreqCorresfreuencycorrestomaxampl = [i for i in frequencyforMaxamplit if i-1 <= freuencycorrestomaxampl/4 <= i+1 or i-1 <= freuencycorrestomaxampl/3 <= i+1 or i-1 <= freuencycorrestomaxampl/2 <= i+1]
        rpmfreqcorresto2x3x = [j for j in frequencyforMaxamplit for i in frequencyforMaxamplit if j-1 <= i/4 <= j+1 or j-1 <= i/3 <= j+1 or j-1 <= i/2 <= j+1 ]
    
# Here considering only maximum amplitude under rpm range
        if rpmfreqcorresto2x3x==[] and maxoneamplitude!=[]:
            rpmAmplitude = maxoneamplitude
            rpmis = freuencycorrestomaxampl
        # print('first',freuencycorrestomaxampl)
            return rpmis, rpmAmplitude
        else:
        
            rpmis = (rpmfreqcorresto2x3x[0])
        # print('second',rpmis)
            rpmis2_index = frequency.index(rpmis)
            rpm2_amplitude = amplitudesvalues[rpmis2_index]
            rpmAmplitude = rpm2_amplitude
       
            return rpmis,rpmAmplitude
##function defines the bearing charcterstic freqns
def gear_calculation(No_of_teeth_pinion,frequency_of_pinion):
    GMFF=float(frequency_of_pinion*No_of_teeth_pinion)##355
    return GMFF#gear theriotical fault frequency
def Fault_range(inputvalue,lim): ## decides the ranges of fault frequencies
    rangelimit=inputvalue*lim
    Finalrange1=float(inputvalue+rangelimit)
    Finalrange2=float(inputvalue-rangelimit)
    return Finalrange1,Finalrange2
    
####on passing averaged fft values ,getting corresponding frequencies of amplitudes which are above the RMS value.
##fftavg=averaged fft values ####samplingFrequency of the sensor ###window size of the data.

def FFT_calculations(fftavg,freqns,samplingFrequency,windowsize):
    lst1=fftavg  ####fftavg should be in pandas.core.series.Series
    rms =np.sqrt(np.mean(np.square(lst1))) #fft values re averaged
    Amplitude_rms_index = [list(lst1).index(i) for i in lst1 if i>3*rms] #checks for amplitudes index greater thn 3*rms
    #print(Amplitude_rms_index)
    HorizontAmplitudAbove_rms_values = [i for i in lst1 if i>3*rms] #checks for the amplitudes for the above index values
    #print(HorizontAmplitudAbove_rms_values)
    corres_frequency = [list(freqns)[i] for i in Amplitude_rms_index] #corresponding freqns of amplitudes greater than 3*rms
    print(corres_frequency)
    return HorizontAmplitudAbove_rms_values,corres_frequency,rms #returns the ampltide,frqns, and rms 
##R1=bcf of FTF, R2=BCF of BSF ,samplingFrequency,
##lst=frequencies after 


resultant=[]
  
def GMFF_ANALYSIS(input1,faultrange1,faultrange2):
    global result
    for x in input1: 
        
        if x>= faultrange1 and x<= faultrange2:
            result= "first harmonic GMFF fault"
            #print("first GMFF")
            resultant.append(result)
        if x>= 2*faultrange1 and x<= 2*faultrange2:
            result="2nd harmonic GMFF fault"
            #print("2nd GM")
            resultant.append(result)

        if x>= 3*faultrange1 and x<=3*faultrange2:
            result="3rd harmonic gmff fault"
            #print("3rd gmff")
            resultant.append(result)

    return resultant   