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
import collections
from numpy import (array, dot, arccos, clip)
from numpy.linalg import norm
from configparser import ConfigParser

import csv
import heapq
import timeit
import collections
import time
import pandas as pd
import numpy as np
import math
from configparser import ConfigParser
import os
import matplotlib.pyplot as plt
import heapq
from collections import Counter
from configparser import ConfigParser
import logging as localLogging

class unbalance():
	def __init__(self,fft_signal,sampling_freq,Max_rpm,horizontAccelData,verticalAccelData):
		self.fft_signal = fft_signal
		self.sampling_freq = sampling_freq
		self.Max_rpm = Max_rpm
		self.df1 =horizontAccelData
		self.df2 =verticalAccelData
		#self.angle = angle
	def Rpm(self):
		try:
			maximum_rpm_hz = self.Max_rpm/60
			rpm_thresholdStart = 0.3*maximum_rpm_hz
			rpm_thresholdend = 1.2*maximum_rpm_hz
			sampling_fre = self.sampling_freq
			time = 1/sampling_fre
			no_of_samples = len(self.fft_signal)
			fft_y=(np.array(self.fft_signal[0:no_of_samples]))
			fft_x = np.linspace(0.0, 1.0 / (2.0 * time), no_of_samples)
			fft_x_list = list(fft_x)
			amplitudesindex = [list(fft_y).index(i) for i in fft_y]
			amplitudesvalues = [float(i) for i in fft_y]
			frequency = [fft_x_list[i] for i in amplitudesindex]
			indexfreqencylesthanrpm = [frequency.index(i) for i in frequency if rpm_thresholdStart<=i<=rpm_thresholdend]
			indexfreqencylesthanrpmvalues = [frequency[i] for i in indexfreqencylesthanrpm ] #if i<=maximum_rpm
			amplitudesrpm = [amplitudesvalues[i] for i in indexfreqencylesthanrpm]
			largeinamplitud=heapq.nlargest(10,amplitudesrpm)
			indexofMaxAmplit = [amplitudesvalues.index(i) for i in largeinamplitud]
			frequencyforMaxamplit = [frequency[i] for i in indexofMaxAmplit]
			maxoneamplitude = max(amplitudesrpm)
			indexofamplitude = amplitudesvalues.index(maxoneamplitude)
			freuencycorrestomaxampl = frequency[indexofamplitude]
			rpmfreqCorresfreuencycorrestomaxampl = [i for i in frequencyforMaxamplit if i-1 <= freuencycorrestomaxampl/4 <= i+1 or i-1 <= freuencycorrestomaxampl/3 <= i+1 or i-1 <= freuencycorrestomaxampl/2 <= i+1]
			rpmfreqcorresto2x3x = []#j for j in frequencyforMaxamplit for i in frequencyforMaxamplit if j-1 <= i/4 <= j+1 or j-1 <= i/3 <= j+1 or j-1 <= i/2 <= j+1 ]
			if rpmfreqcorresto2x3x==[]:
				rpmAmplitude = maxoneamplitude
				self.rpmis = int(freuencycorrestomaxampl)
				return self.rpmis
		except Exception as e:
			print(str(e))
	
	# Below is online code, since I have used it inside dataframe, below use self.df1['v'] for horizont and vertical
	def phasefind(self):
		try:
			horizontalaxesamplitude = list(self.df1)#['v'])
			verticalamplitude = list(self.df2)#['v'])
			if len(self.df2)!=len(self.df1):
				difference = abs(len(horizontalaxesamplitude)-len(verticalamplitude))
				if len(horizontalaxesamplitude)>len(verticalamplitude):
					horizontalaxesamplitude = horizontalaxesamplitude[: -difference or None]  #to delete last n elemenets
					verticalamplitude = verticalamplitude
				elif len(verticalamplitude)>len(horizontalaxesamplitude):
					verticalamplitude = verticalamplitude[: -difference or None] 
					horizontalaxesamplitude = horizontalaxesamplitude
				amplitudeX =  horizontalaxesamplitude 
				amplitudeY =  verticalamplitude 
				c = dot(amplitudeX,amplitudeY)/norm(amplitudeX)/norm(amplitudeY)
				angle = arccos(clip(c, -1, 1))
				angleindegree = ((angle*360)/(2*3.14))
				# print('angle in degree',((angle*360)/(2*3.14)))
				return angleindegree
			else:
				amplitudeX =  horizontalaxesamplitude 
				amplitudeY =  verticalamplitude
				c = dot(amplitudeX,amplitudeY)/norm(amplitudeX)/norm(amplitudeY)
				angle = arccos(clip(c, -1, 1))
				angleindegree = ((angle*360)/(2*3.14))
				# print('angle in degree',((angle*360)/(2*3.14)))
				return angleindegree
		except Exception as e:
			print(str(e))
	def unbalance1axes(self,rpm,angles):
		try:
			# Inputs
			Fs = float(self.sampling_freq)
			T = 1/Fs
			N = len(self.fft_signal)

			# For phase angle range
			start_angle = int(90-30)
			end_angle = int(90+30)

			# 1x and looseness harmonics range
			start1x = 0.8
			end1x = 1.2
			loosenessrange = 10.3

			# FFT rms threshold to differentiate good and bad data
			fft_y=(np.array(self.fft_signal[0:N]))
			fft_x = np.linspace(0.0, 1.0 / (2.0 * T), N)
			fft_rms_Ampl = np.sqrt(np.mean(np.square(fft_y)))

			# Taking only those data which is above 1.2 times fft rms
			fft_rms_index = [list(fft_y).index(i) for i in fft_y if i>1.2*fft_rms_Ampl ] #taking amplitude above 1.5*rms
			fft_rms_values = [i for i in fft_y if i>1.2*fft_rms_Ampl]
			frequency_above_rms = [list(fft_x)[i] for i in fft_rms_index ]#if i<=maximum_rpm #frequency corres to 1.25*rms amplitudes
			
			# rpm
			

			# Taking rpm 1x range to detect unbalance fault
			rpm1xranage = [i for i in frequency_above_rms if start1x*rpm<=i<=end1x*rpm]
			max1xrpmAmplitude = max([fft_rms_values[frequency_above_rms.index(i)] for i in rpm1xranage])
			max1xrpmAmplitude = max1xrpmAmplitude

			# Checking for multiple harmonics with 20%, from 2x to 10.5x checking harmonics corresponding to 1x harmonic
			harmonic_allowance = 0.2
			# harmonicsfrequ = [i for i in frequency_above_rms if ((finalRPM*2)-harmonic_allowance)<= i <= ((finalRPM*2)+harmonic_allowance) or ((finalRPM*2.5)-harmonic_allowance)<= i <= ((finalRPM*2.5)+harmonic_allowance) or ((finalRPM*3)-harmonic_allowance)<= i <= ((finalRPM*3)+harmonic_allowance) or ((finalRPM*3.5)-harmonic_allowance)<= i <= ((finalRPM*3.5)+harmonic_allowance) or ((finalRPM*4)-harmonic_allowance)<= i <= ((finalRPM*4)+harmonic_allowance) or ((finalRPM*4.5)-harmonic_allowance)<= i <= ((finalRPM*4.5)+harmonic_allowance) or ((finalRPM*5)-harmonic_allowance)<= i <= ((finalRPM*5)+harmonic_allowance) or ((finalRPM*5.5)-harmonic_allowance)<= i <= ((finalRPM*5.5)+harmonic_allowance) or ((finalRPM*6)-harmonic_allowance)<= i <= ((finalRPM*6)+harmonic_allowance) or ((finalRPM*6.5)-harmonic_allowance)<= i <= ((finalRPM*6.5)+harmonic_allowance) or ((finalRPM*7)-harmonic_allowance)<= i <= ((finalRPM*7)+harmonic_allowance) or ((finalRPM*7.5)-harmonic_allowance)<= i <= ((finalRPM*7.5)+harmonic_allowance) or ((finalRPM*8)-harmonic_allowance)<= i <= ((finalRPM*8)+harmonic_allowance) or ((finalRPM*8.5)-harmonic_allowance)<= i <= ((finalRPM*8.5)+harmonic_allowance) or ((finalRPM*9)-harmonic_allowance)<= i <= ((finalRPM*9)+harmonic_allowance) or ((finalRPM*9.5)-harmonic_allowance)<= i <= ((finalRPM*9.5)+harmonic_allowance) or ((finalRPM*10)-harmonic_allowance)<= i <= ((finalRPM*10)+harmonic_allowance) or ((finalRPM*10.5)-harmonic_allowance)<= i <= ((finalRPM*10.5)+harmonic_allowance)]
			harmonicsfrequ = [i for i in frequency_above_rms if ((rpm*2)-(rpm*harmonic_allowance))<= i <= ((rpm*2)+(rpm*harmonic_allowance)) or ((rpm*2.5)-(rpm*harmonic_allowance))<= i <= ((rpm*2.5)+(rpm*harmonic_allowance)) or ((rpm*3)-(rpm*harmonic_allowance))<= i <= ((rpm*3)+(rpm*harmonic_allowance)) or ((rpm*3.5)-(rpm*harmonic_allowance))<= i <= ((rpm*3.5)+(rpm*harmonic_allowance)) or ((rpm*4)-(rpm*harmonic_allowance))<= i <= ((rpm*4)+(rpm*harmonic_allowance)) or ((rpm*4.5)-(rpm*harmonic_allowance))<= i <= ((rpm*4.5)+(rpm*harmonic_allowance)) or ((rpm*5)-(rpm*harmonic_allowance))<= i <= ((rpm*5)+(rpm*harmonic_allowance)) or ((rpm*5.5)-(rpm*harmonic_allowance))<= i <= ((rpm*5.5)+(rpm*harmonic_allowance)) or ((rpm*6)-(rpm*harmonic_allowance))<= i <= ((rpm*6)+(rpm*harmonic_allowance)) or ((rpm*6.5)-(rpm*harmonic_allowance))<= i <= ((rpm*6.5)+(rpm*harmonic_allowance)) or ((rpm*7)-(rpm*harmonic_allowance))<= i <= ((rpm*7)+(rpm*harmonic_allowance)) or ((rpm*7.5)-(rpm*harmonic_allowance))<= i <= ((rpm*7.5)+(rpm*harmonic_allowance)) or ((rpm*8)-(rpm*harmonic_allowance))<= i <= ((rpm*8)+(rpm*harmonic_allowance)) or ((rpm*8.5)-(rpm*harmonic_allowance))<= i <= ((rpm*8.5)+(rpm*harmonic_allowance)) or ((rpm*9)-(rpm*harmonic_allowance))<= i <= ((rpm*9)+(rpm*harmonic_allowance)) or ((rpm*9.5)-(rpm*harmonic_allowance))<= i <= ((rpm*9.5)+(rpm*harmonic_allowance)) or ((rpm*10)-(rpm*harmonic_allowance))<= i <= ((rpm*10)+(rpm*harmonic_allowance)) or ((rpm*10.5)-(rpm*harmonic_allowance))<= i <= ((rpm*10.5)+(rpm*harmonic_allowance))]
			harmonicAmpli = [fft_rms_values[frequency_above_rms.index(i)] for i in harmonicsfrequ ]
			
			# Considering harmonics above 40% of 1x harmonics to detect other faults
			harmonicAmplituAbove40percent1x = [i for i in harmonicAmpli if i>0.4*max1xrpmAmplitude]
			onepoint8to10point2freq = [i for i in frequency_above_rms if end1x*rpm<=i<=loosenessrange*rpm]
			amplitude_corres_frequency10Point2 = [fft_rms_values[frequency_above_rms.index(i)] for i in onepoint8to10point2freq]
			amplitud40PercentAbove = [i for i in amplitude_corres_frequency10Point2 if i>0.4*max1xrpmAmplitude]
			freqonepoint2to10point2 = [frequency_above_rms[amplitud40PercentAbove.index(i)] for i in amplitud40PercentAbove]
			
			# Returning faults with respect to their condition
			if harmonicAmplituAbove40percent1x!=[]:
				result = 2
				# print(result)
				return 'Check for other faults'

			# In unbalance phase angle will be 90 degree
			elif  start_angle <= angles <= end_angle:
				return "Unbalance"
				result = 1
			else:

				result = 0
				return "No faults"
		except Exception as e:
			print(str(e))
	def unbalancetotal(self):
		try:    
			rpmis = self.Rpm()
			angle = self.phasefind()
			faultis = self.unbalance1axes(rpmis,angle)
			return faultis
		except Exception as e:
			print(str(e))
		
      

