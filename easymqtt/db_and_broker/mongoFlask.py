from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import pyMongoSetUp
from datetime import datetime
import dbCreds
import os

##Initialisations
# =============================
app = Flask(__name__)

uri = ""
dbName = ""

#check for creds
if os.path.getsize("dbCreds.py") > 0:
        dbName = dbCreds.dbName
        uri = dbCreds.uri
else:
    with open ("dbCreds.py", 'r+') as f:
        dbName = input("Enter a name for your database: ")
        uri = input("Please enter the connection URI for your databse: ")
        dbNameWrite = "dbName = \"" + dbName + "\"\n"
        uriWrite = "uri = \"" + uri +"\""
        print(uri)
        lines = [dbNameWrite, uriWrite]
        f.writelines(lines)

# init db
client = pyMongoSetUp.connectDB(uri)
switchCol, sensorCol, histCol, deviceCol, archiveCol, liveBrokerCol = pyMongoSetUp.initDefault(client, dbName)

# configure flask app
app.config["MONGO_DBNAME"] = dbName
app.config["MONGO_URI"] = uri
mongo = PyMongo(app)


## ROUTES TO GET ALL  DEVICES
# ================================

# route to get all the current switch type devices connected
@app.route('/switches', methods=['GET'])
def getSwitches():
    """
    Function to get all the switches in in the database

    :return: An array of JSON Objects(dictionaries) where each object represents a specific switch
    :rtype: List of dictionaries
    """
    result = []
    for q in switchCol.find():
        result.append({'DeviceName': q['DeviceName'], 'Status': q['Status'], 'PinNumber': q['PinNumber'],
                       "CommandIssued": q['CommandIssued'], "LastModified": q['LastModified']})

    return jsonify({'result': result})


# route to get all the sensor type devices
@app.route('/sensors', methods=['GET'])
def getSensors():
    """
    Function to get all the sensors in the database

    :return:  An array of JSON Objects(dictionaries) where each object represents a specific sensor
    :rtype: List of Dictionaries
    """
    result = []
    for q in sensorCol.find():
        result.append(
            {'DeviceName': q['DeviceName'], 'LastRecordedValue': q['LastRecordedValue'], 'PinNumber': q['PinNumber'],
             "CommandIssued": q['CommandIssued'], "LastModified": q['LastModified']})

    return jsonify({'result': result})


# route to get the entire history log
@app.route('/history', methods=['GET'])
def getHistory():
    """
        Function to get all the data in the history collection

        :return:  An array of JSON Objects(dictionaries) where each object represents a specific history record
        :rtype: List of Dictionaries
        """
    result = []
    for q in histCol.find():
        #check to see if there is a lastrecordedValue
        if 'LastRecordedValue' in q.keys():
            result.append({'DeviceName': q['DeviceName'], 'PinNumber': q['PinNumber'], "CommandIssued": q['CommandIssued'],
                       'LastRecordedValue': q['LastRecordedValue'], "IssueTime": q['IssueTime']})
        else:
            result.append({'DeviceName': q['DeviceName'], 'PinNumber': q['PinNumber'], "CommandIssued": q['CommandIssued'], 'Status': q['Status'], "IssueTime": q['IssueTime']})
    return jsonify({'result': result})

#route to get all devices in the db
@app.route('/devices',methods=['GET'])
def getDevices():
    """
        Function to get all the devices in the database

        :return:  An array of JSON Objects(dictionaries) where each object represents a specific device
        :rtype: List of Dictionaries
        """
    result = []
    for q in deviceCol.find():
        result.append({'DeviceName':q['DeviceName'],'CreatedAt':q['CreatedAt']})
    return jsonify({'result':result})
# ============================================

# ROUTES TO GET A PARTICULAR DEVICE (IDENTIFIED BY PIN NUMBER AND NAME)

# route to get a particular switch
@app.route('/switches/<deviceName>/<pinNum>', methods=['GET'])
def getSwitch(deviceName, pinNum):
    """
        Function to get a specific switch
        
        :param deviceName: The name of the device the switch is connected to
        :type deviceName: String

        :param pinNum: The pin that the switch is connected to (Note that in the case of mulitple pins, use any one of the pins)
        :type pinNum: int

        :return:  A JSON object (Dictionary) representing a specific switch, or None
        :rtype: Dictionary containing the data for that particilar switch or None
        """
    q = switchCol.find_one({"DeviceName": deviceName, "PinNumber": pinNum})
    result = {'DeviceName': q['DeviceName'], 'Status': q['Status'], 'PinNumber': q['PinNumber'],
              "CommandIssued": q['CommandIssued'], "LastModified": q['LastModified']}

    return jsonify({'result': result})


# route to get a particular sensor
@app.route('/sensors/<deviceName>/<pinNum>', methods=['GET'])
def getSensor(deviceName, pinNum):
    """
          Function to get a specific sensor
         
          :param deviceName: The name of the device the sensor is connected to
          :type deviceName: String

          :param pinNum: The pin that the sensor is connected to (Note that in the case of mulitple pins, use any one of the pins)
          :type pinNum: int

          :return:  A JSON object (Dictionary) representing a specific sensor, or None
          :rtype: Dictionary containing the data for that particilar sensor or None
          """
    q = sensorCol.find_one({"DeviceName": deviceName, "PinNumber": pinNum})
    result = {'DeviceName': q['DeviceName'], 'LastRecordedValue': q['LastRecordedValue'], 'PinNumber': q['PinNumber'],
              "CommandIssued": q['CommandIssued'], "LastModified": q['LastModified']}

    return jsonify({'result': result})


# route to get the entire history for a particular device
@app.route('/history/<deviceName>/<pinNum>', methods=['GET'])
def getDeviceHistory(deviceName, pinNum):
    """
          Function to get the entire history for a particular switch or sensor
          
          :param deviceName: The name of the device the switch or sensor is connected to
          :type deviceName: String

          :param pinNum: The pin that the switch or sensor is connected to (Note that in the case of mulitple pins, use any one of the pins)
          :type pinNum: int

          :return:  An array of JSON objects (Dictionary) representing the history of the sensor or switch , or None
          :rtype: An array of dictionaries containing the entire history for a particular sensor or switch
          """

    result = []
    for q in histCol.find({"DeviceName": deviceName, "PinNumber": pinNum}):
        result.append({'DeviceName': q['DeviceName'], 'PinNumber': q['PinNumber'], "CommandIssued": q['CommandIssued'],
                       'LastRecordedValue': q['LastRecordedValue'], 'Status': q['Status'], "IssueTime": q['IssueTime']})

    return jsonify({'result': result})


# ======================================================

# POST METHODS TO ADD TO THE  DB

# method to add a new device
@app.route('/register', methods=['POST'])
def registerDevice():
    """
    Method to register a device to the DB
    
    :return: A JSON object containing either the data of the newly created device or and Error Message in the event the database could not be reached or a device with that name already exists
    :rtype: A single JSON dictionary as the response body or an error mssage 
    """

    deviceName = request.json["DeviceName"]
    modified = datetime.utcnow()

    # Check to see if the device name is available
    p = deviceCol.find_one({"DeviceName": deviceName})
    if p is not None:
        result = f"Error: There is already a device with the name {deviceName} in the database. Please Try again"
    else:
        # attempt to add to the database, if the data cannot be added, inform the user that an error has occured
        try:
            id = deviceCol.insert_one({"DeviceName": deviceName, "CreatedAt": modified})
            print("Success")
            q = deviceCol.find_one({"DeviceName": deviceName})
            result = {"DeviceName": q["DeviceName"], "CreatedAt": q["CreatedAt"]}
        except:
            result = f'Error: Could not add device {deviceName} to database. Please try again'

    return jsonify({'result': result})


# method to add a new switch
@app.route('/switches', methods=['POST'])
def addSwitch():
    """
        Method to register a switch to the DB 

        :return: A JSON object containing either the data of the newly created switch or and Error Message indicating what went wrong during registration
        :rtype: A single JSON dictionary as the response body or an error mssage 
        """
    deviceName = request.json['DeviceName']
    status = request.json['Status']
    pinNum = request.json["PinNumber"]
    command = request.json["CommandIssued"]
    modified = datetime.utcnow()

    try:
        # check if the device actually exists in the db
        p = deviceCol.find_one({"DeviceName": deviceName})
        # make sure that the switch does not exist in the DB to maintain uniqueness
        switch = switchCol.find_one({"DeviceName": deviceName, "PinNumber": pinNum})

        if p is not None and switch is None:
            id = switchCol.insert_one(
                {'DeviceName': deviceName, 'Status': status, 'PinNumber': pinNum, "CommandIssued": command,
                 "LastModified": modified})
            q = switchCol.find_one({'DeviceName': deviceName, 'PinNumber': pinNum})

            id2 = histCol.insert_one(
                {'DeviceName': deviceName, 'Status': status, 'PinNumber': pinNum, "CommandIssued": command,
                 "IssueTime": modified})

            result = {'DeviceName': q['DeviceName'], 'Status': q['Status'], 'PinNumber': q['PinNumber'],
                      "CommandIssued": q['CommandIssued'], "LastModified": q['LastModified']}
        elif p is None:
            # if no such record exists
            result = f'The device {deviceName} was not found. Please make sure that you have initialised the device'
        elif switch is not None:
            result = f"The required device and pin combination {deviceName}, pin {pinNum} " \
                     f"is not available, try again with a different configuration or remove the device at this pin"
    except:
        result = f'Error: Could not add device {deviceName} to database. Please try again'

    return jsonify({'result': result})


@app.route('/sensors', methods=['POST'])
def addSensor():
    """
        Method to register a sensor to the DB 

        :return: A JSON object containing either the data of the newly created sensor or and Error Message indicating what went wrong during registration
        :rtype: A single JSON dictionary as the response body or an error mssage 
        """
    deviceName = request.json['DeviceName']
    lastVal = request.json['LastRecordedValue']
    pinNum = request.json["PinNumber"]
    command = request.json["CommandIssued"]
    modified = datetime.utcnow()

    try:
        # check if the device actually exists in the db
        p = deviceCol.find_one({"DeviceName": deviceName})
        # make sure that the switch does not exist in the DB to maintain uniqueness
        sensor = sensorCol.find_one({"DeviceName": deviceName, "PinNumber": pinNum})
        if p is not None and sensor is None:
            id = sensorCol.insert_one(
                {'DeviceName': deviceName, 'LastRecordedValue': lastVal, 'PinNumber': pinNum, "CommandIssued": command,
                 "LastModified": modified})
            q = sensorCol.find_one({'DeviceName': deviceName, 'PinNumber': pinNum})

            id2 = histCol.insert_one(
                {'DeviceName': deviceName, 'LastRecordedValue': lastVal, 'PinNumber': pinNum, "CommandIssued": command,
                 "IssueTime": modified})

            result = {'DeviceName': q['DeviceName'], 'LastRecordedValue': q['LastRecordedValue'],
                      'PinNumber': q['PinNumber'],
                      "CommandIssued": q['CommandIssued'], "LastModified": q['LastModified']}
        elif p is None:
            # if no such record exists
            result = f'The device {deviceName} was not found. Please make sure that you have initialised the device'
        elif sensor is not None:
            result = f"The required device and pin combination {deviceName}, pin {pinNum} " \
                     f"is not available, try again with a different configuration or remove the device at this pin"

    except:
        result = f'Error: Could not add device {deviceName} to database. Please try again'
    return jsonify({'result': result})


# =========================================================================

# Update calls

# route to update the status of the switch
@app.route('/switches/update/<deviceName>/<pinNum>', methods=['PUT'])
def updateSwitch(deviceName, pinNum):
    # at this point it is assumed that the device exists
    # here we just need to make sure it exists in the switch table
    """
          Function to update a specific switch. Note that this function assumes that the device already exists and only checks for existence in the switch table 
          
          :param deviceName: The name of the device the switch is connected to
          :type deviceName: String

          :param pinNum: The pin that the switch is connected to (Note that in the case of mulitple pins, use any one of the pins)
          :type pinNum: int

          :return: A JSON object containing either the data of the newly updated switch or and Error Message indicating what went wrong during registration
          :rtype: A single JSON dictionary as the response body or an error message 
          """
    status = request.json['Status']
    command = request.json["CommandIssued"]
    modified = datetime.utcnow()

    pinNum = int(pinNum)

    try:
        # check if that specific configuration is in the database
        p = switchCol.find_one({"DeviceName": deviceName, "PinNumber": pinNum})
        if p is not None:
            res = switchCol.find_one_and_update({"DeviceName": deviceName, "PinNumber": pinNum},
                                                {"$set": {'Status': status, "CommandIssued": command,
                                                          "LastModified": modified}}
                                                )

            q = switchCol.find_one({'DeviceName': deviceName, 'PinNumber': pinNum})

            id2 = histCol.insert_one(
                {'DeviceName': deviceName, 'Status': status, 'PinNumber': pinNum, "CommandIssued": command,
                 "IssueTime": modified})

            result = {'DeviceName': q['DeviceName'], 'Status': q['Status'], 'PinNumber': q['PinNumber'],
                      "CommandIssued": q['CommandIssued'], "LastModified": q['LastModified']}
        else:
            # if no such record exists
            result = f'The device {deviceName} was not found. Please make sure that you have initialised the device'
    except:
        result = f'Error: Could not update device {deviceName} . Please try again'
    return jsonify({'result': result})


# route to update the last revorded value from a sensor
@app.route('/sensors/update/<deviceName>/<pinNum>', methods=['PUT'])
def updateSensor(deviceName, pinNum):
    # at this point it is assumed that the device exists
    # here we just need to make sure it exists in the sensor table
    """
           Function to update a specific sensor. Note that this function assumes that the device already exists and only checks for existence in the sensor table 
           
           :param deviceName: The name of the device the sensor is connected to
           :type deviceName: String

           :param pinNum: The pin that the sensor is connected to (Note that in the case of mulitple pins, use any one of the pins)
           :type pinNum: int

           :return: A JSON object containing either the data of the newly updated sensor or and Error Message indicating what went wrong during registration
           :rtype: A single JSON dictionary as the response body or an error message 
           """
    lastVal = request.json['LastRecordedValue']
    command = request.json["CommandIssued"]
    modified = datetime.utcnow()

    pinNum = int(pinNum)

    try:
        # check if that specific configuration is in the database
        p = sensorCol.find_one({"DeviceName": deviceName, "PinNumber": pinNum})
        if p is not None:
            res = sensorCol.find_one_and_update({"DeviceName": deviceName, "PinNumber": pinNum},
                                                {"$set": {'LastRecordedValue': lastVal, "CommandIssued": command,
                                                          "LastModified": modified}}
                                                )

            q = sensorCol.find_one({'DeviceName': deviceName, 'PinNumber': pinNum})

            id2 = histCol.insert_one(
                {'DeviceName': deviceName, 'LastRecordedValue': lastVal, 'PinNumber': pinNum, "CommandIssued": command,
                 "IssueTime": modified})

            result = {'DeviceName': q['DeviceName'], 'LastRecordedValue': lastVal, 'PinNumber': q['PinNumber'],
                      "CommandIssued": q['CommandIssued'], "LastModified": q['LastModified']}
        else:
            # if no such record exists
            result = f'The device {deviceName} was not found. Please make sure that you have initialised the device'
    except:
        result = f'Error: Could not update device {deviceName} . Please try again'
    return jsonify({'result': result})


# =========================================================================

# DELETE FUNCTIONALITY

# route to delete a switch
@app.route('/switches/delete/<deviceName>/<pinNumber>', methods=['DELETE'])
def deleteSwitch(deviceName, pinNumber):
    """
          Function to delete a specific switch. Note that this function assumes that the device already exists . Additionally, all records of it in the history column get moved to the archive
          
          :param deviceName: The name of the device the switch is connected to
          :type deviceName: String

          :param pinNum: The pin that the switch is connected to (Note that in the case of mulitple pins, use any one of the pins)
          :type pinNum: int

          :return: A JSON object containing a success or error message depending on what happened durind deletion
          :rtype: JSON object with a single string
          """
    pinNumber = int(pinNumber)
    q = {'DeviceName': deviceName, 'PinNumber': pinNumber}
    IO = 'O'
    archivedAt = datetime.utcnow()

    try:
        # delete from the switch collection
        switchCol.delete_one(q)

        # add all teh records pertaining to that device in the history table into the archive
        for record in histCol.find(q):
            archiveCol.insert_one({'DeviceName': deviceName, 'Status': record['Status'], 'PinNumber': pinNumber,
                                   "CommandIssued": record['CommandIssued'],
                                   "IssueTime": record['IssueTime'], "I/O": IO, "ArchivedAt": archivedAt})

        # delete all from the history table
        histCol.delete_many(q)

        return jsonify({
            "result": f"Successfully deleted the switch. at {deviceName}, pin {pinNumber} Its data can still be seen in archiveCol in MongoDB"})
    except:
        return jsonify({"result": f"Error: Could not delete switch at {deviceName}, pin {pinNumber} ."})


# route to delete a sensor
@app.route('/sensors/delete/<deviceName>/<pinNumber>', methods=['DELETE'])
def deleteSensor(deviceName, pinNumber):
    """
          Function to delete a specific sensor. Note that this function assumes that the device already exists . Additionally, all records of it in the history column get moved to the archive
          
          :param deviceName: The name of the device the sensor is connected to
          :type deviceName: String

          :param pinNum: The pin that the sensor is connected to (Note that in the case of mulitple pins, use any one of the pins)
          :type pinNum: int

          :return: A JSON object containing a success or error message depending on what happened durind deletion
          :rtype: JSON object with a single string
          """
    pinNumber = int(pinNumber)
    q = {'DeviceName': deviceName, 'PinNumber': pinNumber}
    IO = 'I'
    archivedAt = datetime.utcnow()

    try:
        # delete from the switch collection
        sensorCol.delete_one(q)

        # add all teh records pertaining to that device in the history table into the archive
        for record in histCol.find(q):
            archiveCol.insert_one(
                {'DeviceName': deviceName, 'LastRecordedValue': record['LastRecordedValue'], 'PinNumber': pinNumber,
                 "CommandIssued": record['CommandIssued'],
                 "IssueTime": record['IssueTime'], "I/O": IO, "ArchivedAt": archivedAt})

        # delete all from the history table
        histCol.delete_many(q)

        return jsonify(
            {"result": f"Successfully deleted the sensor at {deviceName}, pin {pinNumber}.Its data can still be seen "
                       f"in archiveCol in MongoDB"})
    except:
        return jsonify({"result": f"Error: Could not delete sensor at {deviceName}, pin {pinNumber} ."})


# route to swap from sensor to switch
@app.route('/sensors/toSwitch/<deviceName>/<pinNumber>', methods=['DELETE'])
def sensorToSwitch(deviceName, pinNumber):
    pinNumber = int(pinNumber)
    q = {'DeviceName': deviceName, 'PinNumber': pinNumber}
    """
          Function to change a pin on a device from mapping to a sensor to mapping to a switch. additionally, it moves all associated records from the hisoty and archives them
          
          :param deviceName: The name of the device the sensor is connected to
          :type deviceName: String

          :param pinNum: The pin that the sensor is connected to (Note that in the case of mulitple pins, use any one of the pins)
          :type pinNum: int

          :return: A JSON object containing either the data of the newly updated switch or and Error Message indicating what went wrong during registration
          :rtype: JSON object with a single string
          """
    modified = datetime.utcnow()

    try:
        # get the sensor in question
        sensor = sensorCol.find_one(q)

        # delete the sensor from the db
        deleteSensor(deviceName, pinNumber)

        id = switchCol.insert_one(
            {'DeviceName': deviceName, 'Status': False, 'PinNumber': pinNumber,
             "CommandIssued": sensor['CommandIssued'],
             "LastModified": modified})
        p = switchCol.find_one(q)

        result = {'DeviceName': p['DeviceName'], 'Status': p['Status'], 'PinNumber': p['PinNumber'],
                  "CommandIssued": p['CommandIssued'], "LastModified": p['LastModified']}
        return jsonify({"result": result})

    except:
        return jsonify({"result": f"Error: Could not convert sensor at {deviceName}, pin {pinNumber} to a switch"})


# route to swap from switch to sensor
@app.route('/switches/toSensor/<deviceName>/<pinNumber>', methods=['DELETE'])
def switchToSensor(deviceName, pinNumber):
    """
          Function to change a pin on a device from mapping to a switch to mapping to a sensor. additionally, it moves all associated records from the hisoty and archives them
          
          :param deviceName: The name of the device the sensor is connected to
          :type deviceName: String

          :param pinNum: The pin that the sensor is connected to (Note that in the case of mulitple pins, use any one of the pins)
          :type pinNum: int

          :return: A JSON object containing either the data of the newly updated switch or and Error Message indicating what went wrong during registration
          :rtype: JSON object with a single string
          """
    pinNumber = int(pinNumber)
    q = {'DeviceName': deviceName, 'PinNumber': pinNumber}

    modified = datetime.utcnow()

    try:
        # get the switch in question
        switch = switchCol.find_one(q)

        # delete the switch from the db
        deleteSwitch(deviceName, pinNumber)

        id = sensorCol.insert_one(
            {'DeviceName': deviceName, 'LastRecordedValue': -1.0, 'PinNumber': pinNumber,
             "CommandIssued": switch['CommandIssued'],
             "LastModified": modified})
        p = sensorCol.find_one(q)

        result = {'DeviceName': p['DeviceName'], 'LastRecordedValue': p['LastRecordedValue'],
                  'PinNumber': p['PinNumber'],
                  "CommandIssued": p['CommandIssued'], "LastModified": p['LastModified']}
        return jsonify({"result": result})

    except:
        return jsonify({"result": f"Error: Could not convert switch at {deviceName}, pin {pinNumber} to a sensor"})


# route to entirely delete a device.
@app.route('/delete/<deviceName>', methods=['DELETE'])
def deleteDevice(deviceName):
    # at this point it is assumed that the pins have been cleared out from the device
    # thus the only thing that needs deleting from is the device collection
    """
    Method to delete a device from the database. Note that  it assumes that all the pins on the device ave been cleared.

    :param deviceName: The name of ther device
    :type deviceName: String

    :return: A JSON object with either a success or error message
    :rtype: JSON object containing a single string
    """
    try:
        q = {"DeviceName": deviceName}
        deviceCol.delete_one(q)
        return jsonify({"result": f"Successfully deleted device {deviceName}"})

    except:
        return jsonify({"result": f"Error: Failed to delete device {deviceName}. Please try agaain"})

#==================================================================================================

#Special route for the broker to annouce the ip for external access
@app.route('/broker/notifyURL', methods=['PUT'])
def brokerUpdateUrl():
    """
    Method called by the broker to update its URL in the DB for liveness checks

    :return: A JSON object indicating transaction status
    :rtype: JSON object containing a string
    """
    url = request.json["URL"]
    broker = request.json["Broker"]
    modified = datetime.utcnow()

    try:
        q = liveBrokerCol.find_one({'Broker':broker})
        if q is None:
            print("Inserting")
            liveBrokerCol.insert_one({"Broker":broker, 'URL':url, "LastModified":modified})
        else:
            liveBrokerCol.update_one(q,
                             {"$set":{'Broker':broker, 'URL':url, 'LastModified':modified}}
                             )
        return jsonify({"result":"ok"})
    except Exception as e:
        print(e)
        return jsonify({"result":"could not update the url"})




if __name__ == '__main__':
    app.run(debug=True)
