# Detector
from matplotlib.pyplot import box
from ultralytics import YOLO
from datetime import datetime
import cv2
from config import ANIMAL_CLASSES, PERSON_CLASS


class Detector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def process_frame(self, frame, best_conf):
        results = self.model(frame, conf=0.4, verbose=False)
        r = results[0]

        best_frame = None
        detected_class = None

        if r.boxes is not None:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])

                if conf > best_conf:
                    best_conf = conf

                    if cls_id in ANIMAL_CLASSES:
                        detected_class = "animal"
                    elif cls_id == PERSON_CLASS:
                        detected_class = "person"
                    else:
                        detected_class = "unknown"

                    # Draw label on clean frame
                    clean = frame.copy()
                    x1, y1, x2, y2 = map(int, box.xyxy[0]) # Get coordinates
    
                    # Draw the rectangle
                    cv2.rectangle(clean, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    cv2.putText(clean, f"{detected_class.upper()} {conf:.2f}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                    best_frame = clean

        return best_frame, best_conf, detected_class