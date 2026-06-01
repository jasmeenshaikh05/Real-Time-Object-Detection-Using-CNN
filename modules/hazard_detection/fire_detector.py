import os
from ultralytics import YOLO
from utils.alert_manager import trigger_alert
from utils.sound_alert import play_fire_alarm


class FireDetector:

    def __init__(self):

        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        MODEL_PATH = os.path.join(BASE_DIR, "models", "hazard", "fire_model.pt")

        self.model = YOLO(MODEL_PATH)

        self.FIRE_CLASS = 0
        self.SMOKE_CLASS = 1

        # 🔥 UPDATED threshold
        self.CONF_THRESHOLD = 0.8

    def detect(self, frame):

        results = self.model(
            frame,
            imgsz=960,
            conf=0.25
        )

        for r in results:

            if r.boxes is None:
                continue

            for box in r.boxes:

                cls = int(box.cls[0])
                conf = float(box.conf[0])

                # 🔥 UPDATED condition (>= 0.8)
                if conf < self.CONF_THRESHOLD:
                    continue

                if cls == self.FIRE_CLASS or cls == self.SMOKE_CLASS:

                    play_fire_alarm()

                    # screenshot only, no video
                    trigger_alert(frame, record_video_flag=False)

        return results