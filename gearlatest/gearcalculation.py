import pandas as pd
import numpy as np
import heapq
def Rpm2nd_version(preferHorizontFFT,Sampling_freqn, Max_rpm,rpm_threshold):
    rpm_threshold = rpm_threshold
    maximum_rpm_hz = Max_rpm/60
    sampling_fre = Sampling_freqn
    time = 1/sampling_fre
    fft = preferHorizontFFT
    no_of_samples = len(fft)

    fft_y=abs(np.array(fft[0:no_of_samples // 2]))
    fft_x = np.linspace(0.0, 1.0 / (2.0 * time), no_of_samples // 2)

    fft_x_list = list(fft_x)
    amplitudesindex = [list(fft_y).index(i) for i in fft_y]
    amplitudesvalues = [float(i) for i in fft_y]
    frequency = [fft_x_list[i] for i in amplitudesindex ]
    indexfreqencylesthanrpm = [frequency.index(i) for i in frequency if rpm_threshold*maximum_rpm_hz<=i<=maximum_rpm_hz]
    indexfreqencylesthanrpmvalues = [frequency[i] for i in indexfreqencylesthanrpm ] #if i<=maximum_rpm
    amplitudesrpm = [amplitudesvalues[i] for i in indexfreqencylesthanrpm]
    largeinamplitud=heapq.nlargest(10,amplitudesrpm)
    
    indexofMaxAmplit = [amplitudesvalues.index(i) for i in largeinamplitud]
    frequencyforMaxamplit = [frequency[i] for i in indexofMaxAmplit]
    maxoneamplitude = max(amplitudesrpm)
    indexofamplitude = amplitudesvalues.index(maxoneamplitude)

    freuencycorrestomaxampl = frequency[indexofamplitude]

    rpmfreqCorresfreuencycorrestomaxampl = [i for i in frequencyforMaxamplit if i-1 <= freuencycorrestomaxampl/4 <= i+1 or i-1 <= freuencycorrestomaxampl/3 <= i+1 or i-1 <= freuencycorrestomaxampl/2 <= i+1]
    rpmfreqcorresto2x3x = [j for j in frequencyforMaxamplit for i in frequencyforMaxamplit if j-1 <= i/4 <= j+1 or j-1 <= i/3 <= j+1 or j-1 <= i/2 <= j+1 ]
    
    if rpmfreqcorresto2x3x==[]:
        rpmAmplitude = maxoneamplitude
        rpmis = freuencycorrestomaxampl
        #print(rpmis)
        
        # print(freuencycorrestomaxampl)
        return rpmis, rpmAmplitude
    else:
        
        rpmis = (rpmfreqcorresto2x3x[0])
        rpmis2_index = frequency.index(rpmis)
        rpm2_amplitude = amplitudesvalues[rpmis2_index]
        rpmAmplitude = rpm2_amplitude
        print(rpmAmplitude)
        return rpmis,rpmAmplitude


def gear_calculation(No_of_teeth_pinion,frequency_of_pinion,No_of_teeth_gear,Sampling_freqn,speed_of_pinion1):
   #frequency_of_pinion=float(Speed_of_pinion1)
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
 ###349.94
   #print(GEAR_GMFF)
   return  GMFF,gear_ratio,GEAR_FREQUENCY,GEAR_GMFF,frequency_of_pinion

def fftcalculations(fftavg,Sampling_freqn,window_size):
   lst1=fftavg
   #####rms of fft values
   rms =np.sqrt(np.mean(np.square(lst1))) 
   ####count of values which are greater the RMS
   count = len([i for i in lst1 if i > rms]) 
   ######correspondig frequency and amplitudes greater than 1.2xRMS 
   ac=sorted([(x,i) for (i,x) in enumerate(lst1)], reverse=True )[:count]  
   ad=pd.DataFrame(ac,columns=['amplitude','Frequency'])
   ####multiplying (samplingFrequency/2)/windowsize) to frequencies to get actual frequency values of a spectrum.
   lst=ad['Frequency']*((Sampling_freqn/2)/window_size)
   freqs=lst.astype(int)
   return freqs

def GMFF(No_of_teeth_pinion,frequency_of_pinion,Sampling_freqn,lst,afterallowance,afterfaultfreqallowanceminus,afterfaultfreqallowanceplus):
   GMFF=[i for i in lst if i in range(int(afterallowance*No_of_teeth_pinion),int(afterallowance*frequency_of_pinion))]
   ftfreq=[] #####fault train frequencies
   if len(GMFF)>0:
      # print('first harmonics are present')
      for N in range(len(GMFF)):
         # print('first harmonic is',FTF[N])
         tfshrs=int(2*afterfaultfreqallowanceminus*GMFF[N]) ####train frequency second harmonic range start value
         tfshre=int(2*afterfaultfreqallowanceplus*GMFF[N]) #####train frequency second harmonic range end value
         if tfshrs > int(0.5*Sampling_freqn):
            print("sampling frequency of the sensor is not enough for the analysis")
         else:
            change=[k for k in lst if k in range(tfshrs,tfshre)]
            if len(change)>0:
                    # print('second harmonic ranges are ',range(tfshrs,tfshre))
                    # print('second harmonic is present',change)
               tftrs=int(3*afterfaultfreqallowanceminus*GMFF[N]) ###spin frequency third harmonic range start value
               tftre=int(3*afterfaultfreqallowanceplus*GMFF[N]) ####spin frequency third harmonic range end value
               if tftrs > int(0.5*Sampling_freqn):
                  print("sampling frequency of the sensor is not enough for the analysis")
               else:
                  change1=[i for i in lst if i in range(tftrs,tftre)]
                  if len(change1)>0:
                     # print('third harmonic ranges are ',range(tftrs,tftre))
                            # print('third harmonic is present',change1)
                            # print('it is a strong evidence for train frequency fault')
                     ftfreq.append(GMFF[N])
   return ftfreq