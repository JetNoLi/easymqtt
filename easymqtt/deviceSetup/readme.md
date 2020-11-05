# ESP Device Readme

## Contents
1. Overview
2. Pre Requisites
3. Setting Up Device
4. First Boot after setup
5. MQTT Psuedo Packet Structure


## 1. Overview

The ESP Device will be configured to connect to your WiFi network and your chosen Broker. This will configure all functions in functions.py (refer to the docs for list of functions) to be callable remotely.

## 2. Pre Requisistes

It is recommended that you set up your ESP device on a linux machine. If you are using a windows machine, that is fine, certian features will be excluded from setupDevice.py (The file run to configure your ESP).

### Windows machines
* git
* python3
* Your ESP will need to be flashed with the latest version of Micropython
* You will need a means to copy the generated files to your ESP Device
   
### Linux machines
* git
* python3
* Latest version of Micropython .bin file in the same directory as setupDevice.py
* esptool.py


## 3. Setting Up Device

To set up your ESP device first connect it to the computer of your choice taking note of the serial port used if you are setting up on a linux machine. From terminal you can see a list of your serial ports using:   
ls /dev/tty*  
Take note of the devices before plugging in and after plugging in. An example of serial port is /dev/ttyUSB0  
  
Now you can run setupDevice.py and follow the on screen instructions, please note when giving your ESP a name do not include underscores in the name ("_"). If on a linux machine ampy will be installed if not currently and will automatically copy the generated files over to the ESP device (It will also ask to flash your device, we are working on adding these features for windows machines).
  
Once the Device files have been copied over your ESP is now ready to use.

## 4. First Boot after setup

Once setup is completed you should restart your ESP device, the recommended method is to enter the REPL and use machine.reset().

On this initial boot it will attempt to connect to the WiFi network and your Broker (hence your broker program must be running otherwise you will get an error). At this point your device will register itself on the Database and will subscribe to all the API function topics (Form of MQTT messages discussed in the next section). Your Device will now be accesible remotely and via direct MQTT messages on its local network.
  
## 5. MQTT Psuedo Packet Structure
Topic = deviceName_functionName  
Where functionName is a function from functions.py and your deviceName is the unique name you gave to your ESP in setupDevice.py
  
Example - "MikeESP_switch"
  
Message = param1_param2_param3...  
For switch only 1 param is necessary, the pin number, hence
  
Example - "5"

For a more indepth functions such as the listen or timedInterrupt functions with more parameters, each parameter is seperted with an underscore i.e. For listen which is defaultly configured to a listenCB method in the main.

Example
* Topic = "MikeESP_listen"
* Message = "13_1_listenCB"

This is configured to created an interrupt on pin 13, which is triggered on a rising edge and will call the listenCB function.


