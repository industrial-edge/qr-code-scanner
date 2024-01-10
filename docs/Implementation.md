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

When using an USB QR code scanner in Linux the scanner is mounted to the generic input event interface located in /dev/input/. In this application example the python-evdev library is used to read the input events of the Industrial Edge Device. The evdev interface passes events generated in the kernel directly to user space through character devices typically located in the mentioned /dev/input/ folder.

The python-evdev libray can be used in your python script by importing evdev: *import evdev*

### Accessing device tree

To enable the access to the input devices, the application needs to have access the `/dev/input` folder of the host system. The input device folder can be added by using the **devices** keyword in the docker-compose file. The dedicated devices will then be mapped to the docker container and can be used by the application.

>**Excerpt from docker-compose.yml**
>
>     scanner-service:
>        build: ./src
>        image: scannerap:1.2.0
>        restart: on-failure
>        mem_limit: 100mb
>        networks:
>            - proxy-redirect
>        volumes:
>            - './publish/:/publish/'
>            - './cfg-data/:/cfg-data/'
>        devices:
>            - '/dev/input:/dev/input'

### Check for dedicated input device

As not all input events should be monitored, but only the events of the QR code scanner the application checks for a device with a dedicated name. The device name can be configured via the [config file](../cfg-data/param.json).

The check is done in the **check_for_scanner** function in the **main.py** script. The function lists all devices provided by the evdev library (list_devices), checks for the scanner name and returns the corresponding event to the main function.

**Excerpt from main.py:**

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

After the QR code is scanned and read by the application it is published to the OPC UA Connector topic of the IE Databus. As the IE Databus is based on a MQTT broker the python library **paho-mqtt** is used to publish values on the IE Databus.

This library can be imported by: **import paho.mqtt.client** **as** **mqtt**

### Initializing MQTT client

Before publishing data to the IE Databus the MQTT client needs to be initialized, the connection to the broker established and the loop for accessing the broker started. As the IE Databus is protected by user and password the credentials need to be set before connecting to the broker.

**Excerpt from main.py:**

```python
     # Set username and password, must be created it databus configurator
        self.client.username_pw_set(self.mqtt_user, self.mqtt_password)
        # Connect to databus
        self.client.connect(self.broker)
        self.client.loop_start()
```

The MQTT connection is handled by the  the `class mqttclient`, which is initialized when creating the class object. All needed parameters are handed over by the class constructor and can be configured using the [config file](../cfg-data/param.json).

**Excerpt from main.py:**

```python
    # Initialize mqtt client object with paramter from the config file and starts the connection to the broker 
    my_mqtt_client = mqttclient('scanner-service',mqtt_broker_server, mqtt_user, mqtt_password, meta_data_topic, connection_name)
    my_mqtt_client.start_connection()
```

### Publishing QR Code

As soon as the suffix (enter character) of the QR code is detected by the application the scanned code is published to IE Databus. The QR code as well as the IE Databus topic are printed to the logs using the **print** and **flush** commands.

**Excerpt from main.py:**

```python
     # Check for QRCode suffix
     if event.code == CONST_ENTER:
        # Copy barcode to OPCUA Connector topic
        PLC_QR_Code['vals'][0]['id'] = (my_mqtt_client.IDDict.get(params['Variable']))
        PLC_QR_Code['vals'][0]['val'] = barcode
        # Publish MQTT Topic and flush to logs
        PLC_QR_Code_Str = json.dumps(PLC_QR_Code)
        my_mqtt_client.client.publish(plc_qrcode_topic, PLC_QR_Code_Str)
        print("INFO | Scanned code: " + barcode)
        print("INFO | Code published to the following topic: " + PLC_QR_Code_Str)
        sys.stdout.flush()
        barcode = ""
```

The MQTT topic of the OPC UA Connector for writing to the PLC uses the following format:

```json 
{
  "seq": 1, 
  "vals": [
      {"id": "", "val": ""}
    ]
} 
```

The sequence number **seq** is optional and has no further value here.
The **vals** structure describes the data block variable of the PLC and consists two entries:

- **id**: Variable id, defined in the meta data of the connection.
- **val**: Value of the variable. In this case the *QR code*.
