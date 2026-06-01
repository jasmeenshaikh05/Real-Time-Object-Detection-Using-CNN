import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import cv2
import os
from ultralytics import YOLO

from utils.alert_manager import trigger_alert


# ---------------- PATH FIX ----------------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
WEAPON_MODEL_PATH = os.path.join(BASE_DIR, "models", "hazard", "weapon_model.pt")


# Load models
weapon_model = YOLO(WEAPON_MODEL_PATH)
person_model = YOLO("yolov8n.pt")


def run_weapon_detection():

    # Open webcam
    from backend.utils.camera_manager import get_camera

    cap = get_camera()

    # Window
    cv2.namedWindow("PantherAI Monitor", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("PantherAI Monitor", 1280, 720)

    # Detection parameters
    WEAPON_CONF_THRESHOLD = 0.8
    PERSON_CONF_THRESHOLD = 0.5
    MIN_BOX_AREA = 600


    while True:

        ret, frame = cap.read()

        if not ret:
            break


        frame = cv2.resize(frame, None, fx=1.5, fy=1.5)


        # Run detection models
        weapon_results = weapon_model.predict(frame, conf=0.4, imgsz=960, verbose=False)
        person_results = person_model.predict(frame, conf=0.4, imgsz=960, classes=[0], verbose=False)


        weapon_boxes = []
        person_boxes = []


        # Detect persons
        for box in person_results[0].boxes:

            conf = float(box.conf[0])
            if conf < PERSON_CONF_THRESHOLD:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            person_boxes.append((x1,y1,x2,y2))

            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

            cv2.putText(
                frame,
                f"PERSON {conf:.2f}",
                (x1,y1-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,0),
                2
            )


        # Detect weapons
        for box in weapon_results[0].boxes:

            conf = float(box.conf[0])
            if conf < WEAPON_CONF_THRESHOLD:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            width = x2-x1
            height = y2-y1
            area = width*height

            if area < MIN_BOX_AREA:
                continue

            weapon_boxes.append((x1,y1,x2,y2))

            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),3)

            cv2.putText(
                frame,
                f"WEAPON {conf:.2f}",
                (x1,y1-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,0,255),
                2
            )


        attack_detected = False


        # Draw line between weapon and person
        for px1,py1,px2,py2 in person_boxes:

            pcx = (px1+px2)//2
            pcy = (py1+py2)//2

            for wx1,wy1,wx2,wy2 in weapon_boxes:

                wcx = (wx1+wx2)//2
                wcy = (wy1+wy2)//2

                cv2.line(frame,(pcx,pcy),(wcx,wcy),(0,0,255),3)

                midx = (pcx+wcx)//2
                midy = (pcy+wcy)//2

                cv2.putText(
                    frame,
                    "POSSIBLE ATTACK",
                    (midx,midy),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0,0,255),
                    3
                )

                attack_detected = True


        # ALERT ONLY when attack line exists
        if attack_detected:

            trigger_alert(frame, cap, record_video_flag=True)

            cv2.putText(
                frame,
                "⚠ POSSIBLE ATTACK",
                (40,60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.3,
                (0,0,255),
                3
            )


        yield frame


        if cv2.waitKey(1) & 0xFF == 27:
            break


    
    cv2.destroyAllWindows()