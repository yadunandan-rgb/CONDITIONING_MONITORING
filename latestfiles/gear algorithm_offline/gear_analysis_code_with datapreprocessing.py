# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 12:55:49 2020

@author: User
"""

###libraries ####
import pandas as pd
import numpy as np
import math
from configparser import ConfigParser
import os
import matplotlib.pyplot as plt
#import Bearing_analysis_function_8 as fun
list1=[]
###input parameters ###

os.chdir("D:/gearlatesttesting")####changing wworking directory
import gear_calc3 as gear

config_object = ConfigParser()
config_object.read(r'D:/gearlatesttesting/gearboxinput.ini')
userinfo2= config_object["user_info2"]
serverinfo= config_object["server_config"]
sensor_info=config_object["sensor_config"]
gear_info=config_object["gear_config"]
Broker_address=serverinfo["broker_address"]

# Aunthentication jsw
# Username=sensor_info["user_name"]
# Password=sensor_info["password"]

Broker_port=int(serverinfo["broker_port"])
Sensor_id=sensor_info["sensor_id"]
Tag_name=sensor_info["tag_name"]

Speed_of_pinion =int(gear_info["speed_of_pinion"])
No_of_teeth_pinion=int(gear_info["number_of_teeth_pinion"])
No_of_teeth_gear=int(gear_info["number_of_teeth_gear"])
Sampling_freqn=int(sensor_info["sampling_freqn"])


###sensor details 
samplingFrequency=2400

##number of samples
nsamp=4096
resultant=[]

###window size 
windowsize=512
T=1/samplingFrequency
###number of windows per burst
nwindows=int(nsamp/windowsize)

###calculating bearing characteristic frequencies
####input data #############
basf=pd.read_csv(r'D:/gearlatesttesting/expirement/badffftparser.csv',skiprows=1,header=None)
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
output = [] 
product_list2=[]
product_list3=[]

for row in range(0,len(basf),nwindows):
    ##Readingg data window by window  ###
    df=basf.iloc[windowstart:windowend,indices]
    # df = df.apply(pd.to_numeric, errors='coerce')
#    print(nwindows)
    ###averaging of the windows
    ag=pd.DataFrame(df.mean(axis=0)) 
    fft = ag
    #print(fft)
    # print(len(fft))
    #N = len(fft)
    yf=(np.array(fft[0:len(fft)]))
    #print(yf)
    xf = np.linspace(0.0, 1.0 / (2.0 * (1/samplingFrequency)), len(fft))
    product_list2.append(xf)
    def reemovNestings(l): 
        for i in l: 
            if type(i) == list: 
                reemovNestings(i) 
            else:
                output.append(i) 
   
     
    reemovNestings(yf) 
    rpmtupl1st = gear.rpm1st_version(output,xf,2400,2000) ##rpm calculations
    frequency_of_pinion=rpmtupl1st
    #print(shaftspeed)
    ####frequencies which are above the rms
    gmff=gear.gear_calculation(No_of_teeth_pinion,frequency_of_pinion) 
    limitvalue=float(0.3)
    a1,a2=gear.faultrange(gmff,limitvalue)
    #print(int(a1),int(a2))
    a1=int(a1)
    a2=int(a2)
    """a3,a4=gear.faultrange(gmff2,limitvalue)
    #print(int(a3),int(a4))
    a3=int(a3)
    a4=int(a4)
    a5,a6=gear.faultrange(gmff3,limitvalue)
    #print(int(a5),int(a6))
    a5=int(a5)
    a6=int(a6)"""
    
    print(int(a2),int(a1))
    print(int(2*a2),int(2*a1))
    print(int(3*a2),int(3*a1))

    amp,frqn,rms=gear.fftcalculations(output,xf,samplingFrequency, windowsize) 
    #print("freqn is",freqs)
    reemovNestings(amp) 

    f1=gear.GMFF_ANALYSIS(frqn,a2,a1)
    #print(f1)
    
    if len(f1)==0:
        print ("gear is healthy") 
    else:
        print ("gear has some faults") 


    f1.clear()              
    frqn.clear()
    output.clear()

    #freqs1.clear()
    windowstart=windowstart+nwindows
    windowend=windowend+nwindows
    #print(row)








