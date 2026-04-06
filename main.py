# Main
import cv2
import time
import os
import threading # For non-blocking LED
from datetime import datetime
from gpiozero import MotionSensor, LED # Added LED

import config
from detector import Detector
from camera import capture_window
from logger import init_storage, log_to_file
from telemetry import send_telemetry

# --- INIT ---
pir = MotionSensor(config.PIR_PIN)
red_led = LED(config.LED_PIN) # Initialize LED
detector = Detector(config.MODEL_PATH)

init_storage(config.OUTPUT_FOLDER, config.LOG_FILE)

print(f"System Ready. PIR: Pin {config.PIR_PIN}, LED: Pin {config.LED_PIN}")

def trigger_led():
    """Background task to turn on LED for 2 seconds."""
    red_led.on()
    time.sleep(20)
    red_led.off()

def handle_event():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera error")
        return

    print(f"Motion! Searching best shot ({config.CAPTURE_WINDOW}s)...")

    best_frame, best_conf, detected_class = capture_window(
        cap, detector, config.CAPTURE_WINDOW
    )

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- FILTER: ONLY PROCEED IF IT IS AN ANIMAL ---
    if best_frame is not None and detected_class == "animal":
        
        # 1. Physical Alert (LED) in background thread
        threading.Thread(target=trigger_led, daemon=True).start()

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"animal_{ts}.jpg" # Simplified name
        path = os.path.join(config.OUTPUT_FOLDER, filename)

        # 2. Local Save
        cv2.imwrite(path, best_frame)
        log_to_file(config.LOG_FILE, timestamp, filename, "animal", best_conf)
        print(f"Animal Saved: {filename} ({best_conf:.2f})")

        # 3. Cloud Sync
        print("Sending data to Azure IoT Hub...")
        send_telemetry(timestamp, filename, "animal", best_conf)

    elif best_frame is not None:
        print(f"Detection ignored: {detected_class} is not an animal.")
    else:
        print("No detection")

    cap.release()
    cv2.destroyAllWindows()


# --- MAIN LOOP ---
try:
    while True:
        pir.wait_for_motion()
        handle_event()
        time.sleep(2)

except KeyboardInterrupt:
    print("Exit.")