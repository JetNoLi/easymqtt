import paho.mqtt.client as mqtt
client = mqtt.Client("test")
client.connect("localhost", 8883)
client.subscribe("test")



def on_message(client, userdata, message):
    pass

client.on_message = on_message
client.loop_start()

while True: 
    client.publish("test" , input("message: "))