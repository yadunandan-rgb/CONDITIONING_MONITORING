###libraries ####
import pandas as pd
import numpy as np
import math
from configparser import ConfigParser
import os
import matplotlib.pyplot as plt
import bearingplotmark2fubc as fun
list1=[]
###input parameters ###
config_object = ConfigParser()
config_object.read(r'/home/vegam/bearinglatest2/nasa.ini')

####calling the userinfo object.
userinfo = config_object["user_info"]

#Number of Rolling Element or Ball
NB=int(userinfo["NB"])

#Rolling Element or Ball Diameter 
BD=float(userinfo["BD"]) 

#pitch circle diameter of the bearing
PD=float(userinfo["PD"]) 

#Contact Angle
angle=float(userinfo["angle"]) 

#rpm 
#RPM=float(userinfo["RPM"])
#Shaft Rotational Speed
#shaftspeed=RPM/60 

###percentage of characteristic frequency Range allowance
CFrange_allowance=10

###percentage of fault frequency Range allowance
faultFreqallowance=10

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

####the value after the percentage of characteristic frequency Range allowance
afterallowance=(100-CFrange_allowance)/100

###value after adding the percentage of fault frequency Range allowance
afterfaultfreqallowanceplus=(100+faultFreqallowance)/100

###value after substracting the percentage of fault frequency Range allowance
afterfaultfreqallowanceminus=(100-faultFreqallowance)/100
def Enquiry(lis1): 
    if not lis1: 
        return 1
    else: 
        return 0


###calculating bearing characteristic frequencies
####input data #############
basf=pd.read_csv(r'/home/vegam/bearinglatest2/nasafft/nasa1healthy.csv',skiprows=1,header=None)
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
resultant1=[]
resultant2=[]
resultant3=[]
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
    rpmtupl1st = fun.rpm1st_version(yf,xf,2400,2000) ##rpm calculations
    shaftspeed=rpmtupl1st
    #print(shaftspeed)
    ####frequencies which are above the rms
    r1,r2,r3,r4=fun.BCF(NB,BD,PD,angle,shaftspeed) #fbio
    limitvalue=float(0.3)
    a1,a2=fun.faultrange(r1,limitvalue)#ftf
    #print(int(a1),int(a2))
    a1=int(a1)
    a2=int(a2)
    a3,a4=fun.faultrange(r2,limitvalue)#bsf
    #print(int(a3),int(a4))
    a3=int(a3)
    a4=int(a4)
    a5,a6=fun.faultrange(r3,limitvalue)#outerrace
    #print(int(a5),int(a6))
    a5=int(a5)
    a6=int(a6)
    a7,a8=fun.faultrange(r4,limitvalue)#innerrace
    a7=int(a7)
    a8=int(a8)
    print(int(a2),int(a1),int(a4),int(a3),int(a6),int(a5),int(a8),int(a7))
    print(int(2*a2),int(2*a1),int(2*a4),int(2*a3),int(2*a6),int(2*a5),int(2*a8),int(2*a7))
    print(int(3*a2),int(3*a1),int(3*a4),int(3*a3),int(3*a6),int(3*a5),int(3*a8),int(3*a7))

    amp,frqn,rms=fun.fftcalculations(output,xf,samplingFrequency, windowsize) 
    #print("freqn is",freqs)
    reemovNestings(amp) 
    plot1=fun.plotmark(xf,yf,frqn,a2,a1,a4,a3,a6,a5,a8,a7,frqn)
    #plt.show()      
    plot2=fun.plotmark(xf,yf,frqn,2*a2,2*a1,2*a4,2*a3,2*a6,2*a5,2*a8,2*a7,frqn)          
    plot3=fun.plotmark(xf,yf,frqn,3*a2,3*a1,3*a4,3*a3,3*a6,3*a5,3*a8,3*a7,frqn)          
    
    
    #print("freqn is",freqs)
    rms2=2*rms
    rms3=3*rms
    
    plot1.hlines(y=3*rms, color='r',linewidth=3,xmin=0,xmax=1200)
    plot2.hlines(y=3*rms, color='b',linewidth=3,xmin=0,xmax=1200)
    plot3.hlines(y=3*rms, color='g',linewidth=3,xmin=0,xmax=1200)
    
    plt.show()

    f1=fun.FTF(frqn,a2,a1)
    print(f1)
    b1=fun.BSF(frqn,a4,a3)
    print(b1) 
    
    #print(result2)
    i1=fun.INNERRACE(frqn,a8,a7)
    print(i1)
    o1=fun.OUTERRACE(frqn,a6,a5)
    #freqs1.clear()
    print(o1)
    if Enquiry(f1):
        if Enquiry(b1):
            if Enquiry(i1):
                if Enquiry(o1):
                    print ("bearing is healthy") 
                  
    frqn.clear()
    output.clear()
    windowstart=windowstart+nwindows
    windowend=windowend+nwindows
    #print(row)








