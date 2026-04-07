# wildlife_detector
User Manual: AI-Powered Wildlife Monitoring System
## 1. System Overview

The Wildlife Detector is an edge-computing solution that uses a Raspberry Pi and a YOLOv8 AI model to monitor outdoor areas.

Detection: A PIR (Passive Infrared) sensor triggers the camera.

Analysis: The system identifies if the subject is an "animal."

Alerts: A physical Red LED provides a visual signal on the device.

Cloud Sync: Detection metadata is sent to Azure IoT Hub for long-term storage and analysis.

## 2. Hardware Setup

To assemble the device, connect the components to the Raspberry Pi GPIO pins as follows:
Wiring Diagram
Component	Raspberry Pi Pin	Description
PIR Sensor (VCC)	5V (Pin 2 or 4)	Power input
PIR Sensor (OUT)	GPIO 18	Motion trigger signal
PIR Sensor (GND)	Ground (Pin 6 or 9)	Ground
Red LED (+)	GPIO 24	Alert signal (Use 220Ω Resistor)
Red LED (-)	Ground	Ground
USB Camera	USB Port	Standard USB 2.0/3.0 port
3. Software Installation

Before running the system, ensure the environment is configured on your Raspberry Pi, clone the Repository.

    git clone https://github.com/kha-ibr/wildlife_detector.git
    cd wildlife_detector

Set up Virtual Environment:

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

Configure Credentials:
Create a .env file in the root folder and add your Azure Connection String:

    IOTHUB_DEVICE_CONNECTION_STRING="HostName=YourHub.azure-devices.net;DeviceId=YourDevice;SharedAccessKey=..."

## 4. Operational Instructions
Starting the Monitor

To start the system, run the main script:

    python3 main.py

### System Behavior

Standby: The system waits for the PIR sensor to detect heat/motion.

Capture: Upon motion, the camera scans for 10 seconds to find the best shot of an animal.

Classification: If an Animal is found: The Red LED turns on for  20 seconds, and data is sent to Azure. If no animal is found: No LED triggers, and the event is ignored.

## 5. Viewing Data (Azure Cloud)

To verify that the system is successfully syncing data, use the Azure CLI or Portal

    az iot hub monitor-events --hub-name [YourHubName]

### Storage Browser:

Navigate to your Azure Storage Account.
Go to Containers > telemetry-logs.
You will find .json files containing the timestamp, label, and confidence score of each detection.
