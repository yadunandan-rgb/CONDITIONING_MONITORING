import pylab as pyl
import numpy as np
import scipy as sy
import scipy.fftpack as syfp
from scipy import signal
from scipy.fftpack import fft, ifft
import matplotlib.pyplot as plt
import pandas as pd
import os
from scipy.signal import find_peaks_cwt
import csv
import heapq
import datetime
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import scipy.signal
import numpy as np
def harvest_get_downsampled_signal(x, fs, target_fs):
    decimation_ratio = np.round(fs / target_fs)
    offset = np.ceil(140. / decimation_ratio) * decimation_ratio
    start_pad = x[0] * np.ones(int(offset), dtype=np.float32)
    end_pad = x[-1] * np.ones(int(offset), dtype=np.float32)
    x = np.concatenate((start_pad, x, end_pad), axis=0)

    if fs < target_fs:
        raise ValueError("CASE NOT HANDLED IN harvest_get_downsampled_signal")
    else:
        try:
            y0 = scipy.signal.decimate(x, int(decimation_ratio), 3, zero_phase=True)
        except:
            y0 = scipy.signal.decimate(x, int(decimation_ratio), 3)
        actual_fs = fs / decimation_ratio
        y = y0[int(offset / decimation_ratio):-int(offset / decimation_ratio)]
    y = y - np.mean(y)
    y = list(y)
    return y #,actual_fs

os.chdir(r'D:\bearinglatest2\imsnasa\1st_test_csv')
#########files path ###
path=r'D:\bearinglatest2\imsnasa\1st_test_csv'
####listing out the files
ac=os.listdir(path)
#####inputs from configuration file #######
recordstarttime=[]
recordendtime=[]
filename=[]
sampling_frequency = 20000
requiredSampling = 1600
########loop for the list of files in the directory
for n in range(len(ac)):
    # reading data one by one
    mendeley_data=pd.read_csv(path+'/'+ac[n])
    ###defining the empty list 
    #bd=[]
    bc=[]
    aa=[]
    res=[]
    count=0
    for i in range(len(mendeley_data)):
        #bd.append(mendeley_data['Channel_2'].iloc[i])
        bc.append(mendeley_data['Bearing3'].iloc[i])
        resample_signal = harvest_get_downsampled_signal(bc,sampling_frequency,requiredSampling)
        mendleydatawithtstamp=pd.DataFrame(resample_signal,columns=['v'])
        mendleydatawithtstamp.to_csv(ac[n],index=False)


