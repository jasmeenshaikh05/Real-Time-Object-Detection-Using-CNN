import cv2

from modules.object_detection.detector import ObjectDetector
from modules.object_detection.tracker import Tracker
from modules.hazard_detection.crowd_density_estimator import CrowdDensityEstimator


MODEL_PATH = "runs/detect/train/weights/best.pt"


print("Loading models...")

detector = ObjectDetector(MODEL_PATH)
tracker = Tracker()
crowd = CrowdDensityEstimator()


print("Opening webcam...")

cap = cv2.VideoCapture(0)


while True:

    ret, frame = cap.read()

    if not ret:
        break


    results = detector.detect(frame)

    detections = tracker.update(results)

    analysis = crowd.estimate(detections)


    text = f"Crowd: {analysis['count']} Density: {analysis['level']}"

    cv2.putText(
        frame,
        text,
        (10,30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,255,255),
        2
    )

    cv2.imshow("Crowd Analysis", frame)


    if cv2.waitKey(1) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()