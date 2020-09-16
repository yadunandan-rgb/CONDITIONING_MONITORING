import paho.mqtt.client as mqtt
from configparser import ConfigParser
import pandas as pd
import numpy as np
import math 
import scipy as sy
import scipy.fftpack as syfp
from scipy import signal
from scipy.fftpack import fft, ifft
import matplotlib.pyplot as plt
import os
import csv
import sys
import math 
from numpy import savetxt

array=[]
broker_address="176.9.144.238"
broker_port = 1883


def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code "+rc)
def on_disconnect(client, userdata, rc):
   print("Client Got Disconnected")
def on_message(client, userdata, message):
   print("Message Recieved: "+message.payload.decode())
count = 0

client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect  
client.connect(broker_address, broker_port)
client.subscribe("LiteraturateCsvData", qos=1)
client.loop_forever()
count+=1
print(count)