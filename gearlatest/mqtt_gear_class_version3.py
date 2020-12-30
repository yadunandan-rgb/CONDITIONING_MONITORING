import paho.mqtt.client as mqtt  #import the client1
import time
from configparser import ConfigParser
import logging
import sys
from collections import deque
import logging.handlers as handlers
import pandas as pd
import datetime
import json
import numpy as np
import math

class GEAR_analysis():
    

    def __init__(self,speed_of_pinion,number_of_teeth_pinion,samplingFrequency,nsamp,windowsize,fftlist):
        self.Limit_value=float(0.3)
        self.Speed_of_pinion=float(speed_of_pinion)
        self.Number_of_teeth_pinion=int(number_of_teeth_pinion)
        self.Sampling_Frequency=float(samplingFrequency)
        self.No_sample=int(nsamp)
        self.Window_Size = int(windowsize)
        self.FFT_list=fftlist
        self.resultant=[]
        self.resultant1=[]
        self.resultant2=[]
        self.resultant3=[]
        
#####function for handling log functions ####################
    

    def GEAR_range(self): #NB,BD,PD,ANGLE are bearing inputs
        try:
            self.GMFF=float(self.Speed_of_pinion*self.Number_of_teeth_pinion)##355
            rangelimit=self.GMFF*self.Limit_value
            self.GMFFFinalrange1=float(self.GMFF+rangelimit)
            self.GMFFFinalrange2=float(self.GMFF-rangelimit)
            return self.GMFFFinalrange1,self.GMFFFinalrange2                
                        
        except Exception as e:
            print(str(e))

        
        
####on passing averaged fft values ,getting corresponding frequencies of amplitudes which are above the RMS value.
##fftavg=averaged fft values ####samplingFrequency of the sensor ###window size of the data.

    
    def FFT_calculations(self):
        try:
            self.average= [sum(e)/len(e) for e in zip(*self.FFT_list)]
            self.xf = np.linspace(0.0, 1.0 / (2.0 * (1/self.Sampling_Frequency)), len(self.average))  #frequencies selection
            ####fftavg should be in pandas.core.series.Series
            self.rms =np.sqrt(np.mean(np.square(self.average))) #fft values are averaged
            self.Amplitude_rms_index = [list(self.average).index(i) for i in self.average if i>3*self.rms] #checks for amplitudes index greater thn 3*rms
            #print(Amplitude_rms_index)
            self.HorizontAmplitudAbove_rms_values = [i for i in self.average if i>3*self.rms] #checks for the amplitudes for the above index values
            #print(HorizontAmplitudAbove_rms_values)
            self.corres_frequency = [list(self.xf)[i] for i in self.Amplitude_rms_index] #corresponding freqns of amplitudes greater than 3*rms
            #print(corres_frequency)
            return self.corres_frequency #returns the ampltide,frqns, and rms 
        except Exception as e:
            print(str(e))


    def GMFF_analysis(self,range1,range2,frequency): #checks whether ftf therotical frequencies  range matches the the frqns greater then rms obtained from the parser
        #self.corres_frequency=frequency
        try:
            global result
            for x in frequency: 
                
                if x>= range1 and x<=range2: #first harmonic check
                    result= "first harmonic FTF fault"
                    
                    self.resultant.append(result)
                if x>= 2*range1 and x<= 2*range2:##second harmonic check
                    result="2nd harmonic ftf fault"
                    #print("2nd ftf")
                    self.resultant.append(result)

                if x>= 3*range1 and x<= 3*range2: ##third harmonic check
                    result="3rd harmonic FTF fault"
                    #print("3rd ftf")
                    self.resultant.append(result)

            return self.resultant
        except Exception as e:
            print(str(e))
    
    def GEAR_total(self):
        try:

            gearrange1,gearrange2=self.GEAR_range()
            fft_frqns=self.FFT_calculations()
            gear_result=self.GMFF_analysis(gearrange2,gearrange1,fft_frqns)
            return gear_result
        except Exception as e:
            print(str(e))

                    
    