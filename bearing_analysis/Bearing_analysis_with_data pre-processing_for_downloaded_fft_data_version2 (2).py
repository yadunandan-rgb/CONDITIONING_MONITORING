###libraries ####
import pandas as pd
import numpy as np
import math
from configparser import ConfigParser
import os

####changing wworking directory

import Bearing_fault_Analysis_functions_version2 as fun

###input parameters ###
config_object = ConfigParser()
config_object.read(r'/home/vegam/bearinglatest/userinfo6.ini')

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
CFrange_allowance=20

###percentage of fault frequency Range allowance
faultFreqallowance=10

###sensor details 
samplingFrequency=1600

##number of samples
nsamp=4096

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
basf=pd.read_csv(r'/home/vegam/bearinglatest/bearingtesting/data/InnerRace_Fault.csv',skiprows=1,header=None)
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
    
    # rpmtuple = (Rpm2nd_version(yf,xf,200, 1370,0.4))
    # rpmis = rpmtuple[0]
    # rpms.append(int(rpmis))

    rpmtupl1st = fun.rpm1st_version(yf,xf,1600,1710) ##rpm calculations
    shaftspeed=rpmtupl1st
    print(shaftspeed)
    ####frequencies which are above the 
    r1,r2,r3,r4=fun.BCF(NB,BD,PD,angle,shaftspeed)

    freqs=fun.fftcalculations(ag,samplingFrequency, windowsize)
    
    ####here you call the RPM algorithm
    ####call the bearing characteristic frequency function 
    
    ####frequencies belongs to fundamental train frequency. 
    ftf=fun.FTF(r1,r2,samplingFrequency,freqs,afterallowance,afterfaultfreqallowanceminus,afterfaultfreqallowanceplus)
    if len(ftf) > 0:
        #####publishing the output
        print('strong_indication_for train frequency fault')
    
    ####frequencies belongs to ball spin frequency. 
    bsf=fun.BSF(r2,r3,samplingFrequency,freqs,afterallowance,afterfaultfreqallowanceminus,afterfaultfreqallowanceplus)
    if len(bsf) > 0:
        #####publishing the output
        print("strong evidence for spin frequency fault")

    ####frequencies belongs to ball pass outer race frequency.         
    bpfo=fun.BPFO(r3,r4,samplingFrequency,freqs,afterallowance,afterfaultfreqallowanceminus,afterfaultfreqallowanceplus)
    if len(bpfo) > 0:
        #####publishing the output
        print("strong evidence for outerrace fault")
    
    ####frequencies belongs to ball pass inner race frequency. 
    bpfi=fun.BPFI(r4,samplingFrequency,freqs,afterallowance,afterfaultfreqallowanceminus,afterfaultfreqallowanceplus)
    if len(bpfi) > 0:
        print("strong evidence for innerarce fault")
         
    if sum([len(ftf),len(bsf),len(bpfo),len(bpfi)]) == 0:
        print("bearing is healthy")
        
    # print(windowstart)
    # print(windowend)
    windowstart=windowstart+nwindows
    windowend=windowend+nwindows
    #print(row)








