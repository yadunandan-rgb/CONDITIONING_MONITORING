
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

config_object = ConfigParser()
config_object.read("userinfo2.ini")
userinfo2= config_object["user_info2"]
serverinfo= config_object["server_config"]
sensor_info=config_object["sensor_config"]
Broker_address=serverinfo["broker_address"]
#Broker_address='176.9.145.238'
Broker_port=int(serverinfo["broker_port"])
Sensor_id=sensor_info["sensor_id"]
Tag_name=sensor_info["tag_name"]
#Tag_name2=sensor_info["tag_name2"]
Window_size=int(sensor_info["windowsize"])
power=int(userinfo2["p"]) 

viso=pd.read_csv(r'C:\Users\ABC\OneDrive\Pictures\Screenshots\New folder\velocity_severity_02_07_2020.csv')
queue=deque()

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
    # global queue
    queue.append(msg.payload.decode().split("$"))

####checking the class of machine  ####
####fun to check the class of machine ###
def mclass(power): ####power in KW
    if power < 15:
        classofmotor='class1'
    elif power in range(15,75): #####range values are in kW
        classofmotor='class2'
    elif power in range(75,10000):
        classofmotor='class3'
    elif power > 10000 :
        classofmotor='class4'
    return classofmotor

#####checking velocity severity level
def velocity_severity(Vvalue,viso,motorclass):
    vel_value=Vvalue
    viso_val=np.array(viso['Vrms_mm/s']) ##velocity iso standard values
    diff_val=np.abs(viso_val-vel_value) ##difference of velocity values 
    iso_index=list(diff_val).index(min(diff_val)) ##index of velocity iso values
    severityLevel=viso[motorclass][iso_index] 
    return severityLevel

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
    #print('cant connect')
    sys.exit("quit")

classofmotor=mclass(power)  
run_flag=True
count=1
ary=[]
while run_flag:
    msg="test message"+str(count)
    client.subscribe(Tag_name, qos=1)
    #print("length:",+len(queue))
    df = pd.DataFrame(list(queue),columns=['value','var','time_epoch'])
    df=df.drop_duplicates(keep='first',inplace=False)
    df['time_epoch']=df['time_epoch'].astype(float)
    df['time'] =df['time_epoch'].map(lambda val: datetime.datetime.fromtimestamp(val).strftime('%Y-%m-%d %H:%M:%S.%f'))
    #print("lengthdf:",+len(df))
    if len(df)>=Window_size:
        vel_value=np.mean(df['value'].astype(float))
        Slevel=velocity_severity(vel_value,viso,classofmotor)
        #print(vel_value)
        #print(Slevel)
        client.publish("Tag_name2",Slevel)
        queue.clear()
        
    count+=1
    #print("count:"+ str(count))
    time.sleep(1.2)
    
client.loop_stop()

client.disconnect()