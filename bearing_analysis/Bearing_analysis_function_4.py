#### libraries ###############
import math 
import pandas as pd
import numpy as np

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
    
    #print(FTFFinal)
    
    Bfir=((NB/2)*(1+(BD/PD)*math.cos(angle)))
    BPFI=Bfir*shaftspeed #ball pass frequency of inner race
    BPFIFinal=float(BPFI)
    #(FTFFinal)
    
    #print(BPFIFinal) 
    
    Bfor=((NB/2)*(1-(BD/PD)*math.cos(angle)))
    BPFO=Bfor*shaftspeed #ball pass frequency  of outer race
    BPFOFinal=float(BPFO)
    BPFOFinalrangelimit=BPFOFinal*0.2
    BPFOFinalrange1=BPFOFinal+BPFOFinalrangelimit
    BPFOFinalrange2=BPFOFinal-BPFOFinalrangelimit
    
    #print(BPFOFinal) 
    
    Bsf=((PD/(2*BD))*(1-((BD/PD)*(math.cos(angle)))**2))
    BSF=Bsf*shaftspeed #ball spin frequency
    BSFFinal=float(BSF)
    BSFFinalrangelimit=BSFFinal*0.2
    BSFFinalrange1=BSFFinal+BSFFinalrangelimit
    BSFFinalrange2=BSFFinal-BSFFinalrangelimit
    
    #print(BSFFinal
        
    #return BPFIFinal
    return  FTFFinal, BSFFinal, BPFOFinal, BPFIFinal
def faultrange(FTFFinal,BSFFinal,BPFOFinal,BPFIFinal):
    FTFFinalrangelimit=FTFFinal*0.2
    FTFFinalrange1=float(FTFFinal+FTFFinalrangelimit)
    FTFFinalrange2=float(FTFFinal-FTFFinalrangelimit)
    
    BPFIFinalrangelimit=BPFIFinal*0.2
    BPFIFinalrange1=float(BPFIFinal+BPFIFinalrangelimit)
    BPFIFinalrange2=float(BPFIFinal-BPFIFinalrangelimit)
    
    BPFOFinalrangelimit=BPFOFinal*0.2
    BPFOFinalrange1=float(BPFOFinal+BPFOFinalrangelimit)
    BPFOFinalrange2=float(BPFOFinal-BPFOFinalrangelimit)
    
    BSFFinalrangelimit=BSFFinal*0.2
    BSFFinalrange1=float(BSFFinal+BSFFinalrangelimit)
    BSFFinalrange2=float(BSFFinal-BSFFinalrangelimit)
    
    return FTFFinalrange1,FTFFinalrange2,BPFIFinalrange1,BPFIFinalrange2,BPFOFinalrange1,BPFOFinalrange2,BSFFinalrange1,BSFFinalrange2
    
    
    
    
####calculating BCF taking fault frequency ranges and shaft speed as input
# Vibration Frequency Fundamental Train:=FT
##Vibration Frequency Inner Ring Defect: VFIR
#Vibration Frequency Outer Ring Defect:  VFOR
#Vibration Frequency Roller Spin: VFRS  
#shaft speed in RPM
    
def bcffromfaultfreqRange(FT, VFRS,VFOR, VFIR, shaftspeed):
    FundamentalTrain =FT*shaftspeed
    InnerRingDefect = VFIR*shaftspeed
    OuterRingDefect = VFOR*shaftspeed
    RollerSpin = VFRS*shaftspeed
    return FundamentalTrain,RollerSpin, OuterRingDefect, InnerRingDefect 
    
####on passing averaged fft values ,getting corresponding frequencies of amplitudes which are above the RMS value.
##fftavg=averaged fft values ####samplingFrequency of the sensor ###window size of the data.
def fftcalculations(fftavg,samplingFrequency,windowsize):
    lst1=fftavg  ####fftavg should be in pandas.core.series.Series
    yf=(np.array(lst1[0:len(lst1)]))
    #yf1=[10*element for element in yf]  #scaling 
   #
    #####rms of fft values
    rms =np.sqrt(np.mean(np.square(yf))) 
    ####count of values which are greater the RMS
    count = len([i for i in yf if i >rms]) 
    ######correspondig frequency and amplitudes greater than 1.2xRMS 
    ac=sorted([(x,i) for (i,x) in enumerate(yf)], reverse=True )[:count]  
    ad=pd.DataFrame(ac,columns=['amplitude','Frequency'])
    ad1=ad['Frequency']
    
    ####multiplying (samplingFrequency/2)/windowsize) to frequencies to get actual frequency values of a spectrum.
    #lst=ad['Frequency']*((samplingFrequency/2)/windowsize)
    #freqs=lst.astype(int)
    return ad1

##R1=bcf of FTF, R2=BCF of BSF ,samplingFrequency,
##lst=frequencies after 
def FTF(R1,R2,samplingFrequency,lst,afterallowance,FTFFinalrange1,FTFFinalrange2):
    FTF=[i for i in lst if i in range(int(afterallowance*R1),int(afterallowance*R2))]
    ftfreq=[] #####fault train frequencies
    if len(FTF)>0:
        # print('first harmonics are present')
        for N in range(len(FTF)):
            # print('first harmonic is',FTF[N])
            tfshrs=int(2*FTFFinalrange2*FTF[N]) ####train frequency second harmonic range start value
            tfshre=int(2*FTFFinalrange1*FTF[N]) #####train frequency second harmonic range end value
            if tfshrs > int(0.5*samplingFrequency):
                print("sampling frequency of the sensor is not enough for the analysis")
            else:
                change=[k for k in lst if k in range(tfshrs,tfshre)]
                if len(change)>0:
                    # print('second harmonic ranges are ',range(tfshrs,tfshre))
                    # print('second harmonic is present',change)
                    tftrs=int(3*FTFFinalrange2*FTF[N]) ###spin frequency third harmonic range start value
                    tftre=int(3*FTFFinalrange1*FTF[N]) ####spin frequency third harmonic range end value
                    if tftrs > int(0.5*samplingFrequency):
                        print("sampling frequency of the sensor is not enough for the analysis")
                    else:
                        change1=[i for i in lst if i in range(tftrs,tftre)]
                        if len(change1)>0:
                            # print('third harmonic ranges are ',range(tftrs,tftre))
                            # print('third harmonic is present',change1)
                            # print('it is a strong evidence for train frequency fault')
                            ftfreq.append(FTF[N])
    return ftfreq
 
def BSF(R2,R3,samplingFrequency,lst,afterallowance,BSFFinalrange2,BSFFinalrange1):                          
    BSF=sorted([i for i in lst if i in range(int(afterallowance*R2),int(afterallowance*R3))])
    fsfreq=[] ###fault spin frequencies
    if len(BSF) > 0:
        # print('first harmonics are present')
        for M in range(len(BSF)):
            # print('first harmonic is',BSF[M])
            sfshrs=int(2*BSFFinalrange2*BSF[M]) ####spin frequency second harmonic range start value
            sfshre=int(2*BSFFinalrange1*BSF[M]) #####spin frequency second harmonic range end value
            if sfshrs > int(0.5*samplingFrequency):
                print("sampling frequency of the sensor is not enough for the analysis")
            else:
                change=[k for k in lst if k in range(sfshrs,sfshre)]
                if len(change)>0:
                    # print('second harmonic ranges are ',range(sfshrs,sfshre))
                    # print('second harmonic is present',change)
                    sftrs=int(3*BSFFinalrange2*BSF[M]) ###spin frequency third harmonic range start value
                    sftre=int(3*BSFFinalrange1*BSF[M]) ####spin frequency third harmonic range end value
                    if sftrs > int(0.5*samplingFrequency):
                        print("sampling frequency of the sensor is not enough for the analysis")
                    else:
                        change1=[i for i in lst if i in range(sftrs,sftre)]
                        if len(change1)>0:
                            # print('third harmonic ranges are ',range(sftrs,sftre))
                            # print('third harmonic is present',change1)
                            # print('it is a strong evidence for ball spin frequency')
                            fsfreq.append(BSF[M])
    return fsfreq

def BPFO(R3,R4,samplingFrequency,lst,afterallowance,BPFOFinalrange2,BPFOFinalrange1):
    BPFO=[i for i in lst if i in range(int(afterallowance*R3),int(afterallowance*R4))]
    offreq=[] ###outer race fault frequencies
    if len(BPFO) > 0:
        # print('first harmonics are present')
        for j in range(len(BPFO)):
            # print('first harmonic is',BPFO[j])
            oshrs=int(2*BPFOFinalrange2*BPFO[j]) ####outer race second harmonic range start value
            oshre=int(2*BPFOFinalrange1*BPFO[j]) #####outer race second harmonic range end value
            if oshrs > int(0.5*samplingFrequency):
                print("sampling frequency of the sensor is not enough for the analysis")
            else:
                change=[k for k in lst if k in range(oshrs,oshre)]
                if len(change)>0:
                    # print('second harmonic ranges are ',range(oshrs,oshre))                 
                    # print('second harmonic is present',change)
                    otrs=int(3*BPFOFinalrange2*BPFO[j]) ###outer race third harmonic range start value
                    otre=int(3*BPFOFinalrange1*BPFO[j]) #### outer race third harmonic range end value
                    if otrs > int(0.5*samplingFrequency):
                        print("sampling frequency of the sensor is not enough for the analysis")
                    else:
                        change1=[i for i in lst if i in range(otrs,otre)]
                        if len(change1)>0:
                            # print('third harmonic ranges are ',range(otrs,otre))
                            # print('third harmonic is present',change1)
                            # print('it is a strong evidence for outerrace')
                            offreq.append(BPFO[j])
    return offreq

def BPFI(R4,samplingFrequency,lst,afterallowance,BPFIFinalrange2,BPFIFinalrange1):               
    BPFI=sorted([i for i in lst if i>int(afterallowance*R4)])
    iffreq=[] ##inner race fault frequencies
    if len(BPFI)>0:
        # print('first harmonics are present')
        for i in range(len(BPFI)):
            # print('first harmonic is',BPFI[i])
            ishrs=int(2*BPFIFinalrange2*BPFI[i]) ####inner race second harmonic range start value
            ishre=int(2*BPFIFinalrange1*BPFI[i]) #####inner race second harmonic range end value
            if ishrs > int(0.5*samplingFrequency):
                print("sampling frequency of the sensor is not enough for the analysis")
            else:
                change=[i for i in lst if i in range(ishrs,ishre)]
                if len(change)>0:
                    # print('second harmonic ranges are ',range(ishrs,ishre))
                    # print('second harmonic is present',change)
                    itrs=int(3*BPFIFinalrange2*BPFI[i]) ###inner race third harmonic range start value
                    itre=int(3*BPFIFinalrange2*BPFI[i]) #### inner race third harmonic range end value
                    if itrs > int(0.5*samplingFrequency):
                        print("sampling frequency of the sensor is not enough for the analysis")
                    else:
                        change1=[i for i in lst if i in range(itrs,itre)]
                        if len(change1)>0:
                            # print('third harmonic ranges are ',range(itrs,itre))
                            # print('third harmonic is present',change1)
                            # print('it is a strong evidence for innerrace')
                            iffreq.append(BPFI[i])
    return iffreq




