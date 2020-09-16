# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 15:37:54 2020

@author: Chethan
"""
import os
import pandas as pd
import time
import datetime
import paho.mqtt.client as mqtt
from configparser import ConfigParser

os.chdir("/media/vegam/NIKU/mendelesdata/csv")
#########files path ###
path=r'/media/vegam/NIKU/mendelesdata/csv'
ac=os.listdir(path)
#####inputs from configuration file #######
config_object = ConfigParser()
config_object.read(r'/media/vegam/NIKU/mendelesdata/mqttdatapreprocess.ini')
userinfo= config_object["user_info"]
serverinfo= config_object["server_config"]
Broker_address=serverinfo["broker_address"]
Broker_port=int(serverinfo["broker_port"])
samplingfrequency=int(userinfo["samplingfrequency"])
publishtag=serverinfo['publishtagname']
#################################################################3
#######broker connection ############
client = mqtt.Client()
client.connect(Broker_address,Broker_port)
####current system time ######
t=datetime.datetime.now()
milliseconds=1000/samplingfrequency
#######
for n in range(len(ac)):
    mendeley_data=pd.read_csv(path+'/'+ac[n])
    bd=[]
    bc=[]
    aa=[]
    bb=[]
    for i in range(len(mendeley_data)):
        bd.append(mendeley_data['Channel_2'].iloc[i])
        bc.append(mendeley_data['Channel_1'].iloc[i])
        t= t + datetime.timedelta(milliseconds=milliseconds)
        unxtime=t.timestamp()
        unxtime=round(unxtime,3)
        result=str(bc[i])+'$T$'+str(unxtime)
        print(result)
        client.publish(publishtag,result)
        aa.append(t)
        bb.append(unxtime)
    
    mendleydatawithtstamp=pd.DataFrame(list(zip(bc,bd,aa,bb)),columns=['Channel_1','Channel_2','datetime','utime'])
    mendleydatawithtstamp.to_csv('withtimestamp_'+str(ac[n]))

    
        



