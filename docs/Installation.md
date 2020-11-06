# Installation

- [Installation](#installation)
  - [Configure QR Code Scanner](#configure-qr-code-scanner)
  - [Build application](#build-application)
    - [Cloning image](#cloning-image)
    - [Build docker image](#build-docker-image)
  - [Upload Scanner App to the Industrial Edge Managment](#upload-scanner-app-to-the-industrial-edge-managment)
    - [Connect your Industrial Edge App Publisher](#connect-your-industrial-edge-app-publisher)
    - [Upload Scanner App suing the Industrial Edge App Publisher](#upload-scanner-app-suing-the-industrial-edge-app-publisher)
  - [Deploying of QR Code Scanner Demo](#deploying-of-qr-code-scanner-demo)
    - [Configuring application](#configuring-application)
    - [Create & Deploy configuration file](#create--deploy-configuration-file)
      - [Create configuration](#create-configuration)
      - [Deploy application with configuration file](#deploy-application-with-configuration-file)
  
## Configure QR Code Scanner

The application is desigend for checking for the **enter** character as suffix of the scanned code. The scanner can be configured to add this suffix after each scanned code by scanning the following QR Code. After detecting the suffix character the scanned code is published to the IE Databus and sent to the PLC using the S7 Connector.

**Scan to configure the enter suffix**

![deploy VFC](graphics/suffix.png)

## Build application

### Cloning image

- Clone or Download the source code to your engineering VM

### Build docker image

- Open console in the source code folder
- Use command `docker-compose build` to create the docker image.
- This docker image can now be used to build you app with the Industrial Edge App Publisher
- *docker images | grep scannerapp* can be used to check for the images
- You should get a result similiar to this:

![deploy VFC](./graphics/docker_images_scannerapp.png)

## Upload Scanner App to the Industrial Edge Managment

Please find below a short description how to publish your application in your IEM.

For more detailed information please see the section for [uploading apps to the IEM](https://github.com/industrial-edge/upload-app-to-iem).

### Connect your Industrial Edge App Publisher

- Connect your Industrial Edge App Publisher to your docker engine
- Connect your Industrial Edge App Publisher to your Industrial Edge Managment System

### Upload Scanner App suing the Industrial Edge App Publisher

- Create a new application using the Industrial Publisher
- Add a app new version
- Import the [docker-compose](../docker-compose.yml) file using the **Import YAML** button
- The warning `Build (sevices >> scanner-service) is not supported` can be ignored
- **Start Upload** to transfer the app to Industrial Edge Managment
- Further information about using the Industrial Edge App Publisher can be found in the [IE Hub](https://iehub.eu1.edge.siemens.cloud/documents/appPublisher/en/start.html)

## Deploying of QR Code Scanner Demo

### Configuring application

You can find the configuration file "param.json" in cfg-data folder. This configuration file can be used adjust several parameters of this application. You can see the structure of the file in the following example configuration:

>**param.json**
>
>     {
>        "Scannertype": "Siemens AG MV320",
>        "User": "edge",
>        "Password": "edge",
>        "Topic": "ie/d/j/simatic/v1/s7c1/dp/w/PLC_S7P",
>        "Variable": "GDB.appSignals.APP_QRCode"
>      }

- **Scannertype**: Name of your scanner, which is used in the Linux device tree
- **User**: User of the  S7 Connector databus topic
- **Password**: Password of the  S7 Connector databus topic
- **Topic**: The connection name of the S7 Connector connection, which is used to send the scanned code to the PLC. The topic consists of the default S7 Connector topic `ie/d/j/simatic/v1/s7c1/dp/w` and the *connection name* configured in the S7 Connector Configurator (Here `PLC_S7P`)
- **Variable**: The name of the variable, which is configured in the S7 Connector

Adjust the configuration file depending on your needs.

### Create & Deploy configuration file

#### Create configuration

Once you have successfully uploaded the QR Code Scanner application to your IEM you need to add the mentioned configuration file to your application. You can either choose between version and non versioned configuration files. The non version configuration file will be described in the next steps.
Go to **Applications/** **My Projects** and open the QR Code Scanner application. Here you can create a new configuration file.

**Add** **Configuration**

![deploy VFC](./graphics/add_config_file.png)
**Configure** **Configuration**

![deploy VFC](./graphics/configure_config.png)

#### Deploy application with configuration file

During the deploying process of the application you need to select the configuration file, if needed you can adapt the configuration file before deploying.

**Deploy** **Application**

![deploy VFC](./graphics/deploy_config.png)
