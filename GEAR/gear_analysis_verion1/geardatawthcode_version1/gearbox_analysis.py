
#!python3
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
import math 
from numpy import mean, sqrt, square, arange

config_object = ConfigParser()
config_object.read("gearboxinput.ini")
userinfo2= config_object["user_info2"]
serverinfo= config_object["server_config"]
sensor_info=config_object["sensor_config"]
gear_info=config_object["gear_config"]
Broker_address=serverinfo["broker_address"]

# Aunthentication jsw
# Username=sensor_info["user_name"]
# Password=sensor_info["password"]

Broker_port=int(serverinfo["broker_port"])
Sensor_id=sensor_info["sensor_id"]

Tag_name=sensor_info["tag_name"]

no_samples = int(sensor_info["no_samples"])
window_samples =int(sensor_info["window_samples"])
Speed_of_gear =int(gear_info["speed_of_gear"])
No_of_teeth=int(gear_info["number_of_teeth"])
Sampling_freqn=int(sensor_info["sampling_freqn"])
# Mode = sensor_info["mode"]
#power=int(userinfo2["p"]) 
power=int(userinfo2["p"])
frequency_of_gear=float(Speed_of_gear/60)
GMFF=float(frequency_of_gear*No_of_teeth)
GMFF2=float(2*GMFF)
GMFF3=float(3*GMFF)
T = float(1 / Sampling_freqn)
# no_samples = 4096
# window_samples = 512
queue=deque()
queue1 = deque()

def on_log(client, userdata, level,buf):
    # logging.basicConfig(filename='MQTT_ananda.log', level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')
    logger = logging.getLogger()
    log_formatter = logging.Formatter('%(asctime)s%(levelname)s %(message)s')
    logHandler = handlers.RotatingFileHandler(str(Sensor_id)+'.log', maxBytes=1500, backupCount=5)
    logHandler.setFormatter(log_formatter)
    logHandler.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)
    logger.propagate=False

def on_disconnect(client, userdata, rc):
    logging.info("broker disconnected Returned code = "  +str(rc))
    client.connected_flag=False
    client.disconnect_flag=True  

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        # logging.info("MQTTconnection - connected OK")
    else:
        logging.info("Bad connection Returned code=",rc)#pgm of bearing fault

def on_message(client, userdata, msg):
    queue.append((json.loads(msg.payload.decode().split("$", 2)[0]))['f'])
    queue1.append(msg.payload.decode().split("$", 2)[2])


mqtt.Client.connected_flag=False 
mqtt.Client.bad_connection_flag=False #
client = mqtt.Client()
client.on_log=on_log
client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect=on_disconnect


client.loop_start()
try:
    client.connect(Broker_address, Broker_port) #connect to broker
    while not client.connected_flag and not client.bad_connection_flag: #wait in loop
        time.sleep(4)
except:
    logging.info("MQTTconnection -not established :please check")
    print('cant connect')
    sys.exit("quit")

import threading 


tottal_window = no_samples//window_samples
run_flag=True
count=1
array=[]
while run_flag:
    msg="test message"+str(count)
    client.subscribe(Tag_name, qos=1)
    FFT_list = list(queue)
    sys_tme=datetime.datetime.now()
    df = pd.DataFrame(list(queue1),columns=['time_epoch'])
    df=df.drop_duplicates(keep='first',inplace=False)
    df['time_epoch']=df['time_epoch'].astype(float)
    df['time'] =df['time_epoch'].map(lambda val: datetime.datetime.fromtimestamp(val).strftime('%Y-%m-%d %H:%M:%S.%f'))
    df['time']=pd.to_datetime(df['time'])
    if len(FFT_list)>0 and len(FFT_list)<(tottal_window+1):
        time_diff=(sys_tme-df['time'].iloc[-1]).total_seconds()
        if time_diff >60:
            
            average= [sum(e)/len(e) for e in zip(*FFT_list)]
            #print(len(average),average)
            rms =sqrt(mean(square(average)))
            print(rms)
            count_freq_greater = len([i for i in average if i > 1.2*rms]) ####count of values which are greater than 1.2 times the RMS
            sorted_list=sorted([(x,i) for (i,x) in enumerate(average)], reverse=True )[:count_freq_greater]  ######correspondig frequency and amplitudes greater than 1.2xRMS 
            data_list=pd.DataFrame(sorted_list,columns=['amplitude','Frequency'])
            frqn_lst=data_list['Frequency']
            new_list=[]
            new_list.append(frqn_lst)
            print(new_list)
            for element in frqn_lst:
                if element in range(int(GMFF-8),int(GMFF+8)):
                    print("their is fault 1st harmonic in gear")
                    if element in range(int(GMFF2-8),int(GMFF2+8)):
                        print("their is fault in 2nd harmonic of gear")
                        if element in range(int(GMFF3-8),int(GMFF3+8)):
                            print("their is fault in gear")
            
            
                    
            queue.clear()
            queue1.clear()
        # count+=1

# Check by removing below loop in continuous mode
    if len(FFT_list)>=tottal_window:
        # print('',len(FFT_list),FFT_list)
        average= [sum(e)/len(e) for e in zip(*FFT_list)]
        rms =sqrt(mean(square(average)))
        print(rms)
        count_freq_greater = len([i for i in average if i > 1.2*rms]) ####count of values which are greater than 1.2 times the RMS
        sorted_list=sorted([(x,i) for (i,x) in enumerate(average)], reverse=True )[:count_freq_greater]  ######correspondig frequency and amplitudes greater than 1.2xRMS 
        data_list=pd.DataFrame(sorted_list,columns=['amplitude','Frequency'])
        frqn_lst=data_list['Frequency']
        new_list=[]
        new_list.append(frqn_lst)
        print(new_list)
        for element in frqn_lst:
            if element in range(int(GMFF-8),int(GMFF+8)):
                print("their is fault 1st harmonic in gear")
                if element in range(int(GMFF2-8),int(GMFF2+8)):
                    print("their is fault in 2nd harmonic of gear")
                    if element in range(int(GMFF3-8),int(GMFF3+8)):
                        print("their is fault in gear")
       
        queue.clear()
        queue1.clear()
    count+=1
    time.sleep(1.2)

    

client.loop_stop()

client.disconnect()