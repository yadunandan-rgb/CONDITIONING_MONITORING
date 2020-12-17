import paho.mqtt.client as mqtt  #import the client1
import time
from configparser import ConfigParser
import logging
import sys
from collections import deque
import logging.handlers as handlers
import pandas as pd
import datetime
import json
import numpy as np
import math
nb=4
bd=0.76
p_d=0.56
angles=0
Shaftspeed=83
samplingFrequency=1600
nsamp=4096
windowsize=512
brokerport=1883
brokeraddress="176.9.144.238"
tagname="A434F17EE90B/FFTX" 
nwindows=nsamp/windowsize
lim_value=0.3
timetocompleteoneburst=nsamp/samplingFrequency
time_diff_btw_windows=timetocompleteoneburst/nwindows
class Bearing_analysis():

    def __init__(self,NB,BD,PD,angle,shaftspeed,samplingFrequency,nsamp,windowsize,average):
        self.Limit_value=float(0.3)
        self.N_B=int(NB)
        self.B_D=float(BD)
        self.P_D=float(PD)
        self.Angle=float(angle)
        self.Shaft_Speed=shaftspeed
        self.Sampling_Frequency=samplingFrequency
        self.No_sample=nsamp
        self.Window_Size = windowsize
        self.Average=average
        self.resultant=[]
        self.resultant1=[]
        self.resultant2=[]
        self.resultant3=[]
        
#####function for handling log functions ####################
    

    def BCF(self,NB,BD,PD,angle,shaftspeed): #NB,BD,PD,ANGLE are bearing inputs
        self.Fcir=((1/2)*(1-(self.B_D/self.P_D)*math.cos(self.Angle)))
        self.FTF=self.Fcir*self.Shaft_Speed #fundamental train frequency
        self.FTFFinal=float(self.FTF)
        
        #print(FTFFinal)
        
        self.Bfir=((self.N_B/2)*(1+(self.B_D/self.P_D)*math.cos(self.Angle)))
        self.BPFI=self.Bfir*self.Shaft_Speed #ball pass frequency of inner race
        self.BPFIFinal=float(self.BPFI)
        #(FTFFinal)
        
        #print(BPFIFinal) 
        
        self.Bfor=((self.N_B/2)*(1-(self.B_D/self.P_D)*math.cos(self.Angle)))
        self.BPFO=self.Bfor*self.Shaft_Speed #ball pass frequency  of outer race
        self.BPFOFinal=float(self.BPFO)
        
        
        #print(BPFOFinal) 
        
        self.Bsf=((PD/(2*self.B_D))*(1-((self.B_D/self.P_D)*(math.cos(self.Angle)))**2))
        self.BSF=self.Bsf*self.Shaft_Speed #ball spin frequency
        self.BSFFinal=float(self.BSF)
        #print(BSFFinal) 

        #return BPFIFinal
        return  self.FTFFinal, self.BSFFinal, self.BPFOFinal, self.BPFIFinal  ###bearing theriotical fault frequency
    def Fault_range(self,inputvalue,lim): ## decides the ranges of fault frequencies
        rangelimit=inputvalue*lim
        self.Finalrange1=float(inputvalue+rangelimit)
        self.Finalrange2=float(inputvalue-rangelimit)
        return self.Finalrange1,self.Finalrange2
        
    
    
    


####on passing averaged fft values ,getting corresponding frequencies of amplitudes which are above the RMS value.
##fftavg=averaged fft values ####samplingFrequency of the sensor ###window size of the data.

    def FFT_calculations(self,fftavg,freqns,samplingFrequency,windowsize):
        lst1=fftavg  ####fftavg should be in pandas.core.series.Series
        self.rms =np.sqrt(np.mean(np.square(lst1))) #fft values are averaged
        self.Amplitude_rms_index = [list(lst1).index(i) for i in lst1 if i>3*self.rms] #checks for amplitudes index greater thn 3*rms
        #print(Amplitude_rms_index)
        self.HorizontAmplitudAbove_rms_values = [i for i in lst1 if i>3*self.rms] #checks for the amplitudes for the above index values
        #print(HorizontAmplitudAbove_rms_values)
        self.corres_frequency = [list(freqns)[i] for i in self.Amplitude_rms_index] #corresponding freqns of amplitudes greater than 3*rms
        #print(corres_frequency)
        return self.HorizontAmplitudAbove_rms_values,self.corres_frequency,self.rms #returns the ampltide,frqns, and rms 
    ##R1=bcf of FTF, R2=BCF of BSF ,samplingFrequency,
    ##lst=frequencies after 



    def FTF_analysis(self,input1,faultrange1,faultrange2): #checks whether ftf therotical frequencies  range matches the the frqns greater then rms obtained from the parser
        global result
        for x in input1: 
            
            if x>= faultrange1 and x<= faultrange2: #first harmonic check
                result= "first harmonic FTF fault"
                
                self.resultant.append(result)
            if x>= 2*faultrange1 and x<= 2*faultrange2:##second harmonic check
                result="2nd harmonic ftf fault"
                #print("2nd ftf")
                self.resultant.append(result)

            if x>= 3*faultrange1 and x<= 3*faultrange2: ##third harmonic check
                result="3rd harmonic FTF fault"
                #print("3rd ftf")
                self.resultant.append(result)

        return self.resultant   
                    
                        
    def BSF_analysis(self,input1,faultrange1,faultrange2): #checks whether bsf therotical frequencies  range matches the the frqns greater then rms obtained from the parser
        global result
        
        for x in input1:
            if x>= faultrange1 and x<= faultrange2: #first harmonic check
                result= "first harmonic bsf fault"
                #print("first bsf")
                self.resultant1.append(result)

            if x>= 2*faultrange1 and x<= 2*faultrange2:#second harmonic check
                result="2nd harmonic bsf fault"
                
                #print("2nd bsf")
                self.resultant1.append(result)

                #return (result)
            if x>= 3*faultrange1 and x<= 3*faultrange2: #third harmonic check
                result="3rd harmonic bsf fault"
                #print("3rd bsf")
                self.resultant1.append(result)
        return self.resultant1   

    def OUTERRACE_analysis(self,input1,faultrange1,faultrange2):#checks whether outerrace therotical frequencies  range matches the the frqns greater then rms obtained from the parser
        global result
        for x in input1:
            if x>= faultrange1 and x<= faultrange2: #first harmonic check
                result= "first harmonic outerrace fault"
                #print("first outerrace")
                self.resultant2.append(result)

            if x>= 2*faultrange1 and x<= 2*faultrange2: #second harmonic check
                result="2nd harmonic outerrace fault"
                #print("2nd outerrace")
                self.resultant2.append(result)

            if x>= 3*faultrange1 and x<= 3*faultrange2:#third harmonic check
                result="3rd harmonic outerrace fault"
                #print("3rd outerrace")
                self.resultant2.append(result)
        return self.resultant2   

                            
    def INNERRACE_analysis(self,input1,faultrange1,faultrange2): #checks whether innerrace therotical frequencies  range matches the the frqns greater then rms obtained from the parser
        global result
        for x in input1:
            if x>= faultrange1 and x<= faultrange2:   #first harmonic check
                result= "first harmonic innerrace fault"
                #print("first innerrace")
                self.resultant3.append(result)

            if x>= 2*faultrange1 and x<= 2*faultrange2: #second harmonic check
                result="2nd harmonic innerrace fault"
                #print("2nd innerrace")
                self.resultant3.append(result)

            if x>= 3*faultrange1 and x<= 3*faultrange2: #third harmonic check
                result="3rd harmonic innerrace fault" 
                #print("3rd innerrace")
                self.resultant3.append(result)
        return self.resultant3   



###it is used to append the accelerometer data
queue = deque()


###it is used to append epoch time of data
queue1 = deque()
     
#####function for handling log functions ####################
def on_log(client, userdata, level,buf):
    logging.basicConfig(filename='MQTT_bearinginfo.log', level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')
    logger = logging.getLogger()
    log_formatter = logging.Formatter('%(asctime)s%(levelname)s %(message)s')
    logHandler = handlers.RotatingFileHandler(str(Sensor_id)+'.log', maxBytes=1500, backupCount=5)
    logHandler.setFormatter(log_formatter)
    logHandler.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)
    logger.propagate=False


######function for receiving the disconnection messages ######### 
def on_disconnect(client, userdata, rc):
    logging.info("broker disconnected Returned code = "  +str(rc))
    client.connected_flag=False
    client.disconnect_flag=True  

######this fiunction connects the mqtt broker #####
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        # logging.info("MQTTconnection - connected OK")
    else:
        logging.info("Bad connection Returned code=",rc)#pgm of bearing fault

#######function for receiving the data from the broker, once message is recieved it is stored in queque
def on_message(client, userdata, msg):
    queue.append((json.loads(msg.payload.decode().split("$", 2)[0]))['f'])
    queue1.append(msg.payload.decode().split("$", 2)[2])


mqtt.Client.connected_flag=False 
mqtt.Client.bad_connection_flag=False #
client = mqtt.Client()  
client.on_connect = on_connect ####calling mqtt connection function
client.on_message = on_message ####calling data receiving function
client.on_disconnect=on_disconnect #####calling disconnection function
client.on_log=on_log #########calling log function for handling logs 

client.loop_start()
try:
    client.connect(brokeraddress,brokerport) #connect to broker
    while not client.connected_flag and not client.bad_connection_flag: #wait in loop
        time.sleep(4)

#####when there is no internet,the below message will log in to the logger. 
except: 
    logging.info("MQTTconnection -not established :please check")
    # print('cant connect')
    sys.exit("quit")

###for continuous loop running defined runflag as true
run_flag=True
# count=1
# array=[]
while run_flag:
    ###subscribing the topic #####
    client.subscribe(tagname, qos=1)
    sys_tme=datetime.datetime.now()
    ###epoch time of accelerometer data
    df=pd.DataFrame(list(queue1),columns=['time_epoch'])
    ###dropping duplicate values  
    df=df.drop_duplicates(keep='first',inplace=False)
    ###converting datatype of epochtime  to float
    df['time_epoch']=df['time_epoch'].astype(float)
    ###converting epoch time to datetime
    df['time'] =df['time_epoch'].map(lambda val: datetime.datetime.fromtimestamp(val).strftime('%Y-%m-%d %H:%M:%S.%f'))
    df['time']=pd.to_datetime(df['time'])
    FFT_list = set(tuple(x) for x in list(queue))
    FFT_list = [ list(x) for x in FFT_list]
    ####checking the length of fft data and if the length is greater than (nossamples/windowsize) ie nwindows performing fft averaging on the data.
    if len(FFT_list) >= nwindows:
        ###averaging the fft data
        average= [sum(e)/len(e) for e in zip(*FFT_list)]
        #print(average)
        #yf=(np.array(horizontFFT[0:len(average)]))
        #print(yf)
        xf = np.linspace(0.0, 1.0 / (2.0 * (1/samplingFrequency)), len(average))  #frequencies selection
        #print(xf)
        bearing=Bearing_analysis(nb,bd,p_d,angles,Shaftspeed,samplingFrequency,nsamp,windowsize,average)
        
        ftf,bsf,bpfo,bpfi=bearing.BCF() #bearing characterstics frequencies are calculated 
             
        ftf_range1,ftf_range2=bearing.Fault_range(ftf,float(lim_value)) #calculates the ranges of therotical  fft fault frqn
        #print(int(a1),int(a2))
        
        bsf_range1,bsf_range2=bearing.Fault_range(bsf,float(lim_value)) #calculates the ranges of therotical  bsf fault frqn
        #print(int(a3),int(a4))
        
        bpfo_range1,bpfo_range2=bearing.Fault_range(bpfo,float(lim_value)) #calculates the ranges of therotical  outerace fault frqn
    #print(int(a5),int(a6))
        
        bpfi_range1,bpfi_range2=bearing.Fault_range(bpfi,float(lim_value)) #calculates the ranges of therotical  innerrace fault frqn
        
    #print(int(a2),int(a1),int(a4),int(a3),int(a6),int(a5),int(a8),int(a7))

        amp,frqn,rms=bearing.FFT_calculations(average,xf,samplingFrequency,windowsize) #using the fft caluclation function calculates the frequencies corresponding amplitudes greater than 3*rms
    #print("freqn is",freqs)
        f1=bearing.FTF_analysis(frqn,int(ftf_range2),int(ftf_range1)) #checks whether ftf therotical frequencies  range matches the the frqns greater then rms obtained from the parser
        print(f1)
                #client.publish(pubishing_tag,f1)
        b1=bearing.BSF_analysis(frqn, int(bsf_range2),int(bsf_range1)) #checks whether bsf therotical frequencies  range matches the the frqns greater then rms obtained from the parser
        print(b1) 
                #client.publish(pubishing_tag,b1)
        i1=bearing.INNERRACE_analysis(frqn,int(bpfo_range2),int(bpfo_range1)) #checks whether innerace therotical frequencies  range matches the the frqns greater then rms obtained from the parser
        print(i1)
                #client.publish(pubishing_tag,i1)
        o1=bearing.OUTERRACE_analysis(frqn,int(bpfo_range1),int(bpfo_range2)) #checks whether outerace therotical frequencies  range matches the the frqns greater then rms obtained from the parser
        print(o1)
        
        #client.publish(pubishing_tag,o1)
        if sum([len(f1),len(b1),len(o1),len(i1)]) == 0: #checks whether list are empty 
            print("bearing is healthy")
        else:
            print("bearing has some problem")
        
        f1.clear()
        b1.clear() #clears all the list 
        i1.clear()
        o1.clear()
        queue.clear() #emptys the queue
        queue1.clear()                
    else:
        if len(FFT_list)>0:
            time_diff=(sys_tme-df['time'].iloc[-1]).total_seconds()#current sys-latest window
            # print('time dif',time_diff)
            
            if time_diff >60:
                # print('length is ',len(FFT_list),FFT_list)
                ###averaging the fft data
                average= [sum(e)/len(e) for e in zip(*FFT_list)]
                #print(average)
                #yf=(np.array(horizontFFT[0:len(average)]))
                #print(yf)
                xf = np.linspace(0.0, 1.0 / (2.0 * (1/samplingFrequency)), len(average))  #frequencies selection
                #print(xf)
                bearing=Bearing_analysis(nb,bd,p_d,angles,Shaftspeed,samplingFrequency,nsamp,windowsize,average)
                
                ftf,bsf,bpfo,bpfi=bearing.BCF(nb,bd,p_d,angles,Shaftspeed) #bearing characterstics frequencies are calculated 
                    
                ftf_range1,ftf_range2=bearing.Fault_range(ftf,float(lim_value)) #calculates the ranges of therotical  fft fault frqn
                #print(int(a1),int(a2))
                
                bsf_range1,bsf_range2=bearing.Fault_range(bsf,float(lim_value)) #calculates the ranges of therotical  bsf fault frqn
                #print(int(a3),int(a4))
                
                bpfo_range1,bpfo_range2=bearing.Fault_range(bpfo,float(lim_value)) #calculates the ranges of therotical  outerace fault frqn
            #print(int(a5),int(a6))
                
                bpfi_range1,bpfi_range2=bearing.Fault_range(bpfi,float(lim_value)) #calculates the ranges of therotical  innerrace fault frqn
                
            #print(int(a2),int(a1),int(a4),int(a3),int(a6),int(a5),int(a8),int(a7))

                amp,frqn,rms=bearing.FFT_calculations(average,xf,samplingFrequency,windowsize) #using the fft caluclation function calculates the frequencies corresponding amplitudes greater than 3*rms
            #print("freqn is",freqs)
                f1=bearing.FTF_analysis(frqn,int(ftf_range2),int(ftf_range1)) #checks whether ftf therotical frequencies  range matches the the frqns greater then rms obtained from the parser
                print(f1)
                        #client.publish(pubishing_tag,f1)
                b1=bearing.BSF_analysis(frqn, int(bsf_range2),int(bsf_range1)) #checks whether bsf therotical frequencies  range matches the the frqns greater then rms obtained from the parser
                print(b1) 
                        #client.publish(pubishing_tag,b1)
                i1=bearing.INNERRACE_analysis(frqn,int(bpfo_range2),int(bpfo_range1)) #checks whether innerace therotical frequencies  range matches the the frqns greater then rms obtained from the parser
                print(i1)
                        #client.publish(pubishing_tag,i1)
                o1=bearing.OUTERRACE_analysis(frqn,int(bpfo_range1),int(bpfo_range2)) #checks whether outerace therotical frequencies  range matches the the frqns greater then rms obtained from the parser
                print(o1)
                
                #client.publish(pubishing_tag,o1)
                if sum([len(f1),len(b1),len(o1),len(i1)]) == 0: #checks whether list are empty 
                    print("bearing is healthy")
                else:
                    print("bearing has some problem")
                
                f1.clear()
                b1.clear() #clears all the list 
                i1.clear()
                o1.clear()
                queue.clear() #emptys the queue
                queue1.clear() 
                        
                            # count+=1
    time.sleep(time_diff_btw_windows)
client.loop_stop()
####disconnecting the broker
client.disconnect()
