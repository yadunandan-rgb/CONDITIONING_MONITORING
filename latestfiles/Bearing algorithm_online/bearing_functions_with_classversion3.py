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


class BEARING_analysis():

    def __init__(self,NB,BD,PD,angle,shaftspeed,samplingFrequency,nsamp,windowsize,fftlist):
        self.Limit_value=float(0.3)
        self.N_B=int(NB)
        self.B_D=float(BD)
        self.P_D=float(PD)
        self.Angle=float(angle)
        self.Shaft_Speed=shaftspeed
        self.Sampling_Frequency=samplingFrequency
        self.No_sample=nsamp
        self.Window_Size = windowsize
        self.FFT_list=fftlist
        self.resultant=[]
        self.resultant1=[]
        self.resultant2=[]
        self.resultant3=[]
        
#####function for handling log functions ####################
    

    def FTF_range(self): #NB,BD,PD,ANGLE are bearing inputs
        try:
            self.Fcir=((1/2)*(1-(self.B_D/self.P_D)*math.cos(self.Angle)))
            self.FTF=self.Fcir*self.Shaft_Speed #fundamental train frequency
            self.FTFFinal=float(self.FTF)
            rangelimit=self.FTFFinal*self.Limit_value
            self.FTFFinalrange1=float(self.FTFFinal+rangelimit)
            self.FTFFinalrange2=float(self.FTFFinal-rangelimit)
            return self.FTFFinalrange1,self.FTFFinalrange2
        except Exception as e:
            print(str(e))    
        #print(FTFFinal)
    def BSF_range(self): #NB,BD,PD,ANGLE are bearing inputs
        try:
            self.Bsf=((self.P_D/(2*self.B_D))*(1-((self.B_D/self.P_D)*(math.cos(self.Angle)))**2))
            self.BSF=self.Bsf*self.Shaft_Speed #ball spin frequency
            self.BSFFinal=float(self.BSF)
            rangelimit=self.BSFFinal*self.Limit_value
            self.BSFFinalrange1=float(self.BSFFinal+rangelimit)
            self.BSFFinalrange2=float(self.BSFFinal-rangelimit)
            return self.BSFFinalrange1,self.BSFFinalrange2
        except Exception as e:
            print(str(e))
    def BPFI_range(self):   
        #print(BSFFinal) 
        try:
            self.Bfir=((self.N_B/2)*(1+(self.B_D/self.P_D)*math.cos(self.Angle)))
            self.BPFI=self.Bfir*self.Shaft_Speed #ball pass frequency of inner race
            self.BPFIFinal=float(self.BPFI)
            rangelimit=self.BPFIFinal*self.Limit_value
            self.BPFIFinalrange1=float(self.BPFIFinal+rangelimit)
            self.BPFIFinalrange2=float(self.BPFIFinal-rangelimit)
            return self.BPFIFinalrange1,self.BPFIFinalrange2
        except Exception as e:
            print(str(e))
        #(FTFFinal)
        
        #print(BPFIFinal) 
    def BPFO_range(self):      
        try:

            self.Bfor=((self.N_B/2)*(1-(self.B_D/self.P_D)*math.cos(self.Angle)))
            self.BPFO=self.Bfor*self.Shaft_Speed #ball pass frequency  of outer race
            self.BPFOFinal=float(self.BPFO)
            rangelimit=self.BPFOFinal*self.Limit_value
            self.BPFOFinalrange1=float(self.BPFOFinal+rangelimit)
            self.BPFOFinalrange2=float(self.BPFOFinal-rangelimit)
            return self.BPFOFinalrange1,self.BPFOFinalrange2
        except Exception as e:
            print(str(e))    
        #print(BPFOFinal) 
        
        

        #return BPFIFinal
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
    def FTF_analysis(self,range1,range2,frequency): #checks whether ftf therotical frequencies  range matches the the frqns greater then rms obtained from the parser
        #self.corres_frequency=frequency
        try:
            global result
            for x in frequency: 
                
                if x>=range1 and x<=range2: #first harmonic check
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
    def BSF_analysis(self,range1,range2,frequency): #checks whether bsf therotical frequencies  range matches the the frqns greater then rms obtained from the parser
        #self.corres_frequency=frequency
        try:
            global result
            
            for x in frequency:
                if x>=range1 and x<=range2: #first harmonic check
                    result= "first harmonic bsf fault"
                    #print("first bsf")
                    self.resultant1.append(result)

                if x>= 2*range1 and x<= 2*range2:#second harmonic check
                    result="2nd harmonic bsf fault"
                    
                    #print("2nd bsf")
                    self.resultant1.append(result)

                    #return (result)
                if x>= 3*range1 and x<= 3*range2: #third harmonic check
                    result="3rd harmonic bsf fault"
                    #print("3rd bsf")
                    self.resultant1.append(result)
            return self.resultant1   
        except Exception as e:
            print(str(e))
    def OUTERRACE_analysis(self,range1,range2,frequency):#checks whether outerrace therotical frequencies  range matches the the frqns greater then rms obtained from the parser
        #self.corres_frequency=frequency
        try:
            global result
            for x in frequency:
                if x>= range1 and x<=range2: #first harmonic check
                    result= "first harmonic outerrace fault"
                    #print("first outerrace")
                    self.resultant2.append(result)

                if x>= 2*range1 and x<= 2*range2: #second harmonic check
                    result="2nd harmonic outerrace fault"
                    #print("2nd outerrace")
                    self.resultant2.append(result)

                if x>= 3*range1 and x<= 3*range2:#third harmonic check
                    result="3rd harmonic outerrace fault"
                    #print("3rd outerrace")
                    self.resultant2.append(result)
            return self.resultant2   
        except Exception as e:
            print(str(e))
                            
    def INNERRACE_analysis(self,range1,range2,frequency): #checks whether innerrace therotical frequencies  range matches the the frqns greater then rms obtained from the parser
        #self.corres_frequency=frequency
        try:
            global result
            for x in frequency:
                if x>= range1 and x<=range2:   #first harmonic check
                    result= "first harmonic innerrace fault"
                    #print("first innerrace")
                    self.resultant3.append(result)

                if x>= 2*range1 and x<= 2*range2: #second harmonic check
                    result="2nd harmonic innerrace fault"
                    #print("2nd innerrace")
                    self.resultant3.append(result)

                if x>= 3*range1 and x<= 3*range2: #third harmonic check
                    result="3rd harmonic innerrace fault" 
                    #print("3rd innerrace")
                    self.resultant3.append(result)
            return self.resultant3
        except Exception as e:
            print(str(e)) 
    def BEARING_total(self):
        try:
            ftfrange1,ftfrange2=self.FTF_range()
            bsfrange1,bsfrange2=self.BSF_range()
            bpfirange1,bpfirange2=self.BPFI_range()
            bpforange1,bpforange2=self.BPFO_range()
            fft_frqn=self.FFT_calculations()
            bearing_ftfresult=self.FTF_analysis(ftfrange2,ftfrange1,fft_frqn)
            bearing_bsfresult=self.BSF_analysis(bsfrange2,bsfrange1,fft_frqn)
            bearing_bpfiresult=self.INNERRACE_analysis(bpfirange2,bpfirange1,fft_frqn)
            bearing_bpforesult=self.OUTERRACE_analysis(bpforange2,bpforange1,fft_frqn)
            return bearing_ftfresult,bearing_bsfresult,bearing_bpfiresult,bearing_bpforesult
        except Exception as e:
            print(str(e))