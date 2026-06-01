import cv2
from modules.hazard_detection.fire_detector import FireDetector

detector = FireDetector()

def run_fire_detection():

    from backend.utils.camera_manager import get_camera

    cap = get_camera()

    # better resolution for small fire detection
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Camera read failed")
            break

        results = detector.detect(frame)

        annotated = results[0].plot()

        yield annotated


    
    cv2.destroyAllWindows()