##libraries
import os
import pandas as pd
import time
import datetime
import paho.mqtt.client as mqtt
from configparser import ConfigParser

####working directory ####
os.chdir("U:/Vegam_resource/Data")
#########files path ###
path=r'U:/Vegam_resource/Data/Mendeley'
####listing out the files
ac=os.listdir(path)
#####inputs from configuration file #######
config_object = ConfigParser()
config_object.read(r'C:/Users/Chethan/Downloads/mqttdatapreprocess.ini')
userinfo= config_object["user_info"] 
serverinfo= config_object["server_config"]
##accessing broker address,broker port ,sampling frequency and publishing tag from the config file
Broker_address=serverinfo["broker_address"]
Broker_port=int(serverinfo["broker_port"])
samplingfrequency=int(userinfo["samplingfrequency"])
publishtag=serverinfo['publishtagname']
#################################################################3
#######connecting to broker ############
client = mqtt.Client()
client.connect(Broker_address,Broker_port)
########loop for the list of files in the directory
for n in range(len(ac)):
    # reading data one by one
    mendeley_data=pd.read_csv(path+'/'+ac[n])
    ###defining the empty list 
    bd=[]
    bc=[]
    aa=[]
    bb=[]
    for i in range(len(mendeley_data)):
        ###appending channel1,channel2 and unix timestamp of the data
        bd.append(mendeley_data['Channel_2'].iloc[i])
        bc.append(mendeley_data['Channel_1'].iloc[i])
        ###reading time in epoch format 
        millis = int(round(time.time() * 1000))/1000
        aa.append(millis)
        ####creating publishing format data
        result=str(bc[i])+'$T$'+str(millis)
        ###publishing the data to mqtt
        client.publish(publishtag,result)
        time.sleep(1000/1600)
    
    ####saving each data file to the local machine with timestamp data
    mendleydatawithtstamp=pd.DataFrame(list(zip(bc,bd,aa)),columns=['Channel_1','Channel_2','utime'])
    # mendleydatawithtstamp.to_csv('withtimestamp_'+str(ac[n]))


