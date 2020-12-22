# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 17:29:19 2020
@author: Prashanth
"""
####libraries################# 
import numpy as np
#import os
#os.chdir(r"F:\Vegam_Office\Code") 
import pandas as pd
#import def_func as function
import time
import paho.mqtt.client as mqtt  #import the client1
from configparser import ConfigParser
import logging
import sys
from collections import deque
import logging.handlers as handlers
import datetime
import json
import def_func2 as function
# import MQTTLiveBearing_fault_Analysis_functions as bearing

###input parameters  is taken from configration parser##########
config_object = ConfigParser() 
config_object.read(r"D:/bearingtestingnew/userinfo2edited.ini")

####calling the userinfo object.
userinfo= config_object["user_info2"] 

###calling the server info object. 
serverinfo= config_object["server_config"] 

####calling the sensor info object.
sensor_info=config_object["sensor_info"] 
Bearing_info=config_object["bearing_info"] 

###accessing the broker address from the config file. 
Broker_address=serverinfo["broker_address"] 

###accessing the broker port from the config file. 
Broker_port=int(serverinfo["broker_port"]) 

###accessing the sensorid from the config file. 
Sensor_id=sensor_info["sensor_id"] 

###accessing the sampling frequency from the config file. 
samplingFrequency=int(sensor_info["samplingfrequency"]) 

### for subscribing the fft data accessing the tagname from the config file. 
Tag_name=sensor_info["tag_name"] 

### for publishing the alerts/faultlevel through mqtt accessing the publish tagname from the config file. 
pubishing_tag=sensor_info['publish_tag_name'] 

####accessing the mode of the sensor from the config file.
Mode =sensor_info["mode"] 

####accessing the number of samples of the sensor from the config file.
nsamp =int(sensor_info["no_samples"])

####accessing the window size of the sensor from the config file.
windowsize =int(sensor_info['window_size'])

power=int(userinfo["p"]) #power of motor

nwindows=int(nsamp/windowsize)
timetocompleteoneburst=int(nsamp)/int(samplingFrequency)
output=[]
##time difference between one burst to another
time_diff_btw_windows=timetocompleteoneburst/nwindows

#####################
###it is used to append the accelerometer data
queue = deque()

###############################################################################
###it is used to append epoch time of data
queue1 = deque()

###############################################################################
reference_rpm = 2000
maximum_rpm = reference_rpm / 60

###############################################################################
RPM = []
Max_value = []
Misalignment = []
Looseness = []
dataframe = pd.DataFrame()   
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
    client.connect(Broker_address, Broker_port) #connect to broker
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
    client.subscribe(Tag_name, qos=1)

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
        # avg_window = df.mean()###averaging of the windows 
        fft_val = average
        N = len(fft_val)
        yf= (np.array(fft_val[0:N]))
        freq_start_range = maximum_rpm - maximum_rpm * 0.8
        freq_end_range = maximum_rpm + maximum_rpm * 0.2
        xf = np.linspace(0.0, 1.0 / (2.0 * (1/samplingFrequency)), N//2)
        forrpm = function.ShaftSpeed_detection(freq_start_range, freq_end_range, yf)
        RPM.append(forrpm)
        ### Threshold at corresponding harmonics ####
        threshold_RMS = np.sqrt(np.mean(np.square(yf)))
        threshold = threshold_RMS*1
        second_thrsld = threshold*0.40
        third_thrsld = threshold*0.30
        #### List of data
        fft_series = pd.Series(yf, name=0)
        fft_DF = pd.DataFrame(abs(fft_series))
        freqlimit = 0.2
            
        sub_limits = function.start_end_array(freqlimit, forrpm)
    
        list_limits = pd.DataFrame(sub_limits, columns = ['start_range','End_range'])
               
        Max_value = function.limits(sub_limits, fft_DF)
              
        result =  function.harmonics_1x_2x_3x(Max_value[0], Max_value[1], Max_value[2],
                                  threshold, second_thrsld, third_thrsld)
        
        Misalignment.append(result)
        print(Misalignment)
        looseness_result = function.harmonics_greater_than_3x (Max_value[3], Max_value[7], 
                                              third_thrsld)
        Looseness.append(looseness_result)

