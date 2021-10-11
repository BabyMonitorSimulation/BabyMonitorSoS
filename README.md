# BabyMonitorSoS
![sistema](https://github.com/babymonitor-iot/babymonitor-iot/blob/master/babymonitor.png)

## About

This simulator was built with the goal of simulating the baby monitor, smartphone and smart TV devices, considering the relevant functionalities for executing the proposed example in the work: Dealing with IoT Defiant Components. 

## Overview
To test the proposed solution, this web simulator was developed using Flask. The communication is made using RabbitMQ, an open source Message Broker, that uses the AMQP protocol to send messages and provides resources that includes a low message loss.

## Architecture
![arquitetura](https://github.com/babymonitor-iot/babymonitor-iot/blob/master/arquitetura.png)

The simulator architecture is structured in layers, according to the image above. The most external layer is "View", it provides the real time visualization of the messages exchanged and buttons to interact with the system. The "Controller" layer has the methods corresponding to the possible user actions for each device, like connect and disconnect and, for the smartphone and the smart TV, it has the confirm and block/unblock, resepctively. Thus, this layer is used as an interface. The "Model" layer has the data model and business rules for each device. Finally, in "Util" layer are the extra functions that are used by the system, as for the data generation.

In Model layer, there's the sub-layers Publisher and Subscriber, that connect to the broker and send and receive messages, respectively. In "Service" layer are the methods to interact with the Database and in "Business" layer are the business rules.

## Comunication
![comunicacao-entre-sistemas](https://github.com/babymonitor-iot/babymonitor-iot/blob/master/comunication.png)

The configurations used in the broker is shown in the figure above. When a publisher sends a message to the broker, it is sent to an exchange that, through routes previous stablished, forward the message to the queues connected to those routes. The messages that arrive in the queues are delivered to the subscribers linked to them. Thus, for the smart home example, we used only one exchange. Each application stablishes a conection with the respective queue, specifying the routes that will receive the message. 

## Tutorial
### Requirements:
- Python (Version >= 3.7)
- Virtualenv
- SQLite
- Docker

### 1 - Create and activate the virtual enviroment:
Windows
```
virtualenv <virtualenv_name>
<virtualenv_name>\Scripts\activate
```

Ubuntu
```
python3 -m venv <virtualenv_name>
source <virtualenv_name>/bin/activate
```

### 2 - Install modules python:
```
pip install -r requirements.txt
```

### 3 - Execute the project:
#### 3.1 - Run Broker (Docker and RabbitMQ) 
```
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```
#### 3.2 - Execute System BabyMonitor
```
python run.py
```

### Observation:
The broker and System BabyMonitor run in differents terminals.
