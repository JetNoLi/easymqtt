# Test your ESP functionality with direct MQTT

## What to Do
Firstly we will test your broker using the subTest.py and the pubTest.py. We will subscirbe to a dummy test topic and send a message from the publisher to the subscirber and print it to the screen.  

So your mqttbroker.py file needs to be running and thus so do your necessary database files. Now you can open subTest.py and change line 4, so that you connect to your broker IP (replace localhost) and port Number (8883), note keep the IP in string format. Do the same in line 3 in pubTest.py and then first run subTest.py followed by pubTest.py  

pubTest.py should prompt you for a message. This will be sent to and printed by your subTest.py file.

Next we will test your device funtionality. Your ESP should be setup at this point using setupDevice.py, if all is well your ESP should have printed published and subscribed to the screen (Indicating it has published its register message and subscribed to the necessary topics.)

Leaving that running (as well as your DB and broker files) you can now edit line 3 in testDevicePub.py as you did with the others and run it. You will be prompted for the topic (refer to the readMe for the specifics on the psuedo packet structure), as a test you can input deviceName_switch. Next you will be prompted for a message. At this point connect an LED to your ESP on any usable GPIO pin and enter this pin number as your message. The LED should turn on. (Note if you chose a pin which was floating on initial switch it will always set it to a logical high).

You will be prompted for another topic and message. You can use this very basic interface to test your ESP device as long as you follow the psuedo packet structure as outlined in the readme.
  
