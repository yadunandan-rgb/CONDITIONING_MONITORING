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

os.chdir(r'/home/vegam/sortedfolder/geardatawthcode/csv')
#########files path ###
path=r'/home/vegam/sortedfolder/geardatawthcode/csv'
ac=os.listdir(path)
#####inputs from configuration file #######
config_object = ConfigParser()
config_object.read(r'/home/vegam/sortedfolder/geardatawthcode/mqttdatapreprocess.ini')
userinfo= config_object["user_info"]
serverinfo= config_object["server_config"]
Broker_address=serverinfo["broker_address"]
Broker_port=int(serverinfo["broker_port"])
samplingfrequency=int(userinfo["samplingfrequency"])
#publishtag=serverinfo['publishtagname']
#################################################################3
#######broker connection ############
#client = mqtt.Client()
#client.connect(Broker_address,Broker_port)
####current system time ######
t=datetime.datetime.now()
milliseconds=1000/samplingfrequency
#######
for n in range(len(ac)):
    df=pd.read_csv(path+'/'+ac[n])
    bd=[]
    bc=[]
    aa=[]
    bb=[]
    for i in range(len(df)):
        #bd.append(mendeley_data['Channel_2'].iloc[i])
        bc.append(df['acc'].iloc[i])
        t= t + datetime.timedelta(milliseconds=milliseconds)
        unxtime=t.timestamp()
        unxtime=round(unxtime,3)
        result=str(bc[i])+'$T$'+str(unxtime)
        print(result)
        #client.publish(publishtag,result)
        aa.append(t)
        bb.append(unxtime)
    
    df2=pd.DataFrame(list(zip(bc,aa,bb)),columns=['acc','datetime','utime'])
    df2.to_csv('withtimestamp_'+str(ac[n]))

    
        



