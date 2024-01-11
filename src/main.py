# QR Code Scanner App, which sends scanned QR Code to PLC
# Copyright 2023 Siemens AG
# This file is subject to the terms and conditions of the MIT License.  
# See LICENSE file in the top-level directory.
# Date: 22.12.2023

import paho.mqtt.client as mqtt
from createDict import getDict
import evdev
import sys
import os
import time
import json

#============================
# Constants
#============================

CONST_CAPS = 42
CONST_ENTER = 28
CONST_KEY_DOWN = 1
keys = "X^1234567890    qwertzuiop    asdfghjkl   : yxcvbnm )                                                                               "
PLC_DATA_FORMAT = {"seq": 1, "vals": [{"id": "", "val": ""}]}

class mqttclient:

    """
    mqttclient access the IE-Databus and 
    returns the Metadata from the dedicated connection of the OPCUA Connector
    
    """

    def __init__(self,clientname,broker, user, password, topic, plc_connection):
        
        # Initialize the the class object

        # Initialize dictionary for Metadata
        self.IDDict = {}
        # IE Databus and OPCUA Connector information
        self.broker = broker
        self.mqtt_user = user
        self.mqtt_password = password
        self.metaDataTopic = topic
        self.plc_connection = plc_connection
        # Initialize mqtt client and define callback functions
        self.clientname = clientname
        self.client = mqtt.Client(self.clientname)
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message        
        
    # Callback function of mqtt client
    def on_message(self, client, userdata, message):
        msg = message.payload.decode("utf-8")
        # Parse received metadata and create dictionary        
        self.IDDict = getDict(msg, self.plc_connection) 
        
        print("INFO | New message received: " + msg)
        print("INFO | Extracted dict: " + str(self.IDDict))
        sys.stdout.flush()

    def on_connect(self, client, userdata, flags, rc):
        print("INFO | Connected to " + self.broker + " MQTT broker")
        print("INFO | Subscribe to " + self.metaDataTopic + " topic")
        sys.stdout.flush()
        self.client.subscribe(self.metaDataTopic)
      
    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("INFO | On subscribe callback executed")
        sys.stdout.flush()

    def start_connection(self):
        print("INFO | Start connection to " + self.broker + " broker")
        sys.stdout.flush()
        
        # Set username and password, must be created it databus configurator
        self.client.username_pw_set(self.mqtt_user, self.mqtt_password)
        # Connect to databus
        self.client.connect(self.broker)
        self.client.loop_start()

#============================
# Help functions
#============================

# Check for plugged in Scanner
def check_for_scanner(scannertype):
    # Scan devices
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    
    for device in devices:
        # Check for Scanner type 
        if (device.name == scannertype):
            # Get device event
            scannerevent = device.path
            return(scannerevent)

# Read json file
def read_parameter(jsonfile):
    with open(jsonfile) as params:
        data = json.load(params)
        return data

#============================
# Main Function
#============================

# Initialize topic for writing to PLC
PLC_QR_Code = PLC_DATA_FORMAT

# Read parameter file
params = read_parameter('/cfg-data/param.json')
scannertype = (params['Scannertype'])
mqtt_user = params['User']
mqtt_password = params['Password']
mqtt_broker_server = params['Mqtt_Broker_Server']
meta_data_topic = params['Metadata']
plc_qrcode_topic = params['Topic']

# Separates the Connection name from the mqtt topic
connection_name = plc_qrcode_topic.split("/")
connection_name = connection_name[len(connection_name)-1]

# Initialize mqtt client object with paramter from the config file and starts the connection to the broker 
my_mqtt_client = mqttclient('scanner-service',mqtt_broker_server, mqtt_user, mqtt_password, meta_data_topic, connection_name)
my_mqtt_client.start_connection()

# Get Scanner event and attach to event
scannerevent = check_for_scanner(scannertype)
qrdevice = evdev.InputDevice(scannerevent)
barcode = ""
upper = 0

print ("INFO | Ready for scanning QR Codes")
sys.stdout.flush()

for event in qrdevice.read_loop():
    
    if (event.type == evdev.ecodes.EV_KEY) and (event.value == CONST_KEY_DOWN):
        keyvalue = keys[event.code]
        if event.code == CONST_CAPS: # Event.Code = Caps ==> Next value will be a capital letter
            upper = 1 
        else:
            if upper == 1: # Change letter to capitel letter 
                  keyvalue = keyvalue.upper()
                  upper = 0
            barcode += keyvalue
        
        # Check for QRCode suffix
        if event.code == CONST_ENTER:          
            # Copy barcode to OPCUA topic
            PLC_QR_Code['vals'][0]['id'] = (my_mqtt_client.IDDict.get(params['Variable']))
            PLC_QR_Code['vals'][0]['val'] = barcode
            # Publish MQTT Topic and flush to logs
            PLC_QR_Code_Str = json.dumps(PLC_QR_Code)
            my_mqtt_client.client.publish(plc_qrcode_topic, PLC_QR_Code_Str)
            print("INFO | Scanned code: " + barcode)
            print("INFO | Code published to the following topic: " + PLC_QR_Code_Str)
            sys.stdout.flush()
            barcode = ""
            