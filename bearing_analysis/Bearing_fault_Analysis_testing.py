# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 22:07:01 2020

@author: Ananda
"""

from configparser import ConfigParser
import math 
from numpy import mean, sqrt, square, arange
import pandas as pd
import numpy as np

config_object = ConfigParser()
config_object.read("C:/Users/Chethan/Downloads/userinfo6.ini")
userinfo = config_object["user_info"]
NB=int(userinfo["NB"]) #Number of Rolling Element or Ball
BD=int(userinfo["BD"]) #Rolling Element or Ball Diameter
PD=int(userinfo["PD"]) #pitch circle diameter of the bearing
angle=int(userinfo["angle"]) #Contact Angle
RPM=float(userinfo["RPM"])#rpm 
shaftspeed=RPM/60 #Shaft Rotational Speed
CFrange_allowance=20 ###percentage of characteristic frequency Range allowance
afterallowance=(100-CFrange_allowance)/100
faultFreqallowance=2 ###percentage of fault frequency Range allowance
afterfaultfreqallowanceplus=(100+faultFreqallowance)/100
afterfaultfreqallowanceminus=(100-faultFreqallowance)/100
samplingFrequency=1600
windowsize=256
####calculating BCF #######

def BCF(NB,BD,PD,angle,shaftspeed):
    Fcir=((1/2)*(1-(BD/PD)*math.cos(angle)))
    FTF=Fcir*shaftspeed #fundamental train frequency
    FTFFinal=int(FTF)
    print(FTFFinal)
    
    Bfir=((NB/2)*(1+(BD/PD)*math.cos(angle)))
    BPFI=Bfir*shaftspeed #ball pass frequency of inner race
    BPFIFinal=int(BPFI)
    print(BPFIFinal) 
    
    Bfor=((NB/2)*(1-(BD/PD)*math.cos(angle)))
    BPFO=Bfor*shaftspeed #ball pass frequency  of outer race
    BPFOFinal=int(BPFO)
    print(BPFOFinal) 
    
    Bsf=((PD/(2*BD))*(1-((BD/PD)*(math.cos(angle)))**2))
    BSF=Bsf*shaftspeed #ball spin frequency
    BSFFinal=int(BSF)
    print(BSFFinal)       

    return  FTFFinal, BSFFinal, BPFOFinal, BPFIFinal

R1,R2,R3,R4=BCF(NB,BD,PD,angle,shaftspeed)
lst1=average
rms =sqrt(mean(square(lst1)))  #####rms of fft values
count = len([i for i in lst1 if i > 1.2*rms]) ####count of values which are greater than 1.2 times the RMS
ac=sorted([(x,i) for (i,x) in enumerate(lst1)], reverse=True )[:count]  ######correspondig frequency and amplitudes greater than 1.2xRMS 
ad=pd.DataFrame(ac,columns=['amplitude','Frequency'])
lst=ad['Frequency']*((samplingFrequency/2)/windowsize)
FTF=[i for i in lst if i in range(int(afterallowance*R1),int(afterallowance*R2))]
if len(FTF)>0:
    ffreq=[] #####fault frequencies
    print('first harmonics are present')
    for N in range(len(FTF)):
        print('first harmonic is',FTF[N])
        tfshrs=int(2*afterfaultfreqallowanceminus*FTF[N]) ####train frequency second harmonic range start value
        tfshre=int(2*afterfaultfreqallowanceplus*FTF[N]) #####train frequency second harmonic range end value
        if tfshrs > int(0.5*samplingFrequency):
            print("sampling frequency of the sensor is not enough for the analysis")
        else:
            change=[k for k in lst if k in range(tfshrs,tfshre)]
            if len(change)>0:
                print('second harmonic ranges are ',range(tfshrs,tfshre))
                print('second harmonic is present',change)
                tftrs=int(3*afterfaultfreqallowanceminus*FTF[N]) ###spin frequency third harmonic range start value
                tftre=int(3*afterfaultfreqallowanceplus*FTF[N]) ####spin frequency third harmonic range end value
                if tftrs > int(0.5*samplingFrequency):
                    print("sampling frequency of the sensor is not enough for the analysis")
                else:
                    change1=[i for i in lst if i in range(tftrs,tftre)]
                    if len(change1)>0:
                        print('third harmonic ranges are ',range(tftrs,tftre))
                        print('third harmonic is present',change1)
                        print('it is a strong evidence for train frequency fault')
                        
BSF=sorted([i for i in lst if i in range(int(afterallowance*R2),int(afterallowance*R3))])
if len(BSF) > 0:
    print('first harmonics are present')
    for M in range(len(BSF)):
        print('first harmonic is',BSF[M])
        sfshrs=int(2*afterfaultfreqallowanceminus*BSF[M]) ####spin frequency second harmonic range start value
        sfshre=int(2*afterfaultfreqallowanceplus*BSF[M]) #####spin frequency second harmonic range end value
        if sfshrs > int(0.5*samplingFrequency):
            print("sampling frequency of the sensor is not enough for the analysis")
        else:
            change=[k for k in lst if k in range(sfshrs,sfshre)]
            if len(change)>0:
                print('second harmonic ranges are ',range(sfshrs,sfshre))
                print('second harmonic is present',change)
                sftrs=int(3*afterfaultfreqallowanceminus*BSF[M]) ###spin frequency third harmonic range start value
                sftre=int(3*afterfaultfreqallowanceplus*BSF[M]) ####spin frequency third harmonic range end value
                if sftrs > int(0.5*samplingFrequency):
                    print("sampling frequency of the sensor is not enough for the analysis")
                else:
                    change1=[i for i in lst if i in range(sftrs,sftre)]
                    if len(change1)>0:
                        print('third harmonic ranges are ',range(sftrs,sftre))
                        print('third harmonic is present',change1)
                        print('it is a strong evidence for outerrace')

BPFO=sorted([i for i in lst if i in range(int(afterallowance*R3),int(afterallowance*R4))])
if len(BPFO) > 0:
    print('first harmonics are present')
    for j in range(len(BPFO)):
        print('first harmonic is',BPFO[j])
        oshrs=int(2*afterfaultfreqallowanceminus*BPFO[j]) ####outer race second harmonic range start value
        oshre=int(2*afterfaultfreqallowanceplus*BPFO[j]) #####outer race second harmonic range end value
        if oshrs > int(0.5*samplingFrequency):
            print("sampling frequency of the sensor is not enough for the analysis")
        else:
            change=[k for k in lst if k in range(oshrs,oshre)]
            if len(change)>0:
                print('second harmonic ranges are ',range(oshrs,oshre))                 
                print('second harmonic is present',change)
                otrs=int(3*afterfaultfreqallowanceminus*BPFO[j]) ###outer race third harmonic range start value
                otre=int(3*afterfaultfreqallowanceplus*BPFO[j]) #### outer race third harmonic range end value
                if otrs > int(0.5*samplingFrequency):
                    print("sampling frequency of the sensor is not enough for the analysis")
                else:
                    change1=[i for i in lst if i in range(otrs,otre)]
                    if len(change1)>0:
                        print('third harmonic ranges are ',range(otrs,otre))
                        print('third harmonic is present',change1)
                        print('it is a strong evidence for outerrace')
                        
BPFI=sorted([i for i in lst if i>int(afterallowance*R4)])
if len(BPFI)>0:
    print('first harmonics are present')
    for i in range(len(BPFI)):
        print('first harmonic is',BPFI[i])
        ishrs=int(2*afterfaultfreqallowanceminus*BPFI[i]) ####inner race second harmonic range start value
        ishre=int(2*afterfaultfreqallowanceplus*BPFI[i]) #####inner race second harmonic range end value
        if ishrs > int(0.5*samplingFrequency):
            print("sampling frequency of the sensor is not enough for the analysis")
        else:
            change=[i for i in lst if i in range(ishrs,ishre)]
            if len(change)>0:
                print('second harmonic ranges are ',range(ishrs,ishre))
                print('second harmonic is present',change)
                itrs=int(3*afterfaultfreqallowanceminus*BPFI[i]) ###inner race third harmonic range start value
                itre=int(3*afterfaultfreqallowanceplus*BPFI[i]) #### inner race third harmonic range end value
                if itrs > int(0.5*samplingFrequency):
                    print("sampling frequency of the sensor is not enough for the analysis")
                else:
                    change1=[i for i in lst if i in range(itrs,itre)]
                    if len(change1)>0:
                        print('third harmonic ranges are ',range(itrs,itre))
                        print('third harmonic is present',change1)
                        print('it is a strong evidence for innerrace')


        