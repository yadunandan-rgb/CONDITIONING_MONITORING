#### libraries ###############
import math 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.patches as patches
output=[]
#####to calculate bearing characteristic frequency #####
##BCF=bearing characteristic frequency
###NB=number of balls or rollers ,BD=ball or roller diameter 
###PD=Pitch Diameter 
##FTF=fundamental train frequency, BPFI=Ball Pass Frequency of Inner Race
##BPFO=Ball Pass Frequency of OuterRace , BSF=Ball Spin Frequency
def rpm1st_version(preferHorizont_fft_y,preferHorizont_fft_x,sampling_frequency, Max_rpm):
    maximum_rpm_hz = Max_rpm/60
    fft_ = preferHorizont_fft_y
    no_of_samples = len(fft_)
    sampling_frequency = sampling_frequency
    time_period = 1/sampling_frequency

    fft_y_axes=preferHorizont_fft_y
    fft_x_axes = preferHorizont_fft_x

    fft_x_axes_list = list(fft_x_axes)

    amplitudesindex = [list(fft_y_axes).index(i) for i in fft_y_axes]
    amplitudesvalues = [float(i) for i in fft_y_axes]
    frequency = [fft_x_axes_list[i] for i in amplitudesindex ]#if i<=maximum_rpm
    indexfreqencylesthanrpm = [frequency.index(i) for i in frequency if i<=maximum_rpm_hz]
    indexfreqencylesthanrpmvalues = [frequency[i] for i in indexfreqencylesthanrpm ] #if i<=maximum_rpm
    amplitudesofrpm = [amplitudesvalues[i] for i in indexfreqencylesthanrpm]
    maxoneamplitude = max(amplitudesofrpm)
    indexofrpmamplitude = amplitudesvalues.index(maxoneamplitude)
    freuencycorrestomaxampl = indexfreqencylesthanrpmvalues[indexofrpmamplitude]
    return freuencycorrestomaxampl

def BCF(NB,BD,PD,angle,shaftspeed):
    Fcir=((1/2)*(1-(BD/PD)*math.cos(angle)))
    FTF=Fcir*shaftspeed #fundamental train frequency
    FTFFinal=float(FTF) 
    
    print(FTFFinal)
    
    Bfir=((NB/2)*(1+(BD/PD)*math.cos(angle)))
    BPFI=Bfir*shaftspeed #ball pass frequency of inner race
    BPFIFinal=float(BPFI)
    #(FTFFinal)
    
    print(BPFIFinal) 
    
    Bfor=((NB/2)*(1-(BD/PD)*math.cos(angle)))
    BPFO=Bfor*shaftspeed #ball pass frequency  of outer race
    BPFOFinal=float(BPFO)
    
    
    print(BPFOFinal) 
    
    Bsf=((PD/(2*BD))*(1-((BD/PD)*(math.cos(angle)))**2))
    BSF=Bsf*shaftspeed #ball spin frequency
    BSFFinal=float(BSF)
    print(BSFFinal) 

    #return BPFIFinal
    return  FTFFinal, BSFFinal, BPFOFinal, BPFIFinal
def faultrange(inputvalue,lim):
    rangelimit=inputvalue*lim      #67*0.2=13.4
    Finalrange1=float(inputvalue+rangelimit) #67+13.14=76
    Finalrange2=float(inputvalue-rangelimit) #67-13.4=56
    return Finalrange1,Finalrange2
    
    
    
    
####calculating BCF taking fault frequency ranges and shaft speed as input
# Vibration Frequency Fundamental Train:=FT
##Vibration Frequency Inner Ring Defect: VFIR
#Vibration Frequency Outer Ring Defect:  VFOR
#Vibration Frequency Roller Spin: VFRS  
#shaft speed in RPM
def my_function(x):
    return list(dict.fromkeys(x))    
def bcffromfaultfreqRange(FT, VFRS,VFOR, VFIR, shaftspeed):
    FundamentalTrain =FT*shaftspeed
    InnerRingDefect = VFIR*shaftspeed
    OuterRingDefect = VFOR*shaftspeed
    RollerSpin = VFRS*shaftspeed
    return FundamentalTrain,RollerSpin, OuterRingDefect, InnerRingDefect 
    
####on passing averaged fft values ,getting corresponding frequencies of amplitudes which are above the RMS value.
##fftavg=averaged fft values ####samplingFrequency of the sensor ###window size of the data.

def fftcalculations(fftavg,freqns,samplingFrequency,windowsize):
    lst1=fftavg  ####fftavg should be in pandas.core.series.Series
    rms =np.sqrt(np.mean(np.square(lst1)))
    Amplitude_rms_index = [list(lst1).index(i) for i in lst1 if i>3*rms]
    #print(Amplitude_rms_index)
    HorizontAmplitudAbove_rms_values = [i for i in lst1 if i>3*rms]
    #print(HorizontAmplitudAbove_rms_values)
    corres_frequency = [list(freqns)[i] for i in Amplitude_rms_index]
    print(corres_frequency)
    return HorizontAmplitudAbove_rms_values,corres_frequency,rms
##R1=bcf of FTF, R2=BCF of BSF ,samplingFrequency,
##lst=frequencies after 


resultant=[]
resultant1=[] 
resultant2=[]
resultant3=[]  

def FTF(input1,faultrange1,faultrange2):
    global result
    for x in input1: 
        
        if x>= faultrange1 and x<= faultrange2:
            result= "first harmonic FTF fault"
            print("first ftf")
            resultant.append(result)
        if x>= 2*faultrange1 and x<= 2*faultrange2:
            result="2nd harmonic ftf fault"
            print("2nd ftf")
            resultant.append(result)

        if x>= 3*faultrange1 and x<= 3*faultrange2:
            result="3rd harmonic FTF fault"
            print("3rd ftf")
            resultant.append(result)

    return resultant   
                   
                    
def BSF(input1,faultrange1,faultrange2):
    global result
    
    for x in input1:
        if x>= faultrange1 and x<= faultrange2:
            result= "first harmonic bsf fault"
            print("first bsf")
            resultant1.append(result)

        if x>= 2*faultrange1 and x<= 2*faultrange2:
            result="2nd harmonic bsf fault"
            
            print("2nd bsf")
            resultant1.append(result)

            #return (result)
        if x>= 3*faultrange1 and x<= 3*faultrange2:
            result="3rd harmonic bsf fault"
            print("3rd bsf")
            resultant1.append(result)
    return resultant1   

def OUTERRACE(input1,faultrange1,faultrange2):
    global result
    for x in input1:
        if x>= faultrange1 and x<= faultrange2:
            result= "first harmonic outerrace fault"
            print("first outerrace")
            resultant2.append(result)

        if x>= 2*faultrange1 and x<= 2*faultrange2:
            result="2nd harmonic outerrace fault"
            print("2nd outerrace")
            resultant2.append(result)

        if x>= 3*faultrange1 and x<= 3*faultrange2:
            result="3rd harmonic outerrace fault"
            print("3rd outerrace")
            resultant2.append(result)
    return resultant2   

                           
def INNERRACE(input1,faultrange1,faultrange2):
    global result
    for x in input1:
        if x>= faultrange1 and x<= faultrange2:
            result= "first harmonic innerrace fault"
            print("first innerrace")
            resultant3.append(result)

        if x>= 2*faultrange1 and x<= 2*faultrange2:
            result="2nd harmonic innerrace fault"
            print("2nd innerrace")
            resultant3.append(result)

        if x>= 3*faultrange1 and x<= 3*faultrange2:
            result="3rd harmonic innerrace fault"
            print("3rd innerrace")
            resultant3.append(result)
    return resultant3   

               