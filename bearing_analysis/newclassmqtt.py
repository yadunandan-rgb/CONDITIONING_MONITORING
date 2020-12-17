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
nb=4
bd=0.76
p_d=0.56
angles=0
Shaftspeed=83
samplingFrequency=1600
nsamp=4096
windowsize=512
brokerport=1883
brokeraddress="176.19.34.01"
tagname="A434F17EE90B/FFTX"
nwindows=nsamp/windowsize
lim_value=0.3
fftlist=[2.3,3.4,5.3,3.4,3.04]
timetocompleteoneburst=nsamp/samplingFrequency
time_diff_btw_windows=timetocompleteoneburst/nwindows

class Bearing_analysis():

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
    

    def ftf_range(self): #NB,BD,PD,ANGLE are bearing inputs
        self.Fcir=((1/2)*(1-(self.B_D/self.P_D)*math.cos(self.Angle)))
        self.FTF=self.Fcir*self.Shaft_Speed #fundamental train frequency
        self.FTFFinal=float(self.FTF)
        rangelimit=self.FTFFinal*self.Limit_value
        self.FTFFinalrange1=float(self.FTFFinal+rangelimit)
        self.FTFFinalrange2=float(self.FTFFinal-rangelimit)
        return self.FTFFinalrange1,self.FTFFinalrange2
        
        #print(FTFFinal)
    def bsf_range(self): #NB,BD,PD,ANGLE are bearing inputs
        self.Bsf=((self.P_D/(2*self.B_D))*(1-((self.B_D/self.P_D)*(math.cos(self.Angle)))**2))
        self.BSF=self.Bsf*self.Shaft_Speed #ball spin frequency
        self.BSFFinal=float(self.BSF)
        rangelimit=self.BSFFinal*self.Limit_value
        self.BSFFinalrange1=float(self.BSFFinal+rangelimit)
        self.BSFFinalrange2=float(self.BSFFinal-rangelimit)
        return self.BSFFinalrange1,self.BSFFinalrange2
    def bpfi_range(self):   
        #print(BSFFinal) 
        self.Bfir=((self.N_B/2)*(1+(self.B_D/self.P_D)*math.cos(self.Angle)))
        self.BPFI=self.Bfir*self.Shaft_Speed #ball pass frequency of inner race
        self.BPFIFinal=float(self.BPFI)
        rangelimit=self.BPFIFinal*self.Limit_value
        self.BPFIFinalrange1=float(self.BPFIFinal+rangelimit)
        self.BPFIFinalrange2=float(self.BPFIFinal-rangelimit)
        return self.BPFIFinalrange1,self.BPFIFinalrange2
        #(FTFFinal)
        
        #print(BPFIFinal) 
    def bpfo_range(self):      
        self.Bfor=((self.N_B/2)*(1-(self.B_D/self.P_D)*math.cos(self.Angle)))
        self.BPFO=self.Bfor*self.Shaft_Speed #ball pass frequency  of outer race
        self.BPFOFinal=float(self.BPFO)
        rangelimit=self.BPFOFinal*self.Limit_value
        self.BPFOFinalrange1=float(self.BPFOFinal+rangelimit)
        self.BPFOFinalrange2=float(self.BPFOFinal-rangelimit)
        return self.BPFOFinalrange1,self.BPFOFinalrange2
        
        #print(BPFOFinal) 
        
        

        #return BPFIFinal
####on passing averaged fft values ,getting corresponding frequencies of amplitudes which are above the RMS value.
##fftavg=averaged fft values ####samplingFrequency of the sensor ###window size of the data.

    
    def FFT_calculations(self):
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
        return self.HorizontAmplitudAbove_rms_values,self.corres_frequency,self.rms #returns the ampltide,frqns, and rms 
    ##R1=bcf of FTF, R2=BCF of BSF ,samplingFrequency,
    ##lst=frequencies after 


class Bearing_analysis2(Bearing_analysis):

    def FTF_analysis(self): #checks whether ftf therotical frequencies  range matches the the frqns greater then rms obtained from the parser
        
        global result
        for x in self.corres_frequency: 
            
            if x>= self.FTFFinalrange2 and x<= self.FTFFinalrange1: #first harmonic check
                result= "first harmonic FTF fault"
                
                self.resultant.append(result)
            if x>= 2*self.FTFFinalrange2 and x<= 2*self.FTFFinalrange1:##second harmonic check
                result="2nd harmonic ftf fault"
                #print("2nd ftf")
                self.resultant.append(result)

            if x>= 3*self.FTFFinalrange2 and x<= 3*self.FTFFinalrange1: ##third harmonic check
                result="3rd harmonic FTF fault"
                #print("3rd ftf")
                self.resultant.append(result)

        return self.resultant   
                    
    def BSF_analysis(self): #checks whether bsf therotical frequencies  range matches the the frqns greater then rms obtained from the parser
        
        global result
        
        for x in self.corres_frequency:
            if x>= self.BSFFinalrange2 and x<= self.BSFFinalrange1: #first harmonic check
                result= "first harmonic bsf fault"
                #print("first bsf")
                self.resultant1.append(result)

            if x>= 2*self.BSFFinalrange2 and x<= 2*self.BSFFinalrange1:#second harmonic check
                result="2nd harmonic bsf fault"
                
                #print("2nd bsf")
                self.resultant1.append(result)

                #return (result)
            if x>= 3*self.BSFFinalrange2 and x<= 3*self.BSFFinalrange1: #third harmonic check
                result="3rd harmonic bsf fault"
                #print("3rd bsf")
                self.resultant1.append(result)
        return self.resultant1   

    def OUTERRACE_analysis(self):#checks whether outerrace therotical frequencies  range matches the the frqns greater then rms obtained from the parser
        
        global result
        for x in self.corres_frequency:
            if x>= self.BPFOFinalrange2 and x<= self.BPFOFinalrange1: #first harmonic check
                result= "first harmonic outerrace fault"
                #print("first outerrace")
                self.resultant2.append(result)

            if x>= 2*self.BPFOFinalrange2 and x<= 2*self.BPFOFinalrange1: #second harmonic check
                result="2nd harmonic outerrace fault"
                #print("2nd outerrace")
                self.resultant2.append(result)

            if x>= 3*self.BPFOFinalrange2 and x<= 3*self.BPFOFinalrange1:#third harmonic check
                result="3rd harmonic outerrace fault"
                #print("3rd outerrace")
                self.resultant2.append(result)
        return self.resultant2   

                            
    def INNERRACE_analysis(self): #checks whether innerrace therotical frequencies  range matches the the frqns greater then rms obtained from the parser
        
        global result
        for x in self.corres_frequency:
            if x>= self.BPFIFinalrange2 and x<= self.BPFIFinalrange1:   #first harmonic check
                result= "first harmonic innerrace fault"
                #print("first innerrace")
                self.resultant3.append(result)

            if x>= 2*self.BPFIFinalrange2 and x<= 2*self.BPFIFinalrange1: #second harmonic check
                result="2nd harmonic innerrace fault"
                #print("2nd innerrace")
                self.resultant3.append(result)

            if x>= 3*self.BPFIFinalrange2 and x<= 3*self.BPFIFinalrange1: #third harmonic check
                result="3rd harmonic innerrace fault" 
                #print("3rd innerrace")
                self.resultant3.append(result)
        return self.resultant3   
bearing=Bearing_analysis(nb,bd,p_d,angles,Shaftspeed,samplingFrequency,nsamp,windowsize,fftlist)
        
ftf_range1,ftf_range2=bearing.ftf_range() #bearing characterstics frequencies are calculated 
bsf_range1,bsf_range2=bearing.bsf_range()     
bpfo_range1,bpfo_range2=bearing.bpfo_range()
bpfi_range1,bpfi_range2=bearing.bpfi_range()
#print(int(a2),int(a1),int(a4),int(a3),int(a6),int(a5),int(a8),int(a7))

amp,frqn,rms=bearing.FFT_calculations() #using the fft caluclation function calculates the frequencies corresponding amplitudes greater than 3*rms
#print("freqn is",freqs)
bearing2=Bearing_analysis2(nb,bd,p_d,angles,Shaftspeed,samplingFrequency,nsamp,windowsize,fftlist)
f1=bearing2.FTF_analysis() #checks whether ftf therotical frequencies  range matches the the frqns greater then rms obtained from the parser
print(f1)
        #client.publish(pubishing_tag,f1)
b1=bearing2.BSF_analysis() #checks whether bsf therotical frequencies  range matches the the frqns greater then rms obtained from the parser
print(b1) 
        #client.publish(pubishing_tag,b1)
i1=bearing2.INNERRACE_analysis() #checks whether innerace therotical frequencies  range matches the the frqns greater then rms obtained from the parser
print(i1)
        #client.publish(pubishing_tag,i1)
o1=bearing2.OUTERRACE_analysis() #checks whether outerace therotical frequencies  range matches the the frqns greater then rms obtained from the parser
print(o1)

#client.publish(pubishing_tag,o1)
if sum([len(f1),len(b1),len(o1),len(i1)]) == 0: #checks whether list are empty 
    print("bearing is healthy")
else:
    print("bearing has some problem")

f1.clear()
b1.clear() #clears all the list 
i1.clear()
o1.clear()