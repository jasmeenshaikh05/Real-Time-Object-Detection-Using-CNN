from ultralytics import YOLO


class ObjectDetector:

    def __init__(self, model_path):

        print("Loading model:", model_path)

        self.model = YOLO(model_path)

    def detect(self, frame):

        results = self.model.track(
            frame,
            conf=0.08,          # lower confidence → detect small objects
            iou=0.5,
            imgsz=960,          # higher resolution → better small object detection
            persist=True,
            tracker="bytetrack.yaml"
        )

        return results