from ultralytics import YOLO
import cv2
from utils.alert_manager import trigger_alert


class WeaponDetector:

    def __init__(self):

        self.weapon_model = YOLO("models/hazard/weapon_model.pt")
        self.person_model = YOLO("yolov8n.pt")

        self.CONF_THRESHOLD = 0.8

    def detect(self, frame, cap):

        weapon_results = self.weapon_model(frame, conf=0.4)
        person_results = self.person_model(frame, classes=[0])

        persons = []
        weapons = []

        for r in person_results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                persons.append(((x1+x2)//2, (y1+y2)//2))

        for r in weapon_results:
            for box in r.boxes:

                conf = float(box.conf[0])

                if conf < self.CONF_THRESHOLD:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                weapon_center = ((x1+x2)//2, (y1+y2)//2)

                weapons.append(weapon_center)

                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)

        for person in persons:
            for weapon in weapons:

                cv2.line(frame, person, weapon, (0,0,255), 2)

                mid_x = (person[0]+weapon[0])//2
                mid_y = (person[1]+weapon[1])//2

                cv2.putText(
                    frame,
                    "Possible Attack",
                    (mid_x, mid_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,0,255),
                    2
                )

                trigger_alert(frame, cap, record_video_flag=True)

        return frame