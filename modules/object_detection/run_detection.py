import cv2

from modules.object_detection.detector import ObjectDetector
from modules.object_detection.tracker import Tracker
from modules.object_detection.analytics import Analytics


import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
MODEL_PATH = os.path.join(BASE_DIR, "runs", "detect", "train", "weights", "best.pt")


detector = ObjectDetector(MODEL_PATH)
tracker = Tracker()
analytics = Analytics()


def run_object_detection():

    from backend.utils.camera_manager import get_camera

    cap = get_camera()

    # improve webcam resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


    while True:

        ret, frame = cap.read()

        if not ret:
            break


        # run detection
        results = detector.detect(frame)


        # draw bounding boxes
        annotated_frame = results[0].plot()


        # update tracker
        detections = tracker.update(results)


        # update analytics
        analytics.update(detections)


        counts = analytics.get_counts()

        y = 30

        for k, v in counts.items():

            cv2.putText(
                annotated_frame,
                f"{k}: {v}",
                (10, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )

            y += 30


        yield annotated_frame


    
    cv2.destroyAllWindows()