"""
Creates multiple Connections to a broker
and sends and receives messages
"""
import paho.mqtt.client as mqtt
import time
import json
import threading
import logging
topic = ['testTopic','testTopic2','testTopic3','testTopic4']
clients = clients = [
    {"broker":"192.168.1.185", "port": 1883},
    {"broker":"192.168.1.218", "port": 1883},
    {"broker":"192.168.1.102", "port": 5353},
    {"broker":"176.9.144.238", "port": 1883}
]
nclients = len(clients)
message = "test message"
out_queue = []  # use simple array to get printed messages in some form of order
def multi_loop(nclients, flag=True):
    while flag:
        for i in range(nclients):
            client = clients[i]["client"]
            client.loop(0.01)

#########
def on_log(client, userdata, level, buf):
    print(buf)

def on_message(client, userdata, message):
    time.sleep(1)
    for i in range(topic):
        cname = "topic" + str(i)
        msg = "message received", str(cname)
    # print(msg)
    out_queue.append(msg)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        for i in range(nclients):
            if clients[i]["client"] == client:
                client.subscribe(topic)

                
                break
        #client.subscribe(topic)
   

def on_disconnect(client, userdata, rc):
    print("Bad connection Returned code=", rc)
    client.loop_stop()
    client.unsubscribe(topic)

    
    # print("client disconnected ok")

def on_publish(client, userdata, mid):
    time.sleep(1)
    print("In on_pub callback mid= ", mid)

def Create_connections():
    for i in range(nclients):
        cname = "client" + str(i)
        t = int(time.time())
        client_id = cname + str(t)  # create unique client_id
        client = mqtt.Client(client_id)  # create new instance
        clients[i]["client"] = client
        clients[i]["client_id"] = client_id
        clients[i]["cname"] = cname
        broker = clients[i]["broker"]
        port = clients[i]["port"]
        try:
            client.connect(broker, port)  # establish connection
        except:
            print("Connection Fialed to broker ", broker)
            continue
        # client.on_log=on_log #this gives getailed logging
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        # client.on_publish = on_publish
        client.on_message = on_message
        while not client.connected_flag:
            client.loop(0.01)  # check for messages
            time.sleep(0.05)

mqtt.Client.connected_flag = False  # create flag in class
no_threads = threading.active_count()
print("current threads =", no_threads)
print("Creating  Connections ", nclients, " clients")
Create_connections()
t = threading.Thread(target=multi_loop, args=(nclients, True))  # start multi loop
t.start()
print("All clients connected ")
time.sleep(5)
#
count = 0
no_threads = threading.active_count()

Run_Flag = True

try:
    while Run_Flag:
        i = 0
        for i in range(nclients):
            client = clients[i]["client"]
            pub_topic = 'pub1'
            counter = str(count).rjust(6, "0")
            msg = "client " + str(i) + " " + counter + "XXXXXX " + message
            if client.connected_flag:
                client.publish(pub_topic, msg)
                time.sleep(0.1)
                print("publishing client " + str(i))
            i += 1
        time.sleep(10)  # now print messages
        print("queue length=", len(out_queue))
        for x in range(len(out_queue)):
            print(out_queue.pop())
        count += 1
        # time.sleep(5)#wait
except KeyboardInterrupt:
    print("interrupted  by keyboard")
# client.loop_stop() #stop loop
for client in clients:
    client.disconnect()
multi_loop(flag=False)  # stop loop
# allow time for allthreads to stop before existing
time.sleep(10)

