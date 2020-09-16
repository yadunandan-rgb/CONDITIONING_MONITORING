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

####inputs are taken from configration file

config_object = ConfigParser()
config_object.read(r"/home/vegam/Downloads/userinfo2edit_anand.ini")
userinfo2= config_object["user_info2"]
serverinfo= config_object["server_config"]
sensor_info=config_object["sensor_config"]
Broker_address=serverinfo["broker_address"]

#Broker_address='176.9.145.238'

# Aunthentication jsw
# Username=sensor_info["user_name"]
# Password=sensor_info["password"]

Broker_port=int(serverinfo["broker_port"])
Sensor_id=sensor_info["sensor_id"]

Tag_name=sensor_info["tag_name"]

no_samples = int(sensor_info["no_samples"])
window_samples =int(sensor_info["window_samples"])
samplingfrequency = int(sensor_info['samplingfrequency'])
# Mode = sensor_info["mode"]
power=int(userinfo2["p"]) 


# no_samples = 4096
# window_samples = 512
queue=deque()
queue1 = deque()

#### the messages are logged using on_log function, and messages are saved in log_file

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


###whenever the broker gets disconnected the message is send to coustmer using this function

def on_disconnect(client, userdata, rc):
    logging.info("broker disconnected Returned code = "  +str(rc))
    client.connected_flag=False
    client.disconnect_flag=True  

###whenever the broker gets connected then flag value is changed

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        # logging.info("MQTTconnection - connected OK")
    else:
        logging.info("Bad connection Returned code=",rc)#pgm of bearing fault

###whenever client is connected and their is a message then message is appended to queque


def on_message(client, userdata, msg):
    queue.append((json.loads(msg.payload.decode().split("$", 2)[0]))['f'])
    queue1.append(msg.payload.decode().split("$", 2)[2])

##calling the function to check the class of machine ###

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

def averageoflist(FFT_list):
    # print('Burstlength is in Burst mode is ',len(FFT_list),FFT_list)
    averaged_fft_list= [sum(e)/len(e) for e in zip(*FFT_list)]
    # print('Burst modeAveraged list length',len(average),average)
    return averaged_fft_list
################################################################################################
# FFT_list is a queue, all fft lists will fill this queue and in averaged_fft_list averaged fft list 
# will be there.
############################




tottal_window = no_samples//window_samples
timetocompleteoneburst=no_samples/(samplingfrequency)
time_diff_btw_windows=timetocompleteoneburst/tottal_window
run_flag=True
count=1
array=[]
array1 = []
list1=[]
while run_flag:
    msg="test message"+str(count)
    client.subscribe(Tag_name, qos=1)
    FFT_list = list(queue)
    sys_tme=datetime.datetime.now()
    timedataframe = pd.DataFrame(list(queue1),columns=['time_epoch'])
    timedataframe=timedataframe.drop_duplicates(keep='first',inplace=False)
    timedataframe['time_epoch']=timedataframe['time_epoch'].astype(float)
    timedataframe['time'] =timedataframe['time_epoch'].map(lambda val: datetime.datetime.fromtimestamp(val).strftime('%Y-%m-%d %H:%M:%S.%f'))
    timedataframe['time']=pd.to_datetime(timedataframe['time'])
    if len(FFT_list)>0:
        time_diff=(sys_tme-timedataframe['time'].iloc[-1]).total_seconds()
        if time_diff >=60:
            averageoflist(FFT_list)
            timedataframe2=timedataframe['time']
        #print(timedataframe2)
            startandend_time=timedataframe2.iloc[[0, -1]]
            startandend_time= startandend_time.astype(str)
            print(startandend_time)
            v = startandend_time.to_numpy()
            list1.append(v)
            str1 = ','.join(str(e) for e in list1)
            client.publish("ABC1234567/time_stamp",str1) 
  
            queue.clear()
            queue1.clear()
            list1.clear()
    if len(FFT_list)>=tottal_window:
        averageoflist(FFT_list)
        #print(timedataframe)
        #timedataframe.to_csv("/media/vegam/NIKU/output.csv",index=False)
        #print(timedataframe['time'])
        timedataframe2=timedataframe['time']
        #print(timedataframe2)
        startandend_time=timedataframe2.iloc[[0, -1]]
        startandend_time= startandend_time.astype(str)
        print(startandend_time)
        v = startandend_time.to_numpy()
        list1.append(v)
        #list1.append(startandend_time)
        str1 = ','.join(str(e) for e in list1)
        client.publish("ABC1234567/time_stamp",str1) 

        queue.clear()
        queue1.clear()
        list1.clear()

    count+=1
    time.sleep(0.9*time_diff_btw_windows)

    

client.loop_stop()

client.disconnect()
