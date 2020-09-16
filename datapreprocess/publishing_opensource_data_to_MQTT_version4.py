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
t=datetime.datetime.now()
milliseconds=1000/samplingfrequency
#######connecting to broker ############
client = mqtt.Client()
client.connect(Broker_address,Broker_port)
####current system time ######
t=datetime.datetime.now()
milliseconds=1000/samplingfrequency
start=time.time()
########loop for the list of files in the directory
for n in range(len(ac)):
    # reading data one by one
    mendeley_data=pd.read_csv(path+'/'+ac[n])
    ###defining the empty list 
    bd=[]
    bc=[]
    aa=[]
    for i in range(len(mendeley_data)):
        bd.append(mendeley_data['Channel_2'].iloc[i])
        bc.append(mendeley_data['Channel_1'].iloc[i])
        ###adding milliseconds to the datetime
        t=t + datetime.timedelta(milliseconds=milliseconds)
        ###converting datetime to epoch format
        millis=(time.mktime(t.timetuple())*1000+t.microsecond)/1000
        aa.append(millis)
        ####creating publishing format data
        result=str(bc[i])+'$T$'+str(millis)
        print(result)
        ####publishing the data to mqtt
        # client.publish(publishtag,result)
        ####saving each data file to the local machine with timestamp data
    elapsed=time.time()-start

    mendleydatawithtstamp=pd.DataFrame(list(zip(bc,bd,aa)),columns=['Channel_1','Channel_2','utime'])

