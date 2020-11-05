import pymongo
from datetime import datetime
from pymongo.errors import CollectionInvalid
from collections import OrderedDict
from schema import switchColSchema
from schema import sensorColSchema
from schema import histColSchema
from schema import  deviceColSchema
from schema import archiveColSchema
from schema import liveBroker


global client
global db

def connectDB(connectStr):
    """
    Function to connect to the cloud db

    :param connectStr:  The string obtained from mongoDB for connection. Ensure that your details are contained in this
    :type: String

    :return: The new MongoClient
    :rtype: MongoClient
    """
    global client
    client = pymongo.MongoClient(connectStr)

    return client

def initDefault(client, database):
    """
    Initialises the default documents in the database by calling the init functions for each of the collections

    :param client: The client object
    :type client: MongoClient

    :param database: The name of the database you created
    :type database: String

    :return: Six collections are returned: switchCol, sensorCol, histCol, deviceCol, archiveCol,liveBrokerCol
    :rtype: Tuple containing the collections returned
    """
    db = client[database]
    print("Initialising Database, this may take a while...")
    initSwitch(db)
    initSensor(db)
    initHist(db)
    initDevice(db)
    initArchive(db)
    initBrokerCheck(db)
    print("Databases created")


    switchCol = db["switchCol"]
    sensorCol = db["sensorCol"]
    histCol = db["historyCol"]
    deviceCol = db["deviceCol"]
    archiveCol = db['archiveCol']
    liveBrokerCol = db['liveBroker']


    return switchCol, sensorCol, histCol, deviceCol, archiveCol,liveBrokerCol

def initDevice(db):
    """
    Method that initialises and validates the device collection.
    
    :param db: The database needing to be accessed, which can be obtained using client["<Name of DB>"] or client.db

    """
    collection = "deviceCol"
    validator = {'$jsonSchema': {'bsonType': 'object', 'properties': {}}}
    required = []

    for fieldKey in deviceColSchema:
        field = deviceColSchema[fieldKey]
        props = {'bsonType': field['type']}
        min  = field.get("minlength")

        if type(min) == int:
            props["minimum"] = min

        if field.get("required") is True: required.append(fieldKey)
        validator['$jsonSchema']['properties'][fieldKey] = props

    if len(required) > 0:
        validator['$jsonSchema']['required'] = required

    query = [('collMod', collection),
         ('validator', validator)]

    try:
        db.create_collection(collection)
    except CollectionInvalid:
        pass

    command_result = db.command(OrderedDict(query))

    print(command_result)

def initSwitch(db):
    """
       Method that initialises and validates the switch collection.
       
       :param db: The database needing to be accessed, which can be obtained using client["<Name of DB>"] or client.db

       """
    collection = "switchCol"
    validator = {'$jsonSchema': {'bsonType': 'object', 'properties': {}}}
    required = []

    for fieldKey in switchColSchema:
        field = switchColSchema[fieldKey]
        props = {'bsonType': field['type']}
        min  = field.get("minlength")

        if type(min) == int:
            props["minimum"] = min

        if field.get("required") is True: required.append(fieldKey)
        validator['$jsonSchema']['properties'][fieldKey] = props

    if len(required) > 0:
        validator['$jsonSchema']['required'] = required

    query = [('collMod', collection),
         ('validator', validator)]

    try:
        db.create_collection(collection)
    except CollectionInvalid:
        pass

    command_result = db.command(OrderedDict(query))

    print(command_result)

def initSensor(db):
    """
       Method that initialises and validates the sensor collection.
       
       :param db: The database needing to be accessed, which can be obtained using client["<Name of DB>"] or client.db

       """
    collection = "sensorCol"
    validator = {'$jsonSchema': {'bsonType': 'object', 'properties': {}}}
    required = []

    for fieldKey in sensorColSchema:
        field = sensorColSchema[fieldKey]
        props = {'bsonType': field['type']}
        min  = field.get("minlength")

        if type(min) == int:
            props["minimum"] = min

        if field.get("required") is True: required.append(fieldKey)
        validator['$jsonSchema']['properties'][fieldKey] = props

    if len(required) > 0:
        validator['$jsonSchema']['required'] = required

    query = [('collMod', collection),
         ('validator', validator)]

    try:
        db.create_collection(collection)
    except CollectionInvalid:
        pass

    command_result = db.command(OrderedDict(query))

    print(command_result)

def initHist(db):
    """
       Method that initialises and validates the history collection.
       
       :param db: The database needing to be accessed, which can be obtained using client["<Name of DB>"] or client.db

       """
    collection = "historyCol"
    validator = {'$jsonSchema': {'bsonType': 'object', 'properties': {}}}
    required = []

    for fieldKey in histColSchema:
        field = histColSchema[fieldKey]
        props = {'bsonType': field['type']}
        min  = field.get("minlength")

        if type(min) == int:
            props["minimum"] = min

        if field.get("required") is True: required.append(fieldKey)
        validator['$jsonSchema']['properties'][fieldKey] = props

    if len(required) > 0:
        validator['$jsonSchema']['required'] = required

    query = [('collMod', collection),
         ('validator', validator)]

    try:
        db.create_collection(collection)
    except CollectionInvalid:
        pass

    command_result = db.command(OrderedDict(query))

    print(command_result)

def initArchive(db):
    """
       Method that initialises and validates the archive collection.
       
       :param db: The database needing to be accessed, which can be obtained using client["<Name of DB>"] or client.db

       """
    collection = "archiveCol"
    validator = {'$jsonSchema': {'bsonType': 'object', 'properties': {}}}
    required = []

    for fieldKey in archiveColSchema:
        field = archiveColSchema[fieldKey]
        props = {'bsonType': field['type']}
        min  = field.get("minlength")

        if type(min) == int:
            props["minimum"] = min

        if field.get("required") is True: required.append(fieldKey)
        validator['$jsonSchema']['properties'][fieldKey] = props

    if len(required) > 0:
        validator['$jsonSchema']['required'] = required

    query = [('collMod', collection),
         ('validator', validator)]

    try:
        db.create_collection(collection)
    except CollectionInvalid:
        pass

    command_result = db.command(OrderedDict(query))

    print(command_result)

def initBrokerCheck(db):
    """
       Method that initialises and validates the liveBroker collection.
       
       :param db: The database needing to be accessed, which can be obtained using client["<Name of DB>"] or client.db

       """
    collection = "liveBroker"
    validator = {'$jsonSchema': {'bsonType': 'object', 'properties': {}}}
    required = []

    for fieldKey in liveBroker:
        field = liveBroker[fieldKey]
        props = {'bsonType': field['type']}
        min  = field.get("minlength")

        if type(min) == int:
            props["minimum"] = min

        if field.get("required") is True: required.append(fieldKey)
        validator['$jsonSchema']['properties'][fieldKey] = props

    if len(required) > 0:
        validator['$jsonSchema']['required'] = required

    query = [('collMod', collection),
         ('validator', validator)]

    try:
        db.create_collection(collection)
    except CollectionInvalid:
        pass

    command_result = db.command(OrderedDict(query))

    print(command_result)






