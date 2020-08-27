
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

config_object = ConfigParser()
config_object.read(r"/content/1forPhase_UUID_added.ini")
userinfo2= config_object["user_info2"]
serverinfo= config_object["server_config"]
sensor_info=config_object["sensor_config"]
Broker_address=serverinfo["broker_address"]



Broker_port=int(serverinfo["broker_port"])
Sensor_id=sensor_info["sensor_id"]

Tag_name=sensor_info["tag_name"]

no_samples = int(sensor_info["no_samples"])
window_samples =int(sensor_info["window_samples"])
samplingfrequency  = int(sensor_info['samplingfrequency'])

tagX_name = (sensor_info['uuidX'])
tagY_name = (sensor_info['uuidY'])
power=int(userinfo2["p"]) 



queue=deque()
raw_lists = []
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
        client.connected_flag=True 
    else:
        logging.info("Bad connection Returned code=",rc)#pgm of bearing fault

def on_message(client, userdata, msg):
    queue.append(json.loads(msg.payload.decode()))


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
import time

def phasefind(dataframe54,dataframe55):
    if len(dataframe54)!=len(dataframe55):
        a = list(dataframe55['v'])
        b = list(dataframe54['v'])
        difference = abs(len(a)-len(b))
        if len(a)>len(b):
            a = a[: -difference or None]  #to delete last n elemenets
            b = b
        elif len(b)>len(a):
            b = b[: -difference or None] 
            a = a
        amplitudeX =  a 
        # print('length is ',len(amplitudeX))
        amplitudeY =  b 
        # print('length is ',len(amplitudeY))
        c = dot(amplitudeX,amplitudeY)/norm(amplitudeX)/norm(amplitudeY)
        angle = arccos(clip(c, -1, 1)) 
        print('angle in degree',((angle*360)/(2*3.14)))


tottal_window = no_samples//window_samples
timetocompleteoneburst=no_samples/(samplingfrequency)
time_diff_btw_windows=timetocompleteoneburst/tottal_window
run_flag=True
count=1
content92554 = deque()
content92555 = deque()
timeout = 6000
while run_flag:
    msg="test message"+str(count)
    client.subscribe(tagX_name, qos=1)
    client.subscribe(tagY_name, qos=1)
    raw_uuid_list = list(queue)

    for i in range(len(raw_uuid_list)):
        if raw_uuid_list[i]['u'] == 92555:
            content92555.append(raw_uuid_list[i])
        elif raw_uuid_list[i]['u'] == 92554:
            content92554.append(raw_uuid_list[i])
    dataframe54 = pd.DataFrame(list(content92554),columns=['u','v','t'])
    dataframe55 = pd.DataFrame(list(content92555),columns=['u','v','t'])
    sys_tme=datetime.datetime.now()
    dataframe54.to_csv(str(count)+"duplicate_values_in_queue.csv",index=False)
    dataframe54=dataframe54.drop_duplicates(keep='first',inplace=False)
    dataframe55.to_csv(str(count)+"duplicate_values_in_queue.csv",index=False)
    dataframe55=dataframe55.drop_duplicates(keep='first',inplace=False)
    dataframe55['t']=(dataframe55['t']).astype(float)
    dataframe55['time'] =dataframe55['t'].map(lambda val: datetime.datetime.fromtimestamp(val/1e3).strftime('%Y-%m-%d %H:%M:%S.%f'))
    dataframe55['time']=pd.to_datetime(dataframe55['time'])
    if len(dataframe55) > 0:
        time_diff=(sys_tme - dataframe55['time'].iloc[-1]).total_seconds()
        if time_diff > 60:
            phasefind(dataframe54,dataframe55)
            queue.clear()
            content92554.clear()
            content92555.clear()
            
    if len(dataframe54)>=10000 and len(dataframe55)>=10000:
        phasefind(dataframe54,dataframe55)
        queue.clear()
        content92554.clear()
        content92555.clear()
    count+=1
  
    time.sleep(0.9*time_diff_btw_windows)

client.loop_stop()
client.disconnect()