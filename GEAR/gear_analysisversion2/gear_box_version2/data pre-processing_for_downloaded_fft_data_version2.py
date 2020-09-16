###libraries ####
import pandas as pd
import numpy as np
import math
from configparser import ConfigParser
import os
import paho.mqtt.client as mqtt

os.chdir("U:/vegam_data/code")####changing wworking directory
import Bearing_fault_Analysis_functions_version2 as fun
#from configparser import ConfigParser
###input parameters ###
config_object = ConfigParser()
config_object.read("U:/vegam_data/configuration_files/userinfo6.ini")
userinfo = config_object["user_info"]
NB=int(userinfo["NB"]) #Number of Rolling Element or Ball
BD=int(userinfo["BD"]) #Rolling Element or Ball Diameter
PD=int(userinfo["PD"]) #pitch circle diameter of the bearing
angle=int(userinfo["angle"]) #Contact Angle
RPM=float(userinfo["RPM"])#rpm 
shaftspeed=RPM/60 #Shaft Rotational Speed
#config_object.read("userinfo2.ini")
#userinfo2= config_object["user_info2"]
#serverinfo= config_object["server_config"]
Broker_address=userinfo["broker_address"]
Broker_port=int(userinfo["broker_port"])
CFrange_allowance=20 ###percentage of characteristic frequency Range allowance
faultFreqallowance=10 ###percentage of fault frequency Range allowance

###sensor details 
samplingFrequency=1600
nsamp=4096
windowsize=512
nwindows=int(nsamp/windowsize)

afterallowance=(100-CFrange_allowance)/100
afterfaultfreqallowanceplus=(100+faultFreqallowance)/100
afterfaultfreqallowanceminus=(100-faultFreqallowance)/100

###calculating bearing characteristic frequencies
r1,r2,r3,r4=fun.BCF(NB,BD,PD,angle,shaftspeed)
####input data #############
basf=pd.read_csv("U:/Vegam_resource/K_Means/DataExtractor/tagExportData3.csv",skiprows=1,header=None)
########################
basf.replace(regex=True, inplace=True, to_replace=r'[^0-9.E-]', value=r'')
# a=basf.select_dtypes(object).columns
# basf[a].astype(str).astype(float)
# basf.iloc[basf.dtypes==object]
basf=basf.apply(pd.to_numeric, errors='coerce')
basf.rename(columns={0:'signalid',1:'t',2:'sf'},inplace=True)
basf.columns.values[-1]='q'
mapp={}
indices=[]
j=0
for i in range(3,(len(basf.columns)-1)):
    mapp.update({i:"V"+str(j)})
    indices.append(i)
    j+=1
basf.rename(columns=mapp,inplace=True)  ###renaming all the columns
windowstart=0
windowend=nwindows
for row in range(0,len(basf),nwindows):
    df=basf.iloc[windowstart:windowend,indices]
    # df = df.apply(pd.to_numeric, errors='coerce')
    #print(nwindows)
    ag=df.mean()###averaging of the windows 
    freqs=fun.fftcalculations(ag,samplingFrequency, windowsize) ####frequencies which are above the RMS
    ftf=fun.FTF(r1,r2,samplingFrequency,freqs,afterallowance,afterfaultfreqallowanceminus,afterfaultfreqallowanceplus)
    if len(ftf) > 0:
        #####publishing the output
        #print('strong_indication_for train frequency fault')
        client.publish("A456765467/fault_result",4)
    bsf=fun.BSF(r2,r3,samplingFrequency,freqs,afterallowance,afterfaultfreqallowanceminus,afterfaultfreqallowanceplus)
    if len(bsf) > 0:
        #####publishing the output
        #("strong evidence for spin frequency fault")
        client.publish("A456765467/fault_result",3)
    bpfo=fun.BPFO(r3,r4,samplingFrequency,freqs,afterallowance,afterfaultfreqallowanceminus,afterfaultfreqallowanceplus)
    if len(bpfo) > 0:
        #####publishing the output
        #print("strong evidence for outerrace fault")
        client.publish("A456765467/fault_result",2)
    bpfi=fun.BPFI(r4,samplingFrequency,freqs,afterallowance,afterfaultfreqallowanceminus,afterfaultfreqallowanceplus)
    if len(bpfi) > 0:
        #print("strong evidence for innerarce fault")
        client.publish("A456765467/fault_result",1)
    #print(windowstart)
    #print(windowend)
    windowstart=windowstart+nwindows
    windowend=windowend+nwindows
    #print(row)









