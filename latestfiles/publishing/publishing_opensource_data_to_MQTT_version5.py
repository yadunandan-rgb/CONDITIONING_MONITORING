##libraries
import os
import pandas as pd
import time
import datetime
import paho.mqtt.client as mqtt
from configparser import ConfigParser

####working directory ####
os.chdir("D:\expirement")
#########files path ###
path=r'D:\expirement\downsample2400'
####listing out the files
ac=os.listdir(path)
#####inputs from configuration file #######
config_object = ConfigParser()
config_object.read(r'D:\expirement\mqttdatapreprocess.ini')
userinfo= config_object["user_info"] 
serverinfo= config_object["server_config"]
##accessing broker address,broker port ,sampling frequency and publishing tag from the config file
Broker_address=serverinfo["broker_address"]
Broker_port=int(serverinfo["broker_port"])
samplingfrequency=int(userinfo["samplingfrequency"])
publishtag=serverinfo['publishtagname']
#################################################################3
t=datetime.datetime.now()
milliseconds=1/samplingfrequency
#######connecting to broker ############
client = mqtt.Client()
client.connect(Broker_address,Broker_port)
####current system time ######
t=datetime.datetime.now()
milliseconds=1000/samplingfrequency
recordstarttime=[]
recordendtime=[]
filename=[]
fileuploadedtime=pd.DataFrame()
########loop for the list of files in the directory
for n in range(len(ac)):
    # reading data one by one
    start=time.time()
    mendeley_data=pd.read_csv(path+'/'+ac[n])
    ###defining the empty list 
    #bd=[]
    bc=[]
    aa=[]
    res=[]
    count=0
    for i in range(len(mendeley_data)):
        #bd.append(mendeley_data['Channel_2'].iloc[i])
        bc.append(mendeley_data['v'].iloc[i])
        ###adding milliseconds to the datetime              
        t=t + datetime.timedelta(milliseconds=milliseconds)        
        ###converting datetime to epoch format
        millis=int(time.mktime(t.timetuple())*1000+t.microsecond/1000)/1000
        aa.append(millis)
        ####creating publishing format data
        result=str(bc[i])+'$T$'+str(millis)
        res.append(result)
        ####publishing the data to mqtt
        client.publish(publishtag,result)
        print(result)
        count +=1
        ####saving each data file to the local machine with timestamp data
    endtime=time.time()
    recordstarttime.append(start)
    recordendtime.append(endtime)
    filename.append(ac[n])
    mendleydatawithtstamp=pd.DataFrame(list(zip(bc,aa)),columns=['v','utime'])
    mendleydatawithtstamp.to_csv(ac[n],index=False)
    # res.to_csv('mendeleytestfile.txt',header=None,index=None)

fileuploadedtime['filename']=filename 
fileuploadedtime['starttime']=recordstarttime
fileuploadedtime['endtime']=recordendtime

fileuploadedtime.to_csv("Data_uploaded_timeo.csv",index=False)
