import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect('localhost', 8883)

def on_connect(client, userdata, flags, rc):
    print("Connected")
    client.subscribe("test")

def on_message(client, userdata, message):
    print(message.payload.decode())



client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()

    
