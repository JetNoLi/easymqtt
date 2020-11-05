import logging
import asyncio
from hbmqtt.broker import Broker
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_2
from mongotriggers import MongoTrigger
from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId
import threading
import paho.mqtt.client as mqtt
import requests
import dbCreds
from pyngrok import ngrok
import netifaces as ni

client = None
global trigger
global db


#global clientPublisher
topics = []             #stores the topics which have already been added to db i.e. need to update not add 
topicsHeard = ""        #stores the topic of the most recently heard function
url = ""                #url for the ngrok tunnel
#ip =  ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr'] #uncomment this line
ip = ""


#subscriber callback for clientPublish, that listens on
#updateDB and registerDevice, i.e. to notify the DB of a device and of a change
def on_message(topic,msg):
    '''
    Updates the DB as is required, using the topic and the message recieved in BrokerGetMess, will handle accordingly

    :param topic: topic recieved either, updateDB or registerDevice
    :type topic: string
    
    :param msg: message recieved, will be in the psuedo packet format discussed in readme
    :type msg: string
    '''
    global topics
    global topicsHeard
    global url
    #msg = message.payload.decode()
    #msg = msg.split("_")
    deviceName = ""
    commandIssued = ""
    pin = ""
    value = ""

    if topic == "registerDevice":
        #the entire message is the device name in this case
        deviceName = msg
        
        #make the http request to the server. By default it is assumed that the broker and server are running on the same device 
        #http://127.0.0.1:5000/
        r = requests.post(f"{url}/register", json={"DeviceName":deviceName})
        #see the response
        print(r.json())
        
        
    else:
        msg = msg.split("_")
        deviceName = msg[0]
        commandIssued = msg[1]

        if (deviceName + "_" + commandIssued) == topicsHeard:
            print("Already heard")
            topicsHeard = ""

        elif commandIssued == "switch":
            pin = msg[2]          #pin
            value = msg[3]
            #make sure that the value is represented as a boolean
            if int(value) == 1:
                value = True
            else:
                value = False

            #if the device has never been manipulated add it to the switches table
            #otherwise we update the entry
            if topic not in topics:
                r = requests.post(f"{url}/switches", json = {"DeviceName":deviceName, "PinNumber":int(pin), "Status":value, "CommandIssued":commandIssued})
                print(r.json())
                topics.append(topic)
            else:
                r = requests.put(f"{url}/switches/update/{deviceName}/{pin}", json ={"Status":value, "CommandIssued":commandIssued})
                print(r.json())      

def init():
    """
    Initialisation function that connects to the database and provides the database with the ngrok tunnel url. Note that if you  run into trouble with this , you can change the IP line to simply 
    have your broker machines ip, as netifaces attempts to find your ip based on the adapter in the params. Also note that if you do not want remote connectivity, you can remove the http reuesr and set the url to your localhost
    
    """
    global client
    global trigger
    global db
    global url
    
    #ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']

    url = ngrok.connect(5000,"http")
    print(url)
    
    client = MongoClient(dbCreds.uri)
    trigger = MongoTrigger(client)
    db = client[dbCreds.dbName]
    r = requests.put(f"{url}/broker/notifyURL", json={"Broker":ip, "URL":url})
    print(r.json())
    

#this is the method that essentally notifies the device to change its state
#note we do not expect sensors to have a state attached, however, this functionality can easily be added in if needed 
def notification(objectId):
    '''
    Forwards the update to the necessary devices i.e. publishes an MQTT message to the device
    to update itsef as required
    
    :param objectID: the objectI 
    :type objectID: 
    '''
    global db
    global clientPublisher
    global topicsHeard
    doc = db['switchCol'].find_one({'_id':ObjectId(objectId)})
    deviceName = doc["DeviceName"]
    function = doc["CommandIssued"]
    pin = doc["PinNumber"]
    
    topic = deviceName + "_" + function
    msg = pin

    topicsHeard = topic
    clientPublisher = mqtt.Client("Test")
    clientPublisher.connect(ip,1883)
    clientPublisher.publish(topic, msg)    
    print(topic)
    print(doc)

def watchThreaded():
    """
    A function that runs on a separate thread to listen to the database for changes in the switch collection. This would be a part of remote switching feature, having a user make changes to the database via http requests
    and the broker telling the device to enter that state. This can be replicated or modified to handle your specific needs as well.
    """
    try:
        with db['switchCol'].watch([{'$match': {'operationType': 'update'}}]) as stream:
            for update in stream:
                # Do something
                print(update['documentKey']['_id'])
                notification(update['documentKey']['_id'])
    except pymongo.errors.PyMongoError:
        # The ChangeStream encountered an unrecoverable error or the
        # resume attempt failed to recreate the cursor.
        logging.error('...')




logger = logging.getLogger(__name__)

config = {
        'listeners': {
            'default': {
                    'max-connections':0,
                    'type':'tcp',
                    'bind':f"{ip}:1883"
                }
            },
        'sys_interval':10,
        'topic-check':{
            'enabled':True,
            'plugins':['topic_taboo']
            }

        
        }

broker = Broker(config)
@asyncio.coroutine
def broker_coro():
    """
    Starts the broker functionality
    """
    yield from broker.start()

@asyncio.coroutine
def brokerGetMess():
    '''
    Recieves messages on topics the broker client is subscribed to and inputs them into the on_message function
    Subscribes on topics updateDB and registerDevice
    '''
    c = MQTTClient()
    yield from c.connect(f'mqtt://{ip}:1883/')
    yield from c.subscribe([("registerDevice", QOS_2),("updateDB", QOS_2)
        ])
    logger.info("Subscribed")
    try:
        for i in range(1,100):
            message = yield from c.deliver_message()
            print(message.topic)
            packet = message.publish_packet
            print(packet.payload.data.decode("utf-8"))
            on_message(message.topic, packet.payload.data.decode("utf-8"))

            # #see the response
            # print(r.json())
    except ClientException as ce:
        logger.error("Client exception : %s" % ce)




    


# if __name__ == '__main__':
#     global clientPublisher
#     formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
#     logging.basicConfig(level=logging.INFO, format=formatter)
    
#     print("Initialising database listener")
#     init()
#     print("Initialised")
#     print("Starting the watch thread")
#     thread = threading.Thread(target=watchThreaded)
#     thread.start()
#     print("Watch thread started")

#     asyncio.get_event_loop().run_until_complete(broker_coro())
#     asyncio.get_event_loop().run_until_complete(brokerGetMess())
#     asyncio.get_event_loop().run_forever()