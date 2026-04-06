import threading
import json
from azure.iot.device import IoTHubDeviceClient, Message
import config

# Create global client
client = IoTHubDeviceClient.create_from_connection_string(
    config.IOTHUB_DEVICE_CONNECTION_STRING,
    websockets=True
)

client.connect()


def _async_send(timestamp, filename, label, confidence):
    try:
        data = {
            "timestamp": timestamp,
            "file": filename,
            "label": label,
            "conf": round(confidence, 4)
        }

        msg = Message(json.dumps(data))
        msg.content_encoding = "utf-8"
        msg.content_type = "application/json"

        print(f"Sending telemetry: {data}")

        client.send_message(msg)

        print("Telemetry sent!")

    except Exception as e:
        print(f"MQTT Error: {e}")


def send_telemetry(timestamp, filename, label, confidence):
    '''thread = threading.Thread(
        target=_async_send,
        args=(timestamp, filename, label, confidence)
    )
    thread.start()'''
    _async_send(timestamp, filename, label, confidence)
    return True