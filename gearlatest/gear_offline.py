from configparser import ConfigParser
import pandas as pd
import os
#os.chdir("E:/vegam_data/code")####changing wworking directory
import gearcalculation as gear
import scipy.fftpack as syfp
from scipy import signal
from scipy.fftpack import fft, ifft, rfft
import matplotlib.pyplot as plt
import pandas as pd
import os
from scipy.signal import find_peaks_cwt
import csv
import heapq
import timeit
import collections
import time


config_object = ConfigParser()
config_object.read(r'/home/vegam/sortedfolder/gear_analysisversion2/geardatawthcode_version2/gearboxinput.ini')
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

#Speed_of_pinion =int(gear_info["speed_of_pinion"])
No_of_teeth_pinion=int(gear_info["number_of_teeth_pinion"])
No_of_teeth_gear=int(gear_info["number_of_teeth_gear"])
Sampling_freqn=int(sensor_info["sampling_freqn"])

power=int(userinfo2["p"])
no_samples = 4096
window_size = 512
CFrange_allowance=20 ###percentage of characteristic frequency Range allowance
faultFreqallowance=10 ###percentage of fault frequency Range allowance
#frequency_of_pinion=float(gear_info["frequency_of_pinion"])
nwindows=int(no_samples/window_size)
#df = pd.read_csv(r'/home/vegam/sortedfolder/gear_analysisversion2/geardatawthcode_version2/ChartData_Excel_24091113203725.csv')
#df1 =df['Value']

maximum_rpm_hz = 1500/60

afterallowance=(100-CFrange_allowance)/100
afterfaultfreqallowanceplus=(100+faultFreqallowance)/100
afterfaultfreqallowanceminus=(100-faultFreqallowance)/100


###################
basf=pd.read_csv(r'/home/vegam/sortedfolder/gear_analysisversion2/geardatawthcode_version2/11_05To_11_06.csv',skiprows=1,header=None)
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
    ag=df.mean(axis=0)
    print(ag)
    
    freqs=gear.fftcalculations(ag,Sampling_freqn, window_size)
    #print(freqs)
    Speed_of_pinion=gear.Rpm2nd_version(ag,Sampling_freqn, 1500,0.6)
    #print(Speed_of_pinion)
    speed_of_pinion1 = Speed_of_pinion[0]
    frequency_of_pinion=float(speed_of_pinion1)
    print(frequency_of_pinion)
    GMFF=float(frequency_of_pinion*No_of_teeth_pinion)##355
    #print(GMFF)
    #GMFF2=float(2*GMFF)
    #GMFF3=float(3*GMFF)
    T = float(1 / Sampling_freqn)
    gear_ratio=float(No_of_teeth_pinion/No_of_teeth_gear)
    #print(gear_ratio)
    GEAR_FREQUENCY=float(frequency_of_pinion*gear_ratio)
    #print(GEAR_FREQUENCY)
    GEAR_GMFF=float(GEAR_FREQUENCY*No_of_teeth_gear)
    
    #Frequency_of_pinion =gear.frequency_of_pinion(r1)
    #Speed_of_pinion=gear.Rpm2nd_version(freqs,Sampling_freqn, 1500,0.6)

    gmff=gear.GMFF(No_of_teeth_pinion,frequency_of_pinion,Sampling_freqn, freqs,afterallowance,afterfaultfreqallowanceminus,afterfaultfreqallowanceplus)
    if len(gmff) > 0:
        print("strong_indication_for gear fault")
    else:
        print("no fault")
    windowstart=windowstart+nwindows
    windowend=windowend+nwindows
    #print(row)
 
