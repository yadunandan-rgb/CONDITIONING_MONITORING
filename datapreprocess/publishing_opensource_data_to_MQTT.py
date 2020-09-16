import os
import pandas as pd
import time
import datetime
import paho.mqtt.client as mqtt
from configparser import ConfigParser

os.chdir("U:/Vegam_resource/Data")
#########files path ###
path=r'U:/Vegam_resource/Data/Mendeley'
ac=os.listdir(path)
#####inputs from configuration file #######
config_object = ConfigParser()
config_object.read(r'C:/Users/Chethan/Downloads/mqttdatapreprocess.ini')
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
    ####60 represents seconds ###1600 represents number of samples per seconds
    minutestaken=int(len(mendeley_data)/(60*samplingfrequency))
    startingrow=0 ####to access first row of the data
    endrow=samplingfrequency
    mendleydatawithtstamp=pd.DataFrame()
    for i in range(minutestaken):
        print(i)# represents minutes
        for j in range(60): ### represents seconds
            data=mendeley_data[startingrow:endrow]
            aa=[]
            bb=[]
            for k in range(1600): ###number of samples per second
                df=data['Channel_1'].iloc[k]
                t= t + datetime.timedelta(milliseconds=milliseconds)
                unxtime=t.timestamp()
                unxtime=round(unxtime,3)
                result=str(df)+'$T$'+str(unxtime)
                client.publish(publishtag,result)
                aa.append(t)
                bb.append(unxtime)
                # print(result)
                print(k)
                # utc_seconds +=(1000/1600) #one second
            data['datetime']=aa 
            data['utime']=bb 
            mendleydatawithtstamp.append(data)
            startingrow=endrow
            endrow +=endrow
            
            
            mendleydatawithtstamp.to_csv('withtimestamp_'+str(ac[i]))


    


data.to_csv("mendeley_sample.csv",index=False)

# time.time()
# time.strftime("%a, %d %b %Y %H:%M:%S.%f %Z", time.localtime(1599802030.34302))
#created_timestamp = int((datetime.datetime.now() - datetime.datetime(1970,1,1)).total_seconds())


# date = datetime.datetime(2003,8,1,12,4,5)
# for i in range(5): 
#     date += datetime.timedelta(days=1)
#     print(date) 


# datetime.utcnow().timestamp()
# from datetime import datetime
# t=datetime.datetime.now()
# datetime.utcnow().timestamp()
# t.timestamp()
# datetime.fromtimestamp(t)
# datetime.datetime(2020, 9, 11, 10, 57, 11, 342395)