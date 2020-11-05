# FlaskDB
Web Server REST API and MQTT Broker Code


## Pre-requisites
Before attempting to run this code, there are three things that are required:

1. A MongoDB account and a connection url to your cluster. This will be something similar to the url in the figure below. Make sure that you have placed your credentials in the correct before inserting when prompted
![Connection image](https://github.com/VoidMaster23/FlaskDB/blob/master/MongoConnect.png)


2. Make sure that the computer that will be running the broker program has a wlan0. If you are running this on a raspberry pi this should not be a problem. However, if you attempt to run and you get a "ValueError: Must specify a valid interface name", simply edit line 26 in the broker file to have the ip of the device you use as the broker.

3. Make sure your machine is runnning python 3

## Running the programs
Before you run the broker or the mongoFlask, make sure you have installed the necessary packages using "pip install -r requirements.txt" in your virtual environment.


**IMPORTANT**: Make sure you run the files in the following order:
1. python3 mongoFlask.py
    1. You will be prompted to enter a name for your database, enter what ever name youd like, and the system will create all the necessary collections and run valudation for you.
    2. You will be prompted to enter your cluster connection url. If at any point you would like to change this in future, you can edit or clear dbCreds.py as these details will only be asked for on the first run
  
2. python3 mqttbroker.py
The first run will take some time as the system will attempt to download ngrok tunneling software onto your system. If you do not want this functionality enabled make sure to change line 89 to have either your own url or localhost

The system will then attempt to push the randomly generated url to the liveBroker collection in the database
