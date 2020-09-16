import math 
import pandas as pd
import numpy as np
import paho.mqtt.client as mqtt
from configparser import ConfigParser
config_object = ConfigParser()
config_object.read("userinfo2.ini")
userinfo2= config_object["user_info2"]
serverinfo= config_object["server_config"]
Broker_address=serverinfo["broker_address"]
Broker_port=int(serverinfo["broker_port"])

client = mqtt.Client()
client.connect(Broker_address,Broker_port)
def BCF(NB,BD,PD,angle,shaftspeed):
    Fcir=((1/2)*(1-(BD/PD)*math.cos(angle)))
    FTF=Fcir*shaftspeed #fundamental train frequency
    FTFFinal=int(FTF)
    #print(FTFFinal)
    
    Bfir=((NB/2)*(1+(BD/PD)*math.cos(angle)))
    BPFI=Bfir*shaftspeed #ball pass frequency of inner race
    BPFIFinal=int(BPFI)
    #print(BPFIFinal) 
    
    Bfor=((NB/2)*(1-(BD/PD)*math.cos(angle)))
    BPFO=Bfor*shaftspeed #ball pass frequency  of outer race
    BPFOFinal=int(BPFO)
    #print(BPFOFinal) 
    
    Bsf=((PD/(2*BD))*(1-((BD/PD)*(math.cos(angle)))**2))
    BSF=Bsf*shaftspeed #ball spin frequency
    BSFFinal=int(BSF)
    #print(BSFFinal)       

    return  FTFFinal, BSFFinal, BPFOFinal, BPFIFinal

def fftcalculations(fftavg,samplingFrequency,windowsize):
    lst1=fftavg
    rms =np.sqrt(np.mean(np.square(lst1)))  #####rms of fft values
    count = len([i for i in lst1 if i > 1.2*rms]) ####count of values which are greater than 1.2 times the RMS
    ac=sorted([(x,i) for (i,x) in enumerate(lst1)], reverse=True )[:count]  ######correspondig frequency and amplitudes greater than 1.2xRMS 
    ad=pd.DataFrame(ac,columns=['amplitude','Frequency'])
    lst=ad['Frequency']*((samplingFrequency/2)/windowsize)
    freqs=lst.astype(int)
    return freqs


def FTF(R1,R2,samplingFrequency,lst,afterallowance,afterfaultfreqallowanceminus,afterfaultfreqallowanceplus):
    FTF=[i for i in lst if i in range(int(afterallowance*R1),int(afterallowance*R2))]
    ftfreq=[] #####fault train frequencies
    if len(FTF)>0:
        # print('first harmonics are present')
        for N in range(len(FTF)):
            # print('first harmonic is',FTF[N])
            tfshrs=int(2*afterfaultfreqallowanceminus*FTF[N]) ####train frequency second harmonic range start value
            tfshre=int(2*afterfaultfreqallowanceplus*FTF[N]) #####train frequency second harmonic range end value
            if tfshrs > int(0.5*samplingFrequency):
                #print("sampling frequency of the sensor is not enough for the analysis")
            else:
                change=[k for k in lst if k in range(tfshrs,tfshre)]
                if len(change)>0:
                    # print('second harmonic ranges are ',range(tfshrs,tfshre))
                    # print('second harmonic is present',change)
                    tftrs=int(3*afterfaultfreqallowanceminus*FTF[N]) ###spin frequency third harmonic range start value
                    tftre=int(3*afterfaultfreqallowanceplus*FTF[N]) ####spin frequency third harmonic range end value
                    if tftrs > int(0.5*samplingFrequency):
                        #print("sampling frequency of the sensor is not enough for the analysis")
                    else:
                        change1=[i for i in lst if i in range(tftrs,tftre)]
                        if len(change1)>0:
                            # print('third harmonic ranges are ',range(tftrs,tftre))
                            # print('third harmonic is present',change1)
                            # print('it is a strong evidence for train frequency fault')
                            client.publish("A456765467/fault_result",4)#PUBLISHES THE CAGE FAULT RESULT

                            ftfreq.append(FTF[N])
    return ftfreq
 
def BSF(R2,R3,samplingFrequency,lst,afterallowance,afterfaultfreqallowanceminus,afterfaultfreqallowanceplus):                          
    BSF=sorted([i for i in lst if i in range(int(afterallowance*R2),int(afterallowance*R3))])
    fsfreq=[] ###fault spin frequencies
    if len(BSF) > 0:
        # print('first harmonics are present')
        for M in range(len(BSF)):
            # print('first harmonic is',BSF[M])
            sfshrs=int(2*afterfaultfreqallowanceminus*BSF[M]) ####spin frequency second harmonic range start value
            sfshre=int(2*afterfaultfreqallowanceplus*BSF[M]) #####spin frequency second harmonic range end value
            if sfshrs > int(0.5*samplingFrequency):
                #print("sampling frequency of the sensor is not enough for the analysis")
            else:
                change=[k for k in lst if k in range(sfshrs,sfshre)]
                if len(change)>0:
                    # print('second harmonic ranges are ',range(sfshrs,sfshre))
                    # print('second harmonic is present',change)
                    sftrs=int(3*afterfaultfreqallowanceminus*BSF[M]) ###spin frequency third harmonic range start value
                    sftre=int(3*afterfaultfreqallowanceplus*BSF[M]) ####spin frequency third harmonic range end value
                    if sftrs > int(0.5*samplingFrequency):
                        #print("sampling frequency of the sensor is not enough for the analysis")
                    else:
                        change1=[i for i in lst if i in range(sftrs,sftre)]
                        if len(change1)>0:
                            # print('third harmonic ranges are ',range(sftrs,sftre))
                            # print('third harmonic is present',change1)
                            # print('it is a strong evidence for ball spin frequency')
                            client.publish("A456765467/fault_result",3)#PUBLISHES THE BALL/ROLLER FAULT RESULT
                            fsfreq.append(BSF[M])
    return fsfreq

def BPFO(R3,R4,samplingFrequency,lst,afterallowance,afterfaultfreqallowanceminus,afterfaultfreqallowanceplus):
    BPFO=[i for i in lst if i in range(int(afterallowance*R3),int(afterallowance*R4))]
    offreq=[] ###outer race fault frequencies
    if len(BPFO) > 0:
        # print('first harmonics are present')
        for j in range(len(BPFO)):
            # print('first harmonic is',BPFO[j])
            oshrs=int(2*afterfaultfreqallowanceminus*BPFO[j]) ####outer race second harmonic range start value
            oshre=int(2*afterfaultfreqallowanceplus*BPFO[j]) #####outer race second harmonic range end value
            if oshrs > int(0.5*samplingFrequency):
                #print("sampling frequency of the sensor is not enough for the analysis")
            else:
                change=[k for k in lst if k in range(oshrs,oshre)]
                if len(change)>0:
                    # print('second harmonic ranges are ',range(oshrs,oshre))                 
                    # print('second harmonic is present',change)
                    otrs=int(3*afterfaultfreqallowanceminus*BPFO[j]) ###outer race third harmonic range start value
                    otre=int(3*afterfaultfreqallowanceplus*BPFO[j]) #### outer race third harmonic range end value
                    if otrs > int(0.5*samplingFrequency):
                        #print("sampling frequency of the sensor is not enough for the analysis")
                    else:
                        change1=[i for i in lst if i in range(otrs,otre)]
                        if len(change1)>0:
                            # print('third harmonic ranges are ',range(otrs,otre))
                            # print('third harmonic is present',change1)
                            # print('it is a strong evidence for outerrace')
                            client.publish("A456765467/fault_result",2)#PUBLISHES THE OUTERRACE FAULT RESULT
                            offreq.append(BPFO[j])
    return offreq

def BPFI(R4,samplingFrequency,lst,afterallowance,afterfaultfreqallowanceminus,afterfaultfreqallowanceplus):               
    BPFI=sorted([i for i in lst if i>int(afterallowance*R4)])
    iffreq=[] ##inner race fault frequencies
    if len(BPFI)>0:
        # print('first harmonics are present')
        for i in range(len(BPFI)):
            # print('first harmonic is',BPFI[i])
            ishrs=int(2*afterfaultfreqallowanceminus*BPFI[i]) ####inner race second harmonic range start value
            ishre=int(2*afterfaultfreqallowanceplus*BPFI[i]) #####inner race second harmonic range end value
            if ishrs > int(0.5*samplingFrequency):
                #print("sampling frequency of the sensor is not enough for the analysis")
            else:
                change=[i for i in lst if i in range(ishrs,ishre)]
                if len(change)>0:
                    # print('second harmonic ranges are ',range(ishrs,ishre))
                    # print('second harmonic is present',change)
                    itrs=int(3*afterfaultfreqallowanceminus*BPFI[i]) ###inner race third harmonic range start value
                    itre=int(3*afterfaultfreqallowanceplus*BPFI[i]) #### inner race third harmonic range end value
                    if itrs > int(0.5*samplingFrequency):
                        #print("sampling frequency of the sensor is not enough for the analysis")
                    else:
                        change1=[i for i in lst if i in range(itrs,itre)]
                        if len(change1)>0:
                            # print('third harmonic ranges are ',range(itrs,itre))
                            # print('third harmonic is present',change1)
                            # print('it is a strong evidence for innerrace')
                            client.publish("A456765467/fault_result",1)#PUBLISHES THE INNERRACE FAULT RESULT
                            iffreq.append(BPFI[i])
    return iffreq




