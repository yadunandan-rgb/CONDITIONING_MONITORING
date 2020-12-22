# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 17:29:19 2020
@author: Prashanth
"""
import numpy as np
import os
#os.chdir(r"F:\Vegam_Office\Code") 
import pandas as pd
import def_func2 as function
import time
from scipy import signal
from scipy.fftpack import fft, ifft
import matplotlib.pyplot as plt
import matplotlib.patches as patches

start = time.time()
########################################################################
windowsize = 0 ##Range of window size (Start)
window_val = 256 ##Range of window size (End)
windowsize1 = window_val
samplewindow = window_val
sampling_frequency = 1600
reference_rpm = 3600
maximum_rpm = reference_rpm / 60
actual_rpm = 13
# allowance = 0.2
# freq_start_range = maximum_rpm - maximum_rpm * 0.26
# freq_end_range = maximum_rpm + maximum_rpm * 0.1
T = 1/sampling_frequency
nwindows = 1
########################################################################
basf=pd.read_csv(r"C:/Users/user/Downloads/0081F99EF478FFTX.csv",skiprows=1,header=None)
########################################################################
basf.replace(regex=True, inplace=True, to_replace=r'[^0-9.E-]', value=r'')
basf=basf.apply(pd.to_numeric, errors='coerce')
basf.rename(columns={0:'signalid',1:'t',2:'sf'},inplace=True)
basf.columns.values[-1]='q'
########################################################################
mapp={}
indices=[]
j=0
for i in range(3,(len(basf.columns)-1)):  ####"""here -3 will vary depending on FFT data in excel"""
    mapp.update({i:"V"+str(j)})
    indices.append(i)
    j+=1
basf.rename(columns=mapp,inplace=True)  ###renaming all the columns
windowstart = 0
windowend = nwindows
########################################################################
########################################################################
# F:/Vegam_Office/Data/Dynaspede_mis/Dynaspede_misalignment/90Bx_10_10_4.csv
# data = pd.read_csv(r"F:/Vegam_Office/Data/Dynaspede_mis/Dynaspede_misalignment/90Bx_10_10_4.csv",skiprows=1,header=None)
# data = pd.read_csv(r"F:/Vegam_Office/Data/Dynaspede_mis/Dynaspede_misalignment/9.25.10.11.Y_90B.csv",skiprows=1,header=None)
########################################################################
########################################################################
# data = pd.read_csv(r"F:/Vegam_Office/Data/Mafaulda Horizontal_misalignment/12.288.csv.csv",skiprows=1,header=None)
# data = data.head(1024)
# data_1 = data[2]
########################################################################
########################################################################
data_1 = basf
########################################################################
windowstart = 0
windowend = nwindows
########################################################################
########################################################################
RPM = []
Max_value = []
Misalignment = []
Looseness = []
dataframe = pd.DataFrame()
########################################################################
# def func_FaultAnalysis(windowsize, window_val, windowsize1, df_signal):
for row in range(0,len(basf),nwindows):
    df = basf.iloc[windowstart:windowend,indices]
    avg_window = df.mean()###averaging of the windows 
    fft_val = avg_window
    N = len(fft_val)
    yf= (np.array(fft_val[0:N]))
    freq_start_range = maximum_rpm - maximum_rpm * 0.8
    freq_end_range = maximum_rpm + maximum_rpm * 0.2
    xf = np.linspace(0.0, 1.0 / (2.0 * T), N//2)
    forrpm = function.ShaftSpeed_detection(freq_start_range, freq_end_range, yf)
    RPM.append(forrpm)
    
    threshold_RMS = np.sqrt(np.mean(np.square(yf)))
    threshold = threshold_RMS*1
    second_thrsld = threshold*0.40
    third_thrsld = threshold*0.30
    
    fft_series = pd.Series(yf, name=0)
    fft_DF = pd.DataFrame(abs(fft_series))
    freqlimit = 0.2
        
    sub_limits = function.start_end_array(freqlimit, forrpm)
    print(sub_limits)
    list_limits = pd.DataFrame(sub_limits, columns = ['start_range', 
                                                      'End_range'])
    #print(list_limits)
           
    Max_value = function.limits(sub_limits, fft_DF)
          
    result =  function.harmonics_1x_2x_3x(Max_value[0], Max_value[1], Max_value[2],
                              threshold, second_thrsld, third_thrsld)
    
    Misalignment.append(result)
    #print(Misalignment)
    
    looseness_result = function.harmonics_greater_than_3x (Max_value[3], Max_value[7], 
                                          third_thrsld)
    Looseness.append(looseness_result)
    #print(Looseness)
    windowsize = windowsize + window_val
    windowsize1=windowsize1 + window_val
        
# val = func_FaultAnalysis(windowsize, window_val, windowsize1, data)

# end = time.time()
# print(end - start)
########################################################################
########################################################################
Max_value_df = pd.DataFrame(Max_value, columns = ['Max_value'])
Misalignment_Result = pd.DataFrame(Misalignment, columns = ['Result'])
# dataframe['Misalignment_Result'] = Misalignment_Result['Result']
# # # dataframe['Looseness_Result'] = Looseness_Result['Result']
# dataframe
#dataframe['Max_Speed'] = reference_rpm_hz
## dataframe['Actual_Speed'] = RPM
#dataframe['Dataset_Used'] = str(dataset_used)
#dataframe['Actual_Speed'] = str(data_name)
#dataframe = dataframe[['Dataset_Used', 'Max_Speed', 'Actual_Speed', 
                          # 'Misalignment_Result', 'Looseness_Result']]
#dataframe
########################################################################
                         # END
########################################################################

