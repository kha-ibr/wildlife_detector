import cv2
import time
import os
from datetime import datetime
from ultralytics import YOLO
from gpiozero import MotionSensor

# --- CONFIGURATION ---
PIR_PIN = 18
MODEL_PATH = "yolo26n.pt"
OUTPUT_FOLDER = "detections"
LOG_FILE = "detection_log.txt"
CAPTURE_DURATION = 5
ANIMAL_CLASSES = [14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

# Initialize Hardware/Model
pir = MotionSensor(PIR_PIN)
model = YOLO(MODEL_PATH)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Initialize Log File with Header if it doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("Timestamp,Image,Class,Confidence\n")

def log_to_file(timestamp, filename, label, confidence):
    """Appends a detection row to the text file."""
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp},{filename},{label},{confidence:.2f}\n")

def record_and_analyze():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    
    frames_list = []
    best_conf = 0.0
    detected_class = "Unknown"
    # Capture the start time for the log entry
    log_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"Motion Detected! Recording {CAPTURE_DURATION}s...")
    
    start_time = time.time()
    while (time.time() - start_time) < CAPTURE_DURATION:
        ret, frame = cap.read()
        if not ret:
            break

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        results = model(frame, stream=True, conf=0.4)
        
        for r in results:
            for box in r.boxes:
                if int(box.cls[0]) in ANIMAL_CLASSES:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])
                    
                    # Track the highest confidence animal found in this clip
                    detected_class = "animal"
                    if conf > best_conf:
                        best_conf = conf

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"Animal {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Burn-in Timestamp
        cv2.rectangle(frame, (5, frame_height - 35), (280, frame_height - 5), (0, 0, 0), -1)
        cv2.putText(frame, now, (10, frame_height - 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

        frames_list.append(frame)
        cv2.imshow("Wildlife Cam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Save logic
    if frames_list:
        actual_fps = len(frames_list) / (time.time() - start_time)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_filename = f"animal_vid_{ts}.avi"
        full_path = os.path.join(OUTPUT_FOLDER, video_filename)
         
        out = cv2.VideoWriter(full_path, cv2.VideoWriter_fourcc(*'XVID'), actual_fps, (frame_width, frame_height))
        for f in frames_list:
            out.write(f)
        out.release()
        
        # Log the result of this 10s window
        log_to_file(log_timestamp, video_filename, detected_class, best_conf)
        print(f"Video saved: {video_filename} | Logged as: {detected_class}")

    cap.release()
    cv2.destroyWindow("Wildlife Cam")

# --- MAIN LOOP ---
print("PIR Sensor Warming Up...")
time.sleep(2)
print("System Ready. Waiting for movement...")

try:
    while True:
        pir.wait_for_motion()
        record_and_analyze()
        print("Waiting for next movement...")
        time.sleep(2)
except KeyboardInterrupt:
    print("System Shutdown.")