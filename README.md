# Connecting USB QR Code Scanner

Connecting an USB based QR Code Scanner to an Industrial Edge Device.

- [Connecting USB QR Code Scanner](#connecting-usb-qr-code-scanner)
  - [Description](#description)
    - [Overview](#overview)
    - [General task](#general-task)
  - [Requirements](#requirements)
    - [Used components](#used-components)
    - [TIA Project](#tia-project)
    - [Configuring PLC Connection](#configuring-plc-connection)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Implementation](#implementation)
  - [Documentation](#documentation)
  - [Contribution](#contribution)
  - [Licence and Legal Information](#licence-and-legal-information)

## Description

### Overview

This application examples shows how to connect a QR Code Scanner via USB to the Industrial Edge Device. The scanned QR Code will be sent to a PLC and displayed in an HMI Panel.

### General task

The application reads the QR Code provided by the scanner and publishes it on the IE Databus to the topic corresponding to the S7 Connector, which sends the data to the PLC. This  topic needs to be created in the IE Databus in advance.
Scanner type, plc tag, databus topic as well as databus credentials can be configured via an external configuration file.

![deploy VFC](docs/graphics/qrcode_task.png)

## Requirements

### Used components

- Industrial Edge App Publisher V1.2.7
- Docker Engine 18.09.6
- Docker Compose V2.4
- S7 Connector V1.2.26
- S7 Connector Configurator V1.2.23
- IE Databus V1.2.16
- IE Databus Configurator V1.2.23
- Industrial Edge Device V1.2.0-56
- QR Code Scanner: SIMATIC MV320
- TIA Portal V16
- PLC: CPU 1518 FW 2.8.3

### TIA Project

The used TIA Portal project can be found in the [miscellaneous repository](https://github.com/industrial-edge/miscellaneous) in the tank application folder and is also used for several further application examples:

- [Tia Tank Application](https://github.com/industrial-edge/miscellaneous/tree/main/tank%20application)
  
### Configuring PLC Connection

Further information about how to configure the S7 Connection to write data to the PLC can be found in the [docs](docs/PLC_connection.md) section

- Configure IE Databus
- Configure S7 Connection

## Installation

You can find the further information about the following steps in the [docs](./docs)

- [Configure QR Code Scanner](docs/Installation.md#configure-qr-code-scanner)
- [Build application](docs/Installation.md#build-application)
- [Upload app to Industrial Edge Management](docs/Installation.md#upload-scanner-app-to-the-industrial-edge-managment)
- [Deploying application to Industrial Edge Device](docs/Installation.md#deploying-of-qr-code-scanner-demo)

## Usage

Plug your SIMATIC MV320 Bar Code Scanner (or any other USB Scanner) to one of the USB Ports of your Industrial Edge Device.

Go to the TIA Portal Project, start the HMI Runtime and scan any available QR Code (e.g the following QR Code). A pop up will appear with the content of the scanned code.

You can also open the GBD data block in the TIA Portal and check the content of the APP_QRCode variable in the app signals structure.

![QR_Code_Industrial_Edge](docs/graphics/qr_code_industrial_edge.png)

## Implementation

How to access the USB based QR Code Scanner inside the application as well as further details about the source code can be found in the [implementation section](docs/Implementation.md).

- [Accessing QR Code Scanner](docs/Implementation.md#accessing-qr-code-scanner) inside the application
- [Publishing QR Code](docs/Implementation.md#accessing-qr-code-scanner) to the IE Databus

## Documentation

- Here is a link to the [docs](docs/) of this application example.
- You can find further documentation and help in the following links
  - [Industrial Edge Hub](https://iehub.eu1.edge.siemens.cloud/#/documentation)
  - [Industrial Edge Forum](https://www.siemens.com/industrial-edge-forum)
  - [Industrial Edge landing page](http://siemens.com/industrial-edge)
  
## Contribution

Thanks for your interest in contributing. Anybody is free to report bugs, unclear documentation, and other problems regarding this repository in the Issues section or, even better, is free to propose any changes to this repository using Merge Requests.

## Licence and Legal Information

Please read the [Legal information](LICENSE.md).
