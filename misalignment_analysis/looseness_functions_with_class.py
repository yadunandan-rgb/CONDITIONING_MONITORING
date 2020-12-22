# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 12:46:18 2020

@author: User
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 17:29:19 2020
@author: Prashanth
"""
import numpy as np
import pandas as pd
sub_limits = []
Max_value = []

class Looseness():
    def __init__(self,samplingFrequency,nsamp,windowsize,fftlist,referencerpm):
        self.freqnLimit=float(0.2)
        #self.rpm=shaftspeed
        self.Sampling_Frequency=samplingFrequency
        self.No_sample=nsamp
        self.Window_Size = windowsize
        self.FFT_list=fftlist
        self.reference_rpm=referencerpm
        self.sub_limits=[]
        self.Max_value=[]
        
#####################################################################
    ########################################################################
    
#################
    def rpm_ranges(self):
        try:
            self.maxrpm=self.reference_rpm/60
            self.freq_start_range = self.maxrpm -(self.maxrpm * 0.8)
            self.freq_end_range = self.maxrpm + (self.maxrpm * 0.2)
            return self.freq_start_range,self.freq_end_range
        except Exception as e:
            print(str(e))
        
    def FFT_calculations(self,fftdata):
        try:
            
            self.average= [sum(e)/len(e) for e in zip(*fftdata)]
            self.xf = np.linspace(0.0, 1.0 / (2.0 * (1/self.Sampling_Frequency)), len(self.average))  #frequencies selection
            #average= [sum(e)/len(e) for e in zip(*FFT_list)]
        # avg_window = df.mean()###averaging of the windows 
            self.fft_val = self.average
            N = len(self.fft_val)
            self.yf= (np.array(self.fft_val[0:N]))
            fft_series = pd.Series(self.yf, name=0)
            self.fft_DF = pd.DataFrame(abs(fft_series))
            
            
            return self.yf,self.fft_DF #returns the ampltide,frqns, and rms 
        except Exception as e:
            print(str(e))
    def ShaftSpeed_detection(self,start_range, end_range, vibsig):
        try:
            amp = pd.DataFrame(vibsig) 
            amplist = amp[int(start_range):int(end_range)]
            amplist.rename(columns = {0: 'amp'}, inplace = True)    
         # amplitude = amplist['amp']
            amplist = amplist.reset_index()
            amp_freq = np.argmax(amplist['amp'])
            amp_x1 = (int(start_range))
            self.RPM = amp_x1 + amp_freq
    # print(RPM)
            return self.RPM
        except Exception as e:
            print(str(e))
        
    def rms_ranges(self,fftdata):
        self.average= [sum(e)/len(e) for e in zip(*fftdata)]
        self.rms =np.sqrt(np.mean(np.square(self.average))) #fft values are averaged
        self.rms2=self.rms*0.40
        self.rms3=self.rms*0.3
        return self.rms,self.rms2,self.rms3
        
    def start_end_array (self,rpm):
        try:    
            for i in range(1, 9):
                Rpm = rpm * i
                self.limitss = Rpm - (self.freqnLimit * Rpm), Rpm + (self.freqnLimit * Rpm)
                self.sub_limits.append(self.limitss)
            return self.sub_limits
        except Exception as e:
            print(str(e))
    ###########################################################################################
    ########################################################################
    def limits (self,limit,fft_Df):
        try:
            for j in limit:
                start, end = j
                start_x, end_y = int(start), int(end)
                harmonics_list = fft_Df.iloc[start_x : end_y]
                max_value = max(harmonics_list[0])
                self.Max_value.append(max_value)
            return self.Max_value
        except Exception as e:
            print(str(e))
    ########################################################################
    ########################################################################
    def looseness_check (self,amplitude_4, amplitude_7, threshold_3):
        try:
            if amplitude_4 > threshold_3:
                result = "Looseness" 
                if amplitude_7 > threshold_3:
                    result = "Severe Looseness"
            else:
                result = "No Looseness"
            return result
        except Exception as e:
            print(str(e))
    def looseness_total_check(self,fftdata):
        try:
            yf,fft_data=self.FFT_calculations(fftdata)
        
            startrange,endrange=self.rpm_ranges()
            forrpm = self.ShaftSpeed_detection(startrange,endrange,yf)
            limits=self.start_end_array(forrpm)
            sublimit=self.limits(limits,fft_data)
            rmsthreshold1,rmsthreshold2,rmsthreshold3=self.rms_ranges(fftdata)
            loose_result=self.looseness_check(sublimit[4],sublimit[7],rmsthreshold3)
            return loose_result
        except Exception as e:
            print(str(e))
    """def looseness_check (self,amplitude_4, amplitude_7, threshold_3):
        try:
            if amplitude_4 > threshold_3:
                result = "Looseness" 
                if amplitude_7 > threshold_3:
                    result = "Severe Looseness"
            else:
                result = "No Looseness"
            return result
        except Exception as e:
            print(str(e))"""