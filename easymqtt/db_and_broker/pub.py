import paho.mqtt.client as mqtt
client = mqtt.Client("EdPoo")
client.connect("localhost",9999)
client.subscribe("updateDB")
client.subscribe("registerDevice")

def on_message(client, userdata, message):
    print(message.payload.decode())

client.on_message = on_message
client.loop_start()

while True:
    client.publish(input("Topic: "),input("message: "))
