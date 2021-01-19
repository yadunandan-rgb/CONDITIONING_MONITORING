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
    rangelimit=inputvalue*lim
    Finalrange1=float(inputvalue+rangelimit)
    Finalrange2=float(inputvalue-rangelimit)
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
    print(HorizontAmplitudAbove_rms_values)
    corres_frequency = [list(freqns)[i] for i in Amplitude_rms_index]
    print(corres_frequency)
    return HorizontAmplitudAbove_rms_values,corres_frequency,rms
##R1=bcf of FTF, R2=BCF of BSF ,samplingFrequency,
##lst=frequencies after 
def plotmark(x1,y1,freq,range1,range2,range3,range4,range5,range6,range7,range8,frens):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x1,y1)
    plt.xlabel('Frequency(Hz')
    plt.ylabel('FFT Values')           
    
    min_f0_0, max_f0_0 = range1,range2
    
    min_f0_1, max_f0_1 = range3,range4
    min_f0_2, max_f0_2= range5,range6
    min_f0_3, max_f0_3= range7,range8
    min_f1, max_f1 = min(y1), max(y1)
    width_0 = max_f0_0 - min_f0_0
    width_1 = max_f0_1 - min_f0_1
    width_2 = max_f0_2 - min_f0_2
    width_3 = max_f0_3 - min_f0_3
    height = max_f1 - min_f1
    #fres=frens[0]
    for element in range (len(freq)):
        ax.plot(freq[element],0,'vk')
    #ax.plot(frens1,0,'vk')
    #ax.plot(frens2,0,'vk')
    #ax.plot(frens3,0,'vk')

    # print(min_f0, max_f0, min_f1, max_f1, width, height)
       
    ax.add_patch(
                patches.Rectangle(
                xy=(min_f0_0, min_f1),  # point of origin.
                width=width_0,
                height=height,
                linewidth=1,
                color='red',
                 fill=False
                )
            )
    
    ax.add_patch(
                patches.Rectangle(
                xy=(min_f0_1, min_f1),  # point of origin.
                width=width_1,
                height=height,
                linewidth=1,
                color='blue',
                fill=False
                )
            )
    ax.add_patch(
                patches.Rectangle(
                xy=(min_f0_2, min_f1),  # point of origin.
                width=width_2,
                height=height,
                linewidth=1,
                color='green',
                fill=False
                )
            )
    
    ax.add_patch(
                patches.Rectangle(
                xy=(min_f0_3, min_f1),  # point of origin.
                width=width_3,
                height=height,
                linewidth=1,
                color='brown',
                fill=False
                )
            )
    
    
    
    return ax

resultant=[]
def FTF(input1,faultrange1,faultrange2):
    global result
    for element in input1:
        if element in range(faultrange1,faultrange2):
            result= "first harmonic FTF fault"
            return result
        
        elif element in range(2*faultrange1,2*faultrange1):
            
            result="2nd harmonic ftf fault"
            return result
        
        elif element in range(3*faultrange1,3*faultrange2):
            result="3rd harmonic FTF fault"
            return result
        else:
            result="no ftf fault"
            return result
            
def BSF(input1,faultrange1,faultrange2):
    global result
    for element in input1:
        if element in range(faultrange1,faultrange2):
            result= "first harmonic BSF fault"
            return result
        
        elif element in range(2*faultrange1,2*faultrange1):
            result="2nd harmonic BSF fault"
            return result
        
        elif element in range(3*faultrange1,3*faultrange2):
            result="3rd harmonic BSF fault"
            return result
        else:
            result="no bsf fault"
            return result


def OUTERRACE(input1,faultrange1,faultrange2):
    global result
    for element in input1:
        if element in range(faultrange1,faultrange2):
            result= "first harmonic outerrace fault"
            return result
        
        elif element in range(2*faultrange1,2*faultrange1):
            result="2nd harmonic outerrace fault"
            return result
        
        elif element in range(3*faultrange1,3*faultrange2):
            result="3rd harmonic outerrace fault"
            return result
        else:
            result="no outerrace fault"
            return result

            
    
            
def INNERRACE(input1,faultrange1,faultrange2):
    global result
    for element in input1:
        if element in range(faultrange1,faultrange2):
            result= "first harmonic innerrace fault"
            return result
        
        elif element in range(2*faultrange1,2*faultrange1):
            result="2nd harmonic innerrace fault"
            return result
       
        elif element in range(3*faultrange1,3*faultrange2):
            result="3rd harmonic innerrace fault"
            return result
        else:
             result="no innerrace fault"
             return result

            
            
    

        
        