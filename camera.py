# Camera
import cv2
import time


def capture_window(cap, detector, duration):
    best_frame = None
    best_conf = 0.0
    detected_class = "non-animal"

    start_time = time.time()

    while (time.time() - start_time) < duration:
        ret, frame = cap.read()
        if not ret: break

        # Pass the CURRENT best_conf so the detector knows the score to beat
        frame_result, new_conf, cls = detector.process_frame(frame, best_conf)

        # ONLY update if the detector actually found a better frame
        if frame_result is not None:
            best_frame = frame_result
            best_conf = new_conf
            detected_class = cls

    return best_frame, best_conf, detected_class