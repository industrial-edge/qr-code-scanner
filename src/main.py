# QR Code Scanner App, which sends scanned QR Code to PLC
# Copyright 2020 Siemens AG
# This file is subject to the terms and conditions of the MIT License.  
# See LICENSE file in the top-level directory.
# Date: 05.05.2021

import paho.mqtt.client as mqtt
from createDict import getDict
import evdev
import sys
import os
import time
import json

class mqttsettings:

    def __init__(self,clientname,broker,topic, plc_connection):
        
        self.IDDict = {}
        self.broker = broker
        self.metaDataTopic = topic
        self.plc_connection = plc_connection
        self.clientname = clientname
        self.client = mqtt.Client(self.clientname)
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message        
        
    # Callback function for connection to MQTT Client
    def on_message(self, client, userdata, message):
        msg = message.payload.decode("utf-8")
        print("[INFO] New message received: " + msg)
        sys.stdout.flush()        
        self.IDDict = getDict(msg, self.plc_connection) 

    def on_connect(self, client, userdata, flags, rc):
        print("[INFO] Connected to " + self.broker + "MQTT broker")
        print("[INFO] Subscribe to " + self.metaDataTopic + " topic")
        sys.stdout.flush()
        self.client.subscribe(self.metaDataTopic)
      
    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("[INFO] On subscribe callback executed")
        sys.stdout.flush()

    def start_connection(self):
        print("[INFO] Start connection to " + self.broker + " broker")
        sys.stdout.flush()

        MQTT_USER = 'edge'
        MQTT_PASSWORD = 'edge'
        
        self.client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        self.client.connect(self.broker)
        self.client.loop_start()

#============================
# Constants
#============================

MQTT_IP = 'ie-databus'
QR_CODE_TOPIC = 'topic1'
META_DATA_TOPIC = "ie/m/#"
CONST_CAPS = 42
CONST_ENTER = 28
CONST_KEY_DOWN = 1
keys = "X^1234567890    qwertzuiop    asdfghjkl   : yxcvbnm )                                                                               "
PLC_DATA_FORMAT = {"seq": 1, "vals": [{"id": "", "val": ""}]}
JSON_PLC_FORMAT = json.dumps(PLC_DATA_FORMAT)
PLC_QR_Code = json.loads(JSON_PLC_FORMAT)

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

def read_parameter(jsonfile):
    with open(jsonfile) as params:
        data = json.load(params)
        return data

#============================
# Main Function
#============================

# Read parameter file
params = read_parameter('/cfg-data/param.json')
scannertype = (params['Scannertype'])
MQTT_USER = params['User']
MQTT_PASSWORD = params['Password']
PLC_QR_CODE_TOPIC = params['Topic']

my_mqtt_class = mqttsettings('scanner-service',MQTT_IP, META_DATA_TOPIC, 'PLC_S7')
my_mqtt_class.start_connection()

# Get Scanner event and attach to event
scannerevent = check_for_scanner(scannertype)
qrdevice = evdev.InputDevice(scannerevent)
barcode = ""
upper = 0

print ("[INFO] Ready for scanning QR Codes")
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
            
            # Copy barcode to S7 Connector topic
            PLC_QR_Code['vals'][0]['id'] = (my_mqtt_class.IDDict.get(params['Variable']))
            PLC_QR_Code['vals'][0]['val'] = barcode
            print("[INFO] Scanned code: " + barcode)
            print("[INFO] Code published to the following topic: " + barcode)
            sys.stdout.flush()

            # Publish MQTT Topic and flush to logs
            qr_code_json = json.dumps(PLC_QR_Code)
            my_mqtt_class.client.publish(QR_CODE_TOPIC, barcode)
            my_mqtt_class.client.publish(PLC_QR_CODE_TOPIC, qr_code_json)
            barcode = ""