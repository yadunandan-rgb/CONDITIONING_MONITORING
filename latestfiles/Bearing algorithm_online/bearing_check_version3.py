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
import Mqtt_class_bearing_version2 as function

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

#Number of Rolling Element or Ball of bearing

NB=int(Bearing_info["NB"]) 

#Rolling Element or Ball Diameter of bearing
BD=float(Bearing_info["BD"]) 

#pitch circle diameter of the bearing 
PD=float(Bearing_info["PD"]) 

#Contact Angle
angle=int(Bearing_info["angle"]) 
shaftspeed=int(Bearing_info["shaftspeed"])
power=int(userinfo["p"]) #power of motor

#############derived variables from the config file #######################
###number of windows per burst
nwindows=int(nsamp/windowsize)
timetocompleteoneburst=int(nsamp)/int(samplingFrequency)
output=[]
##time difference between one burst to another
time_diff_btw_windows=timetocompleteoneburst/nwindows

#####################
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
    if len(FFT_list) >= nwindows:
        ###averaging the fft data
        
        bearing=function.BEARING_analysis(NB,BD,PD,angle,shaftspeed,samplingFrequency,nsamp,windowsize,FFT_list)
        
        f1,b1,i1,o1=bearing.BEARING_total()
        #client.publish(pubishing_tag,o1)
        if sum([len(f1),len(b1),len(i1),len(o1)]) == 0: #checks whether list are empty 
            print("bearing is healthy")
        else:
            print("bearing has some problem")

        f1.clear()
        b1.clear() #clears all the list 
        i1.clear()
        o1.clear()
                

    else:
        if len(FFT_list)>0:
            time_diff=(sys_tme-df['time'].iloc[-1]).total_seconds()#current sys-latest window
            # print('time dif',time_diff)
            
            if time_diff >60:
                # print('length is ',len(FFT_list),FFT_list)
                ###averaging the fft data
                average= [sum(e)/len(e) for e in zip(*FFT_list)]  
                print(average)  
                bearing=function.BEARING_analysis(NB,BD,PD,angle,shaftspeed,samplingFrequency,nsamp,windowsize,FFT_list)

                f1,b1,i1,o1=bearing.BEARING_total()
                #client.publish(pubishing_tag,o1)
                if sum([len(f1),len(b1),len(o1),len(i1)]) == 0: #checks whether list are empty 
                    print("bearing is healthy")
                else:
                    print("bearing has some problem")

                f1.clear()
                b1.clear() #clears all the list 
                i1.clear()
                o1.clear()
                        
    time.sleep(time_diff_btw_windows)
client.loop_stop()
####disconnecting the broker
client.disconnect()

