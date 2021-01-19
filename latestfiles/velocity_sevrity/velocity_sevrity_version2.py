
#!python3
import paho.mqtt.client as mqtt  #import the client1
import time
from configparser import ConfigParser #imports the library need to take inputs from configration file
import sys
from collections import deque
import logging.handlers as handlers   #imports the library need to give logs for coustmer
import pandas as pd   #imports the pandas library
import numpy as np  #imports the numpy library
import datetime  #imports the datetime library

####inputs are taken from configration file
config_object = ConfigParser()
config_object.read("userinfo2.ini")
userinfo2= config_object["user_info2"]
serverinfo= config_object["server_config"]
sensor_info=config_object["sensor_config"]
Broker_address=serverinfo["broker_address"]
#Broker_address='176.9.145.238'
classinfo= config_object["class_info"]
Broker_port=int(serverinfo["broker_port"])
Sensor_id=sensor_info["sensor_id"]
Tag_name=sensor_info["tag_name"]
Tag_name2=sensor_info["tag_name2"]
Window_size=int(sensor_info["windowsize"])
power=int(userinfo2["p"])
Power_range1=int(classinfo["power_range1"]) 
Power_range2=int(classinfo["power_range2"]) 
Power_range3=int(classinfo["power_range3"]) 
 
###velocity iso table is selected
velocity_iso=pd.read_csv(r'C:\Users\ABC\OneDrive\Pictures\Screenshots\New folder\velocity_severity_02_07_2020.csv')
queue=deque()
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
    logging.info("broker disconnected Returned code = "  +str(rc))#whenever the broker gets disconnected it returns Returned code in a logfile
    client.connected_flag=False#set flag
    client.disconnect_flag=True # set flag
###whenever the broker gets connected then flag value is changed
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        # logging.info("MQTTconnection - connected OK")
    else:
        logging.info("Bad connection Returned code=",rc)#message is logged in log file
###whenever client is connected and their is a message then message is appended to queque
def on_message(client, userdata, msg):
    # global queue
    queue.append(msg.payload.decode().split("$")) #message is appended to queque and processed to proper formate

####checking the class of machine  ####
####fun to check the class of machine ###
def machineclass(power): ####power in KW
    if power < Power_range1:
        classofmotor='class1'   ##checks the class the range
    elif power in range(Power_range1,Power_range2): #####range values are in kW
        classofmotor='class2'
    elif power in range(Power_range2,Power_range3):
        classofmotor='class3'
    elif power > Power_range3:
        classofmotor='class4'
    return classofmotor

#####checking velocity severity level
def velocity_severity(Vvalue,velocity_iso,motorclass):
    vel_value=Vvalue
    velocity_iso_val=np.array(velocity_iso['Vrms_mm/s']) ##velocity iso standard values from csv are stored in velocity_iso_val
    diff_val=np.abs(velocity_iso_val-vel_value) ##difference of velocity values 
    iso_index=list(diff_val).index(min(diff_val)) ##index of velocity iso values
    severityLevel=velocity_iso[motorclass][iso_index] 
    return severityLevel

##calling the function to check the class of machine ###

mqtt.Client.connected_flag=False #flags gets updated
mqtt.Client.bad_connection_flag=False #
client = mqtt.Client()
client.on_log=on_log                             ###functions are called
client.on_message = on_message
client.on_connect = on_connect  
client.on_disconnect=on_disconnect


client.loop_start()
try:
    client.connect(Broker_address, Broker_port) #connect to broker
    while not client.connected_flag and not client.bad_connection_flag: #wait in loop
        time.sleep(4)
except:
    logging.info("MQTTconnection -not established :please check") #message is sent to loglife
    #print('cant connect')
    sys.exit("quit")

classofmotor=machineclass(power)  #machine class function is called
run_flag=True
count=1
ary=[]
while run_flag:
    msg="test message"+str(count)
    client.subscribe(Tag_name, qos=1)  #velocity values are subscribed through tag_nmae topic
    #print("length:",+len(queue))
    df = pd.DataFrame(list(queue),columns=['value','var','time_epoch']) #message is converted to dataframe
    df=df.drop_duplicates(keep='first',inplace=False)
    df['time_epoch']=df['time_epoch'].astype(float)
    df['time'] =df['time_epoch'].map(lambda val: datetime.datetime.fromtimestamp(val).strftime('%Y-%m-%d %H:%M:%S.%f'))
    #print("lengthdf:",+len(df))
    if len(df)>=Window_size:
        vel_value=np.mean(df['value'].astype(float))
        Sevrity_level=velocity_severity(vel_value,velocity_iso,classofmotor)#sevrity level is determined
        #print(vel_value)
        #print(Slevel)
        client.publish("Tag_name2",Sevrity_level)  #level of sevrity is published to vmaint using the mqtt topic 
        queue.clear()
        
    count+=1
    #print("count:"+ str(count))
    time.sleep(1.2)
    
client.loop_stop()

client.disconnect()
