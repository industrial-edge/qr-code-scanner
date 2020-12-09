# QR Code Scanner App, which sends scanned QR Code to PLC
# Copyright 2020 Siemens AG
# This file is subject to the terms and conditions of the MIT License.  
# See LICENSE file in the top-level directory.
# Date: 22.08.2020

import paho.mqtt.client as mqtt
import evdev
import sys
import os
import time
import json

#============================
# Constants
#============================

MQTT_IP = 'ie-databus'
QR_CODE_TOPIC = 'topic1' 
CONST_CAPS = 42
CONST_ENTER = 28
CONST_KEY_DOWN = 1
keys = "X^1234567890    qwertzuiop    asdfghjkl   : yxcvbnm )                                                                               "

PLC_DATA_FORMAT = {"seq": 1, "vals": {"id": "", "val": ""}}
JSON_PLC_FORMAT = json.dumps(PLC_DATA_FORMAT)
PLC_QR_Code = json.loads(JSON_PLC_FORMAT)

#============================
# Help functions
#============================

# Callback function for connection to MQTT Client
def on_connect(client, userdata, flags, rc):
    print("Connected to " + MQTT_IP + " mqtt broker")

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
PLC_QR_Code['vals']['id'] = params['Variable']
PLC_QR_CODE_TOPIC = params['Topic']

# Initialize MQTT Client
client = mqtt.Client()
# Set username and password, must be created it databus configurator
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
# Add callback functions
client.on_connect = on_connect
# Connect to databus
client.connect(MQTT_IP)
client.loop_start()

# Get Scanner event and attach to event
scannerevent = check_for_scanner(scannertype)
qrdevice = evdev.InputDevice(scannerevent)
barcode = ""
upper = 0

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
            print(barcode)
            # Copy barcode to S7 Connector topic
            PLC_QR_Code['vals']['val'] = barcode
            print(PLC_QR_Code)
            qr_code_json = json.dumps(PLC_QR_Code)
            # Publish MQTT Topic and flush to logs
            client.publish(QR_CODE_TOPIC, barcode)
            client.publish(PLC_QR_CODE_TOPIC, qr_code_json)
            sys.stdout.flush()
            barcode = ""
