# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 12:05:44 2020

@author: lenovo
"""

#Importing Libraries
import numpy as np
import pandas as pd
from scipy import signal
from scipy.fft import fftshift
import matplotlib.pyplot as plt
import statistics

config_object = ConfigParser()
config_object.read("F:/Project - Vibration/Document/userinfo2_version3.ini")
userinfo2= config_object["user_info2"]
serverinfo= config_object["server_config"]
sensor_info=config_object["sensor_config"]
Broker_address=serverinfo["broker_address"]
#Broker_address='176.9.145.238'
Broker_port=int(serverinfo["broker_port"])
Sensor_id=sensor_info["sensor_id"]
Tag_name=sensor_info["tag_name"]
# power=int(userinfo2["p"]) 

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

run_flag=True
count=1
ary=[]
while run_flag:
    msg="test message"+str(count)
    client.subscribe(Tag_name, qos=1)
    print("length:",+len(queue))
    df = pd.DataFrame(list(queue),columns=['value','var','time_epoch'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df=df.drop_duplicates(keep='first',inplace=False)
    df['time_epoch']=df['time_epoch'].astype(float)
    df['time'] =df['time_epoch'].map(lambda val: datetime.datetime.fromtimestamp(val).strftime('%Y-%m-%d %H:%M:%S.%f'))
    print("lengthdf:",+len(df))        
    count+=1
    print("count:"+ str(count))
    time.sleep(1.2)
    
client.loop_stop()
client.disconnect()

# saving the dataframe 
# df.to_csv('F:\MQTT_Data\Acc_data_19-08-2020_file2.csv') 

#df is a data from MQTT
raw_acc_signal_value = df['value']
#Converting the Accelerometer data into Array 
raw_acc_signal_array = np.array(raw_acc_signal_value)

####################################################
####################################################
####################################################

#Reading the Accelerometer data from MQTT 
acc_raw_sig = Data from Mqtt
#Taking only the Accelerometer value
raw_acc_signal_value = acc_raw_sig["Value"]
#Converting the Accelerometer data into Array 
raw_acc_signal_array = np.array(raw_acc_signal_value)
#sampling frequency
sp_fs = 1600
#Computing the Spectrogram 
f, t, Sxx = signal.spectrogram(raw_acc_signal_array, sp_fs,  window=('tukey', .25),mode='psd')
#Plotting the spectrogram
plt.pcolormesh(t, f, abs(Sxx), shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.title('mode = psd')
plt.show()

#Power spectral Density (PSD)
specto = pd.DataFrame(Sxx)
# Frequency
freq = pd.DataFrame(f)
freq.columns=['frequency']
#Concat the frequency and PSD 
inst_freq = pd.concat([freq, specto.reindex(freq.index)], axis=1)
#set frequency as index 
inst_freq.set_index(["frequency"], inplace = True) 
# inst_freq.idxmax(axis = 0) #for each column it gives max value and its index value.
# find the maximum value in the amplitude
fmax, Amplitude = inst_freq.stack().index[np.argmax(inst_freq.values)] #Gives max vlaue and its index value in a dataframe
#Print the values
print(fmax, Amplitude)
#Work Interval [a, b]
a = 37.5
b = 650
# J is partition size
J = 3
# Partitioning
partition = []
for n in range(3):
    P = (n*((b-a)/(J-1))+a)
    partition.append(P)
    # print(P)
    
# constrain_freq_manual = inst_freq.iloc[[6, 55, 104]] 
# part = [37.5, 356.25, 650]
# constrain the frequency 
constrain_freq = []
for m in partition:
    print(m)
    constrain_frequency = inst_freq.xs(m)
    constrain_freq.append(constrain_frequency)
constrained_freq = pd.DataFrame(constrain_freq)
#Considering only constrained frequencies
fmax_if, Amplitude_if = constrained_freq.stack().index[np.argmax(constrained_freq.values)]

#Constrained frequency values
constrained_freq.idxmax(axis = 0)
raw_acc_signal_value = raw_acc_signal_value.head(500)

#Velocity Synchronous Discrete Fourier Transform
def DFT_slow(x,N,n,k):
    M = np.exp(-2j * np.pi * k * n / N)
    return np.dot(M, x)
    """Compute the discrete Fourier Transform of the 1D array x"""
    x = np.asarray(raw_acc_signal_value, dtype=float)
    N = x.shape[0]
    n = np.arange(N)
    k = n.reshape((N, 1))
    # M = np.exp(-2j * np.pi * k * n / N)
    # return np.dot(M, x)
VSDFT = DFT_slow(x,N,n,k)

#Computing Inverse Discrete Fourier Transform
t = np.arange(500)
#Computing IDFT
pseudo_angular_domain = np.fft.ifft(VSDFT)
#Absolute values
pseudo_ang_domain = pseudo_angular_domain.real
#Plotting graph
plt.plot(t, pseudo_angular_domain.real, 'b-', t, pseudo_angular_domain.imag, 'r--')
plt.legend(('real', 'imaginary'))
plt.show()
#Converted the frequencies into angular domain
specgram_df = list(pseudo_angle_order_map)
data_specgram = pd.DataFrame(specgram_df, columns = ['a','b'])
data_specgram_a = list(data_specgram.a)
data_specgram_b = data_specgram.b
tt = np.arange(500)
#Plotting spectrogram 
plt.pcolormesh(ff, tt, data_specgram_a, shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.title('mode = psd_a')
plt.show()
# tt = np.arange(26)
#obtain the pseudo_angle_order_map per Vibration_Signal(alpha)
ff, tt, pseudo_angle_order_map = signal.spectrogram(pseudo_ang_domain, 200,  window=('tukey', .25),
                              mode='psd')
plt.pcolormesh(ff, tt, abs(pseudo_angle_order_map[0]), shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.title('mode = psd')
plt.show()

#Input to Kurtosis Co-efficient of variation
K =abs(pseudo_angle_order_map)
K = float(K)
#Computing the stationary measures, Kurtosis or PCA method
#Cv = Cofficient of Variation
# a = np.array([[1, 2], [3, 4]])
# data1 = [1, 3, 4, 5, 7, 9, 2]
predicted_shaft_speed = []
for i in K:
    print(i)
    Cv = np.std(i)/statistics.mean(K) 
    predicted_shaft_speed.append(Cv)
# a = np.zeros((2, 512*512), dtype=np.float32)
predicted_shaft_speed = [13,12,15,18]
reference_shaft_speed = [10,11,16,20]
# Select the extracted IF with the minimum variability value noted as
# the most closed to the rotational speed
difference = []
zip_object = zip(reference_shaft_speed, predicted_shaft_speed)
for list1_i, list2_i in zip_object:
    difference.append(list1_i-list2_i)
print(difference)
variability =  [abs(ele) for ele in difference] 
Min_variability = min(variability)
RPM = print(Min_variability)


