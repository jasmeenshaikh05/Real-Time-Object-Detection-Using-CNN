import cv2
import numpy as np
import os
from ultralytics import YOLO


class CrowdRiskAnalyzer:

    def __init__(self):

        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        MODEL_PATH = os.path.join(BASE_DIR, "runs", "detect", "train", "weights", "best.pt")
        self.model = YOLO(MODEL_PATH)

        print("Crowd analyzer ready")


    def predict(self, frame):
        frame = cv2.resize(frame, None, fx=1.5, fy=1.5)

        results = self.model.track(
            frame,
            imgsz=1280,
            conf=0.25,
            classes=[0],
            persist=True,
            tracker="bytetrack.yaml"
        )
        boxes = results[0].boxes

        if boxes.id is None:
            count = 0
            centers = []
        else:
            count = len(boxes.id.unique())

            centers = []

            for box in boxes.xyxy:

                x1, y1, x2, y2 = box

                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                centers.append((cx, cy))


        heatmap = self.generate_heatmap(frame, centers)

        risk = self.get_risk_level(count)

        return count, risk, heatmap


    def generate_heatmap(self, frame, centers):

        heatmap = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.float32)

        for x, y in centers:

            cv2.circle(heatmap, (x, y), 60, 1, -1)

        heatmap = cv2.GaussianBlur(heatmap, (0,0), 25)

        heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)

        heatmap = heatmap.astype(np.uint8)

        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        blended = cv2.addWeighted(frame, 0.6, heatmap, 0.4, 0)

        return blended


    def get_risk_level(self, count):

        if count < 5:
            return "SAFE"

        elif count < 15:
            return "MODERATE CROWD"

        elif count < 30:
            return "HIGH DENSITY"

        else:
            return "⚠ STAMPEDE RISK"