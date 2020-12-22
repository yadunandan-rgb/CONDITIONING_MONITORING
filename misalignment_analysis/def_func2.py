# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 17:29:19 2020
@author: Prashanth
"""
import numpy as np
import pandas as pd
class Misalignment():
########################################################################
    def ShaftSpeed_detection(start_range, end_range, vibsig):
        amp = pd.DataFrame(vibsig) 
        amplist = amp[int(start_range):int(end_range)]
        amplist.rename(columns = {0: 'amp'}, inplace = True)    
        # amplitude = amplist['amp']
        amplist = amplist.reset_index()
        amp_freq = np.argmax(amplist['amp'])
        amp_x1 = (int(start_range))
        RPM = amp_x1 + amp_freq
        # print(RPM)
        return RPM
###########################################################################################
########################################################################
    def start_end_array (freqlimit, rpm):
        sub_limits = []
        for i in range(1, 9):
            Rpm = rpm * i
            limits = Rpm - (freqlimit * Rpm), Rpm + (freqlimit * Rpm)
            sub_limits.append(limits)
        return sub_limits
###########################################################################################
########################################################################
    def limits (limit, fft_Df):
        Max_value = []
        for j in limit:
            start, end = j
            start_x, end_y = int(start), int(end)
            harmonics_list = fft_Df.iloc[start_x : end_y]
            max_value = max(harmonics_list[0])
            Max_value.append(max_value)
        return Max_value
########################################################################
########################################################################
    def harmonics_1x_2x_3x(amplitude_1, amplitude_2, amplitude_3, threshold_1,
                            threshold_2, threshold_3):
        if amplitude_1 > threshold_1:
            result = "Harmonic at 1x RPM"
            if amplitude_2 > threshold_2:
                result = "Axial Misalignment"
            if amplitude_2 > amplitude_1:
                result = "parallel Misalignment"
                if amplitude_3 > threshold_3:
                    result = "Severe Misalignment"
        else:
            result = "No Misalignment"
        return result
    ########################################################################
########################################################################
    def harmonics_greater_than_3x (amplitude_4, amplitude_7, threshold_3):
        if amplitude_4 > threshold_3:
            result = "Looseness" 
            if amplitude_7 > threshold_3:
                result = "Severe Looseness"
        else:
            result = "No Looseness"
        return result
