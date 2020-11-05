"""
Module To store the database schema
"""
# This is the schema for the History Collection
histColSchema = {

'DeviceName':{
    'type': 'string',
    'minlength': 1,
    'required': True,
},
'CommandIssued':{
    'type': 'string',
    'minlength': 1,
    'required': True,
},
    'PinNumber': {
        'type': 'int',
        'required': True,
    },

    'LastRecordedValue': {
        'type': 'double',
    },

    'Status':{
        'type': 'bool',
    },

'IssueTime':{
    'type': 'date',
    'required':True,
}


}

# This is the schema for the Switch Collection
sensorColSchema = {

'DeviceName':{
    'type': 'string',
    'minlength': 1,
    'required': True,
},
    'LastRecordedValue':{
        'type': 'double',
        'required': True,
    },

    'PinNumber':{
        'type': 'int',
        'required': True,
    },
'CommandIssued':{
    'type': 'string',
    'minlength': 1,
    'required': True,
},

'LastModified':{
    'type': 'date',
    'required': True,
}


}

# This is the schema for the Switch Collection
switchColSchema = {

'DeviceName':{
    'type': 'string',
    'minlength': 1,
    'required': True,
},
    'Status':{
        'type': 'bool',
        'required': True,
    },

    'PinNumber':{
        'type': 'int',
        'required': True,
    },
'CommandIssued':{
    'type': 'string',
    'minlength': 1,
    'required': True,
},

'LastModified':{
    'type': 'date',
    'required': True,
}


}

# This is the schema for the device collectionn
deviceColSchema = {

'DeviceName':{
    'type': 'string',
    'minlength': 1,
    'required': True,
},

'CreatedAt':{
    'type': 'date',
    'required': True,
}


}

# This is the schema for the archive Collection
archiveColSchema = {

'DeviceName':{
    'type': 'string',
    'minlength': 1,
    'required': True,
},
'CommandIssued':{
    'type': 'string',
    'minlength': 1,
    'required': True,
},
    'PinNumber': {
        'type': 'int',
        'required': True,
    },

    'LastRecordedValue': {
        'type': 'double',
    },

    'Status':{
        'type': 'bool',
    },

'IssueTime':{
    'type': 'date',
    'required':True,
},

'ArchivedAt':{
    'type':'date',
    'required': True
},

'I/O':{
    'type':'string',
    'required': True
}




}

#schema for the liveness column
liveBroker = {
    'Broker':{
        'type':'string',
        'required':True,
    },

    'URL':{
        'type': 'string',
        'minlength': 1,
        'required':True

    },

    'LastModified':{
        'type':'date',
        'required':True
    }


}