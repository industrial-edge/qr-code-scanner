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
  - [License and Legal Information](#license-and-legal-information)
  - [Disclaimer](#disclaimer)

## Description

### Overview

This application examples shows how to connect a QR Code Scanner via USB to the Industrial Edge Device. The scanned QR Code will be sent to a PLC and displayed in an HMI Panel.

### General task

The application reads the QR Code provided by the scanner and publishes it on the IE Databus to the topic corresponding to the S7 Connector, which sends the data to the PLC. This  topic needs to be created in the IE Databus in advance.
Scanner type, plc tag, databus topic as well as databus credentials can be configured via an external configuration file.

![deploy VFC](docs/graphics/qrcode_task.png)

## Requirements

### Used components

- Industrial Edge App Publisher V1.2.8
- Docker Engine 18.09.6
- Docker Compose V2.4
- Simatic S7 Connector V1.8.10-16
- Common Connector Configurator V1.8.1-4
- Databus V2.1.0-4
- Databus Configurator V2.0.0-5
- Industrial Edge Device V1.10.0-9
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

You can find the further information about the following steps in the [docs](./docs/Installation.md)

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
 
- You can find further documentation and help in the following links
  - [Industrial Edge Hub](https://iehub.eu1.edge.siemens.cloud/#/documentation)
  - [Industrial Edge Forum](https://www.siemens.com/industrial-edge-forum)
  - [Industrial Edge landing page](https://new.siemens.com/global/en/products/automation/topic-areas/industrial-edge/simatic-edge.html)
  - [Industrial Edge GitHub page](https://github.com/industrial-edge)
  - [Industrial Edge documentation page](https://docs.eu1.edge.siemens.cloud/index.html)
  
## Contribution

Thank you for your interest in contributing. Anybody is free to report bugs, unclear documentation, and other problems regarding this repository in the Issues section.
Additionally everybody is free to propose any changes to this repository using Pull Requests.

If you are interested in contributing via Pull Request, please check the [Contribution License Agreement](Siemens_CLA_1.1.pdf) and forward a signed copy to [industrialedge.industry@siemens.com](mailto:industrialedge.industry@siemens.com?subject=CLA%20Agreement%20Industrial-Edge).

## License and Legal Information

Please read the [Legal information](LICENSE.txt).

## Disclaimer

IMPORTANT - PLEASE READ CAREFULLY:

This documentation describes how you can download and set up containers which consist of or contain third-party software. By following this documentation you agree that using such third-party software is done at your own discretion and risk. No advice or information, whether oral or written, obtained by you from us or from this documentation shall create any warranty for the third-party software. Additionally, by following these descriptions or using the contents of this documentation, you agree that you are responsible for complying with all third party licenses applicable to such third-party software. All product names, logos, and brands are property of their respective owners. All third-party company, product and service names used in this documentation are for identification purposes only. Use of these names, logos, and brands does not imply endorsement.