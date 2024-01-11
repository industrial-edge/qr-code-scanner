# Configure OPC UA Connection

After scanning a QR code its content should be sent to the PLC using the OPC UA Connector. Therefore the OPC UA Connector as well as the Databus need to be configured properly.

- [Configure OPC UA Connection](#configure-opc-ua-connection)
  - [Configuring Databus](#configuring-databus)
  - [Configuring OPC UA Connector](#configuring-opc-ua-connector)

## Configuring Databus

Create the topic in your Databus, which allows you to write to PLCs.
The corresponding Databus topic for writing to your PLC through the OPC UA Connector looks like this: ie/d/j/simatic/v1/opcuac1/dp/w/#

Additionally, the meta data topic ie/m/# needs to be accessible, which is required to properly configure the MQTT connection inside the application. 

Using the wildcard sign **#** you have access to all topics. A user with access to the ie/# topic can therefore access all required topics.

![deploy VFC](./graphics/databus_config.png)

## Configuring OPC UA Connector

In the TIA Portal project the variable **APP_QRCode** in the Datablock **GDB** had been created for receiving the scanned code. Create a new connection - OPC UA for 1500 PLCs - and add the GDB_APP_QRCode to the connection.

![deploy VFC](./graphics/opcua_config.png)
