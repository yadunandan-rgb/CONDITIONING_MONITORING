###libraries ####
import pandas as pd
import numpy as np
import math
from configparser import ConfigParser
import os
import matplotlib.pyplot as plt

####changing wworking directory

import Bearing_analysis_function_6 as fun
list1=[]
###input parameters ###
config_object = ConfigParser()
config_object.read(r'G:/bearinglatest2/userinfo6.ini')

####calling the userinfo object.
userinfo = config_object["user_info"]

#Number of Rolling Element or Ball
NB=int(userinfo["NB"])

#Rolling Element or Ball Diameter 
BD=float(userinfo["BD"]) 

#pitch circle diameter of the bearing
PD=float(userinfo["PD"]) 

#Contact Angle
angle=int(userinfo["angle"]) 

#rpm 
#RPM=float(userinfo["RPM"])
#Shaft Rotational Speed
#shaftspeed=RPM/60 

###percentage of characteristic frequency Range allowance
CFrange_allowance=10

###percentage of fault frequency Range allowance
faultFreqallowance=10

###sensor details 
samplingFrequency=1600

##number of samples
nsamp=4096
resultant=[]

###window size 
windowsize=512
T=1/samplingFrequency
###number of windows per burst
nwindows=int(nsamp/windowsize)

####the value after the percentage of characteristic frequency Range allowance
afterallowance=(100-CFrange_allowance)/100

###value after adding the percentage of fault frequency Range allowance
afterfaultfreqallowanceplus=(100+faultFreqallowance)/100

###value after substracting the percentage of fault frequency Range allowance
afterfaultfreqallowanceminus=(100-faultFreqallowance)/100

###calculating bearing characteristic frequencies
####input data #############
basf=pd.read_csv(r'G:/bearinglatest2/bearingtesting/data/outerrace_fault.csv',skiprows=1,header=None)
########################
basf.replace(regex=True, inplace=True, to_replace=r'[^0-9.E-]', value=r'')
# a=basf.select_dtypes(object).columns
# basf[a].astype(str).astype(float)
# basf.iloc[basf.dtypes==object]

####converting the data to numeric ####
basf=basf.apply(pd.to_numeric, errors='coerce')

####renaming the columns ######
basf.rename(columns={0:'signalid',1:'t',2:'sf'},inplace=True)

###renaming the last column
basf.columns.values[-1]='q'

####creating a empty dictionary #####
mapp={}

#####creating the empty list ###
indices=[]
j=0

#####for renaming the columns updating the empty dictionary #####
for i in range(3,(len(basf.columns)-1)):
    mapp.update({i:"V"+str(j)})
    indices.append(i)
    j+=1

###renaming all the columns at a time ####        
basf.rename(columns=mapp,inplace=True) 

####start of range value of window
windowstart=0

###start of range value of window
windowend=nwindows
resultant=[]
for row in range(0,len(basf),nwindows):
    ##Readingg data window by window  ###
    df=basf.iloc[windowstart:windowend,indices]
    # df = df.apply(pd.to_numeric, errors='coerce')
#    print(nwindows)
    ###averaging of the windows
    ag=pd.DataFrame(df.mean(axis=0)) 
    fft = ag
    # print(len(fft))
    N = len(fft)
    yf= (np.array(fft[0:N]))
    #xf = np.linspace(0.0, 1.0 / (2.0 * T), N)
    xf = np.linspace(0.0, 1.0 / (2.0 * T), N)
    #plt.plot(xf,yf)
    #plt.show()
    # rpmtuple = (Rpm2nd_version(yf,xf,200, 1370,0.4))
    # rpmis = rpmtuple[0]
    # rpms.append(int(rpmis))

    rpmtupl1st = fun.rpm1st_version(yf,xf,1600,1626) ##rpm calculations
    shaftspeed=rpmtupl1st
    #print(shaftspeed)
    ####frequencies which are above the 
    r1,r2,r3,r4=fun.BCF(NB,BD,PD,angle,shaftspeed)
    limitvalue=float(0.1)
    a1,a2=fun.faultrange(r1,limitvalue)
    #print(int(a1),int(a2))
    a1=int(a1)
    a2=int(a2)
    a3,a4=fun.faultrange(r2,limitvalue)
    #print(int(a3),int(a4))
    a3=int(a3)
    a4=int(a4)
    a5,a6=fun.faultrange(r3,limitvalue)
    #print(int(a5),int(a6))
    a5=int(a5)
    a6=int(a6)
    a7,a8=fun.faultrange(r4,limitvalue)
    a7=int(a7)
    a8=int(a8)
    #print(int(a2),int(a1),int(a4),int(a3),int(a6),int(a5),int(a8),int(a7))

    freqs=fun.fftcalculations(ag,samplingFrequency, windowsize) 
    #print("freqn is",freqs)
    #list1.append(freqs)
    freqs1=freqs.to_list()
    #print(freqs1)
    
    result=fun.FTF(freqs1,a2,a1)
    #print(result)
    result1=fun.BSF(freqs1,a4,a3)
    #print(result) 
    result2=fun.OUTERRACE(freqs1,a6,a5)
    #print(result2)
    result3=fun.INNERRACE(freqs1,a8,a7)
    #print(result3)
    resultant.append(result)
    resultant.append(result1)
    resultant.append(result2)
    resultant.append(result3)
    print(resultant)
    if "no ftf fault" in resultant:
        if "no bsf fault" in resultant:
            if "no outerrace fault" in resultant:
                if "no innerrace fault" in resultant:
                    print("bearing is healthy")
    resultant.clear()
    freqs1.clear()
    
    windowstart=windowstart+nwindows
    windowend=windowend+nwindows
    #print(row)








