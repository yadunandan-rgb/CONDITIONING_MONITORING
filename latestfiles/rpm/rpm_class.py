import paho.mqtt.client as mqtt  #import the client1
import time
from configparser import ConfigParser
import logging
import sys
from collections import deque
import logging.handlers as handlers
import pandas as pd
import numpy as np
import datetime
import json
from numpy import (array, dot, arccos, clip)
from numpy.linalg import norm
import pandas as pd
import matplotlib.pyplot as plt
import math as m
import numpy as np
from scipy import signal
from numpy import *
from  math  import *
import pandas as pd
import numpy as np
import cmath
import heapq
import logging as localLogging




class Rpm():
    def __init__(self,fft_signal,sampling_freq,Max_rpm):
        self.fft_signal = fft_signal
        self.sampling_freq = sampling_freq
        self.Max_rpm = Max_rpm
        self.rpmis = 0

    def Rpm4th_version(self):
        try:
            # Taking inputs
            maximum_rpm_hz = self.Max_rpm/60

            # rpm range from start rpm to end rpm
            rpm_thresholdStart = 0.3* maximum_rpm_hz
            rpm_thresholdend = 1.2*maximum_rpm_hz
            sampling_fre = self.sampling_freq
            time = 1/sampling_fre
            no_of_samples = len(self.fft_signal)

            fft_y=(np.array(self.fft_signal[0:no_of_samples]))
            fft_x = np.linspace(0.0, 1.0 / (2.0 * time), no_of_samples)
    
            fft_x_list = list(fft_x)
            amplitudesindex = [list(fft_y).index(i) for i in fft_y]
            amplitudesvalues = [float(i) for i in fft_y]
            frequency = [fft_x_list[i] for i in amplitudesindex ]

            # taking frequencies in range 0.3*max rpm to 1.2*max rpm and taking amplitudes corresponding to them
            indexfreqencylesthanrpm = [frequency.index(i) for i in frequency if rpm_thresholdStart<=i<=rpm_thresholdend]
            indexfreqencylesthanrpmvalues = [frequency[i] for i in indexfreqencylesthanrpm ] #if i<=maximum_rpm
            amplitudesrpm = [amplitudesvalues[i] for i in indexfreqencylesthanrpm]

            # Taking 10 peak amplitudes from rpm ranged amplitudes list
            largeinamplitud=heapq.nlargest(10,amplitudesrpm)
            indexofMaxAmplit = [amplitudesvalues.index(i) for i in largeinamplitud]
            frequencyforMaxamplit = [frequency[i] for i in indexofMaxAmplit]

            # Taking peak amplitude from 10 
            maxoneamplitude = max(amplitudesrpm)
            indexofamplitude = amplitudesvalues.index(maxoneamplitude)
            freuencycorrestomaxampl = frequency[indexofamplitude]
            rpmfreqCorresfreuencycorrestomaxampl = [i for i in frequencyforMaxamplit if i-1 <= freuencycorrestomaxampl/4 <= i+1 or i-1 <= freuencycorrestomaxampl/3 <= i+1 or i-1 <= freuencycorrestomaxampl/2 <= i+1]
            rpmfreqcorresto2x3x = []#j for j in frequencyforMaxamplit for i in frequencyforMaxamplit if j-1 <= i/4 <= j+1 or j-1 <= i/3 <= j+1 or j-1 <= i/2 <= j+1 ]
            if rpmfreqcorresto2x3x==[]:
                rpmAmplitude = maxoneamplitude
                self.rpmis = int(freuencycorrestomaxampl)
                # print(self.rpmis)
                return self.rpmis

        except Exception as e:
            print(str(e))
    def CallerMain(self):
        self.Rpm4th_version()


fft_data = [1.2266347333466992e-18, 0.0027807329072076967, 0.0016810292890631663, 0.00040824666810200977, 0.0014614349888484493, 0.004747705921383398, 0.009351308985333665, 0.023253892990985816, 0.0021235948984087206, 0.003870627647876974, 0.002023898790223093, 0.0014569038429024749, 0.013611861023212723, 0.0010365687780821355, 0.0014188254494518914, 0.0005506179847328084, 0.0009344212596421027, 0.004257638114417629, 0.0025842848327131377, 0.0007508633035108839, 0.0005951008862390737, 0.0013950769616789015, 0.0013492862101336296, 0.0003087948010228483, 0.00024877166211932693, 0.0003971346735252118, 0.0008519139348420496, 0.002441603557003843, 0.0009800750968677729, 0.001772544995507211, 0.0005583573951228529, 0.0042915276636410005, 0.004443620938980721, 0.0011457185332923185, 0.00014663863222039262, 0.0007522760914767401, 0.0015012541558535961, 0.015715775086710716, 0.0005990933156982622, 0.0032133728311866416, 0.0004967832333167562, 0.002112005561723464, 0.0014885465634877533, 0.0004419343400281783, 0.006497892483412314, 0.0003404756864249961, 0.0014851793086868455, 0.0016035045778055425, 0.00045425260794044407, 0.0019126488370397835, 0.0048198564911547705, 0.0018573985156222481, 0.001557999017887875, 0.00037582290526224987, 0.0027101670070983764, 0.0012189920944620188, 0.0018078235188215398, 0.0005419581556550737, 0.0011455849427786007, 5.132277865157583e-05, 0.00012790153038783557, 0.00015565291866469943, 0.0004793546633936902, 0.0017320116850706735, 0.002154623590295615, 0.0007008662507555554, 0.0005342770710076795, 0.0013996807949179266, 0.0012118462546252095, 0.006779433459306, 0.001036795855576846, 0.0011616161412799026, 0.002483196702170622, 0.001628350087875526, 0.0017982189012981113, 0.0014240767242215946, 0.002721430951131311, 0.00030924460869910915, 0.0018411315961843829, 0.000579731610008295, 0.0005429241710223393, 0.00040638568728418057, 0.0014844552069275356, 6.89461085644591e-05, 0.0006757992198681653, 0.0005404029722320138, 0.0012257558758773676, 0.004624668969328918, 0.0017410903604898535, 0.0018779856219638894, 0.0027536755258049067, 0.002347128889540806, 0.003074578628601645, 0.0008663843372623331, 0.00018902191410239585, 0.0031350308257228647, 0.0013025785268789144, 0.00282075515218278, 0.0011230719153479981, 0.003186127125078925, 0.00626404928855447, 0.003177715177310777, 0.0014758206352309096, 0.0010629974311604537, 0.00034015996720359963, 0.0035122238243047214, 0.003096770818906011, 0.004839308467614151, 0.0021734451080941803, 0.0040588506175182285, 0.0007694162084722584, 0.0004457852880240715, 0.0056017681701511024, 0.0015732721865961716, 0.0027823921194450713, 0.004891410099420838, 0.0014567499856664185, 0.002676428179554941, 0.0027202665166678264, 0.004632007991851045, 0.0014321698361178339, 0.0010987440195606598, 0.0021825749953592348, 0.0009274042085290553, 0.0028209157545245962, 0.00375378483153404, 0.0020647649554033443, 0.0007871367131353767, 0.002943119729811549, 7.459654106786896e-05, 0.0006086952618816776, 0.006366650588929222, 0.009375215687393126, 0.00037813532011584446, 0.0033419583100154906, 0.002306649120603311, 0.0032707963242832763, 0.0014933992140573073, 0.006234315808271696, 0.0015213831460827699, 0.0020133625358653615, 0.00036806997160555583, 0.0005537612217707745, 9.05318653667545e-06, 0.0014858363220344945, 0.002848455453059165, 0.0014983218927095258, 0.0017517443932048035, 0.000995434825191149, 0.0027902272063501416, 0.0009357899529213879, 0.0016951345725650505, 0.0017641726189645739, 0.0020089402603804853, 0.0012388775665960635, 0.0002954980681204253, 0.003398103675710133, 0.0006186817960016458, 4.6304734764640945e-05, 0.0009397596937350991, 0.0004416370259493169, 0.0012168835501947125, 0.00041699415787350096, 0.001319125884744059, 0.0014060713850739628, 0.000466431996630295, 0.0012111347392224359, 0.00020771121110012373, 0.001985791654629386, 0.002613131234534436, 0.00292202006897395, 0.0016701970463767464, 0.000929234162094441, 5.8751041389019e-07, 0.0007807048039804691, 0.00025616694681544533, 0.0010427683459823416, 0.005035202697092514, 0.0015654008998138582, 0.0014696893798853386, 0.00040584337107802933, 0.0015137157508936527, 0.002018107209522872, 0.0010660471593589725, 0.0003820967760472869, 0.0019106352568651953, 0.003027117750516529, 0.0009133898602938448, 0.0018870229467474976, 0.0018677023827030305, 0.0021686753745378687, 0.0040500623604614525, 0.0007055180451639621, 0.002476776981882001, 0.0051955274074358395, 0.0031816229683664697, 0.0011800446414486506, 0.0007388031743813696, 0.0010427448862513331, 0.0007200169180853185, 0.000208914191934083, 0.005926883070030772, 0.00301226065354492, 0.006085627885457028, 0.0006725292279919582, 0.0027298323854364217, 0.002425959619980142, 8.649540420100739e-05, 0.0025094535918559822, 1.0982844701384744e-05, 0.0018493555892149286, 0.0011261118270675227, 0.0009498448129367448, 0.0006194048940959438, 0.003170501502674341, 0.002963816852995525, 0.002459291743098764, 0.003313304630297022, 0.0011131829300603943, 0.0027815947173088643, 0.0016119004494962647, 0.003372169511805069, 0.0009723826216140633, 0.0007863382198374742, 0.0002230660022869281, 0.002874636731370278, 0.0047793417413564175, 0.0010342082330152, 0.0030985053075022607, 0.0004154800021965768, 0.003406765995328194, 0.002849677044931188, 0.004109417587304127, 0.0011727442349917599, 0.00035132416484164703, 0.0019154159377469566, 0.0027720196022152986, 0.0007035853813265104, 0.0013743214114067632, 0.004313479702807607, 0.0023676699466390395, 0.0021832049382822373, 0.001174738872117265, 0.0008423939872669439, 0.0018917518596467773, 0.0008470168725306953, 0.000721732703090095, 0.000924497719271512, 0.0003412632876893224, 1.3309894542109241e-05, 0.0008207705083231882, 0.0002471210063425052, 0.0027071298840891872, 0.00015291852546174192, 0.0010525293443705325, 0.0021846904341685947]



rpmisss = Rpm(fft_data,1600,3600)
# print(rpmisss.Rpm4th_version())














































# def Rpm4th_version(self):

#         maximum_rpm_hz = self.Max_rpm/60 

#         rpm_thresholdStart = 0.3* maximum_rpm_hz

#         rpm_thresholdend = 1.2*maximum_rpm_hz

#         sampling_fre = self.sampling_freq

#         time = 1/sampling_fre

#         fft = self.fft_signal

#         no_of_samples = len(self.fft_signal)

#         fft_y=(np.array(self.fft_signal[0:no_of_samples]))

#         fft_x = np.linspace(0.0, 1.0 / (2.0 * time), no_of_samples)
    
#         fft_x_list = list(fft_x)

#         amplitudesindex = [list(fft_y).index(i) for i in fft_y]

#         amplitudesvalues = [float(i) for i in fft_y]

#         frequency = [fft_x_list[i] for i in amplitudesindex ]

#         indexfreqencylesthanrpm = [frequency.index(i) for i in frequency if rpm_thresholdStart<=i<=rpm_thresholdend]

#         indexfreqencylesthanrpmvalues = [int(frequency[i]) for i in indexfreqencylesthanrpm ] #if i<=maximum_rpm


#         amplitudesrpm = [amplitudesvalues[i] for i in indexfreqencylesthanrpmvalues]

#         largeinamplitud=heapq.nlargest(10,amplitudesrpm)

#         indexofMaxAmplit = [amplitudesvalues.index(i) for i in largeinamplitud]

#         frequencyforMaxamplit = [frequency[i] for i in indexofMaxAmplit]

#         if amplitudesrpm!=[]:

#             maxoneamplitude = max(amplitudesrpm)

#             indexofamplitude = amplitudesvalues.index(maxoneamplitude)

#             freuencycorrestomaxampl = frequency[indexofamplitude]

#             rpmfreqCorresfreuencycorrestomaxampl = [i for i in frequencyforMaxamplit if i-1 <= freuencycorrestomaxampl/4 <= i+1 or i-1 <= freuencycorrestomaxampl/3 <= i+1 or i-1 <= freuencycorrestomaxampl/2 <= i+1]
        
#             rpmfreqcorresto2x3x = []#j for j in frequencyforMaxamplit for i in frequencyforMaxamplit if j-1 <= i/4 <= j+1 or j-1 <= i/3 <= j+1 or j-1 <= i/2 <= j+1 ]

#             if rpmfreqcorresto2x3x==[]:
#                 rpmAmplitude = maxoneamplitude
#                 self.rpmis = freuencycorrestomaxampl
#                 print('first',self.rpmis)
#                 return self.rpmis, rpmAmplitude