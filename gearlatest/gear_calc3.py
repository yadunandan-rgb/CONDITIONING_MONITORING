# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 13:17:29 2020

@author: User
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 13:04:27 2020

@author: User
"""

import pandas as pd
import numpy as np
import heapq
def rpm1st_version(preferHorizont_fft_y,preferHorizont_fft_x,sampling_frequency, Max_rpm):
    maximum_rpm_hz = Max_rpm/60
    fft_ = preferHorizont_fft_y
    no_of_samples = len(fft_)
    sampling_frequency = sampling_frequency
    time_period = 1/sampling_frequency

    fft_y_axes=preferHorizont_fft_y
    fft_x_axes = preferHorizont_fft_x

    fft_x_axes_list = list(fft_x_axes)

    amplitudesindex = [list(fft_y_axes).index(i) for i in fft_y_axes]
    amplitudesvalues = [float(i) for i in fft_y_axes]
    frequency = [fft_x_axes_list[i] for i in amplitudesindex ]#if i<=maximum_rpm
    indexfreqencylesthanrpm = [frequency.index(i) for i in frequency if i<=maximum_rpm_hz]
    indexfreqencylesthanrpmvalues = [frequency[i] for i in indexfreqencylesthanrpm ] #if i<=maximum_rpm
    amplitudesofrpm = [amplitudesvalues[i] for i in indexfreqencylesthanrpm]
    maxoneamplitude = max(amplitudesofrpm)
    indexofrpmamplitude = amplitudesvalues.index(maxoneamplitude)
    freuencycorrestomaxampl = indexfreqencylesthanrpmvalues[indexofrpmamplitude]
    return freuencycorrestomaxampl

def faultrange(inputvalue,lim):
    rangelimit=inputvalue*lim
    Finalrange1=float(inputvalue+rangelimit)
    Finalrange2=float(inputvalue-rangelimit)
    return Finalrange1,Finalrange2
    
    
    
    
####calculating BCF taking fault frequency ranges and shaft speed as input
# Vibration Frequency Fundamental Train:=FT
##Vibration Frequency Inner Ring Defect: VFIR
#Vibration Frequency Outer Ring Defect:  VFOR
#Vibration Frequency Roller Spin: VFRS  
#shaft speed in RPM
def my_function(x):
    return list(dict.fromkeys(x)) 

def gear_calculation(No_of_teeth_pinion,frequency_of_pinion):
   #frequency_of_pinion=float(Speed_of_pinion1)
   GMFF=float(frequency_of_pinion*No_of_teeth_pinion)##355
   return GMFF
def fftcalculations(fftavg,freqns,samplingFrequency,windowsize):
    lst1=fftavg  ####fftavg should be in pandas.core.series.Series
    rms =np.sqrt(np.mean(np.square(lst1)))
    Amplitude_rms_index = [list(lst1).index(i) for i in lst1 if i>3*rms]
    #print(Amplitude_rms_index)
    HorizontAmplitudAbove_rms_values = [i for i in lst1 if i>3*rms]
    #print(HorizontAmplitudAbove_rms_values)
    corres_frequency = [list(freqns)[i] for i in Amplitude_rms_index]
    print(corres_frequency)
    return HorizontAmplitudAbove_rms_values,corres_frequency,rms
resultant=[]
resultant1=[] 
resultant2=[]
resultant3=[]  

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