# Config
import os
from dotenv import load_dotenv

load_dotenv()

PIR_PIN = 18  
LED_PIN = 17
MODEL_PATH = "models/yolo26n.pt"

OUTPUT_FOLDER = "detections"
LOG_FILE = "detection_log.txt"

CAPTURE_WINDOW = 10

ANIMAL_CLASSES = [14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
PERSON_CLASS = 0

IOTHUB_DEVICE_CONNECTION_STRING = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")