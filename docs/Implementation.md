# Implementation

- [Implementation](#implementation)
  - [Accessing QR Code Scanner](#accessing-qr-code-scanner)
    - [Accessing input events](#accessing-input-events)
    - [Accessing device tree](#accessing-device-tree)
    - [Check for dedicated input device](#check-for-dedicated-input-device)
  - [Publishing Code to Databus](#publishing-code-to-databus)
    - [Initializing MQTT client](#initializing-mqtt-client)
    - [Publishing QR Code](#publishing-qr-code)

## Accessing QR Code Scanner

### Accessing input events

Using an USB QR Code Scanner in Linux the Scanner is mounted to the generic input event interface located in /dev/input/. In this application example the python-evdev library is used to read the input events of the Industrial Edge Device. The evdev interface passes events generated in the kernel directly to userspace through character devices typically located in the mentioned /dev/input/ folder.

The python-evdev libray can be used in your python script by importing evdev: *import evdev*

### Accessing device tree

To enable the access to the hosts devices, the application needs to run in priviledge mode. The priviledge mode needs to be enable in the docker-compose file by adding the **privileged:** **true** option to the corresponding service.

>**Excerpt from docker-compose.yml**
>
>     scanner-service:
>        build: .
>        image: scannerap:1.0.0
>        restart: on-failure
>        privileged: true
>        mem_limit: 100mb
>        networks:
>            - proxy-redirect
>        volumes:
>            - './publish/:/publish/'
>            - './cfg-data/:/cfg-data/'

### Check for dedicated input device

As not all input events should be monitored, but only the events of the QR Code Scanner the application checks for a device with a dedicated name. The device name can be configured via the configuration file.

The check is done in the **check_for_scanner** function in the **main.py** script. The function lists all devices provided by the evdev libray (list_devices), checks for the scanner name and returns the corresponding event to the main function

**Excerpt from main.py**

```python
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
```

## Publishing Code to Databus

After the QR Code is scanned and read by the application it is published to the S7 Connector topic of the IE Databus. As the IE Databus is based on a MQTT Broker the python library **paho-mqtt** is used to publish values on the IE Databus.

This library can be import by: **import paho.mqtt.client** **as** **mqtt**

### Initializing MQTT client

Before publishing data to the IE Databus the MQTT Client needs to be initialized, the connection to the broker established and the loop for accessing the broker started. As the IE Databus is protected by user and password the credentials needs to be set before connection to the broker.

**Excerpt from main.py**

```python
     # Initialize MQTT Client
     client = mqtt.Client()
     # Set username and password, must be created it databus configurator
     client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
     # Add callback functions
     client.on_connect = on_connect
     # Connect to databus
     client.connect(MQTT_IP)
     client.loop_start()
```

### Publishing QR Code

As soon as the suffix (enter character) of the QR Code is detected by the application the scanned code is published to IE Databus. The QR Code as well as the IE Databus topic are printed to the logs using the **print** and **flush** commands.

**Excerpt from main.py**

```python
     # Check for QRCode suffix
     if event.code == CONST_ENTER:
         # Check for QRCode suffix
         # Copy barcode to S7 Connector topic
         PLC_QR_Code['vals']['val'] = barcode
         print(PLC_QR_Code)
         qr_code_json = json.dumps(PLC_QR_Code)
         # Publish MQTT Topic and flush to logs
         client.publish(QR_CODE_TOPIC, barcode)
         client.publish(PLC_QR_CODE_TOPIC, qr_code_json)
         sys.stdout.flush()
         barcode = ""
```

The mqtt topic of the S7 Connector uses the following format: *{"seq": 1, "vals": {"id": "", "val": ""}}*.
The sequence number **seq** is optional and has no further value here.

The **vals** structure describes the datablock variable of the PLC and consinst the

- **id**: Variable name, defined in the S7 Connector. In this case *GDB_appSignals_APP_QRCode*
- **val**: Value of the variable. In this case the *QR Code*.
