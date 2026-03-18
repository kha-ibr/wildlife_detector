import os
import time
import cv2
import torch
from datetime import datetime
from picamera2 import Picamera2

# --- CONFIG ---
SAVE_DIR = "./captures"
RESULTS_DIR = "./results"
MODEL_PATH = "models/md_v5a.0.0.pt"
CONF_THRESHOLD = 0.4
INFERENCE_SIZE = 320

# Ensure directories exist
os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# --- CAMERA INIT ---
picam2 = Picamera2()
config = picam2.create_preview_configuration()
picam2.configure(config)
picam2.start()
time.sleep(2)  # camera warmup

# --- CAPTURE PHOTO (no AI) ---
def capture_photo():
    print("\n=== CAPTURING PHOTO ===")
    frame = picam2.capture_array()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(SAVE_DIR, f"photo_{timestamp}.jpg")
    cv2.imwrite(filename, frame)
    print(f"Photo saved to {filename}\n")
    return filename

# --- LOAD YOLOv5 MODEL ---
def load_model():
    print("Loading YOLOv5 model...")
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH)
    model.conf = CONF_THRESHOLD
    return model

# --- ANALYZE AND SAVE RESULTS ---
def analyze_and_save(image_path, model):
    log_path = os.path.join(RESULTS_DIR, "detection_log.txt")
    with open(log_path, "a") as log_file:
        log_file.write("Timestamp,Image,Class,Confidence\n")

        print("=== ANALYSIS STARTED ===")
        img = cv2.imread(image_path)
        results = model(img, size=INFERENCE_SIZE)

        # Annotated image
        annotated = results.render()[0]
        annotated_path = os.path.join(RESULTS_DIR, "annotated_" + os.path.basename(image_path))
        cv2.imwrite(annotated_path, annotated)

        # Log predictions
        for *box, conf, cls in results.xyxy[0].tolist():
            class_name = model.names[int(cls)]
            confidence = round(conf, 2)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{timestamp},{os.path.basename(image_path)},{class_name},{confidence}\n")

        # Display annotated frame
        display = annotated[:, :, ::-1]
        cv2.imshow("Detection", display)
        cv2.waitKey(3000)  # show for 3 seconds
        cv2.destroyAllWindows()

        print(f"=== ANALYSIS FINISHED ===\nResults saved in {RESULTS_DIR}")

# --- MAIN ---
photo_path = capture_photo()
time.sleep(1)  # optional pause
model = load_model()
analyze_and_save(photo_path, model)

# --- CLEANUP ---
picam2.stop()