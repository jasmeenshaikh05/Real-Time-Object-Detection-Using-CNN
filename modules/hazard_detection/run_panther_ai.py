from ultralytics import YOLO
import cv2
import time

from utils.screenshot import save_screenshot
from utils.video_recorder import record_video
from utils.telegram_alert import send_alert
from utils.logger import log_event


# Load models
weapon_model = YOLO("models/hazard/weapon_model.pt")
person_model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)

cv2.namedWindow("PantherAI", cv2.WINDOW_NORMAL)
cv2.resizeWindow("PantherAI", 1400, 800)

ALERT_COOLDOWN = 20
last_alert_time = 0


while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1280, 720))

    # ---------------- WEAPON DETECTION ----------------

    weapon_results = weapon_model.predict(
        frame,
        conf=0.3,
        imgsz=1280,
        device=0,
        verbose=False
    )

    # ---------------- PERSON DETECTION ----------------

    person_results = person_model.predict(
        frame,
        conf=0.4,
        imgsz=640,
        device=0,
        verbose=False
    )

    weapons = []
    persons = []
    high_conf_weapon = False

    # -------- PROCESS WEAPONS --------

    for box in weapon_results[0].boxes:

        cls = int(box.cls[0])

        if cls == 1:

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])

            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            weapons.append((cx, cy, conf))

            if conf >= 0.70:
                high_conf_weapon = True

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)

            cv2.putText(frame,
                        f"WEAPON {conf:.2f}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 255),
                        2)

    # -------- PROCESS PERSONS --------

    for box in person_results[0].boxes:

        cls = int(box.cls[0])

        if cls == 0:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            persons.append((cx, cy, x1, y1, x2, y2))

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # -------- MATCH WEAPON WITH PERSON --------

    attack_detected = False

    for wx, wy, conf in weapons:

        for px, py, x1, y1, x2, y2 in persons:

            if x1 < wx < x2 and y1 < wy < y2:

                attack_detected = True

                cv2.line(frame, (wx, wy), (px, py), (0, 0, 255), 2)

                cv2.putText(frame,
                            "PERSON WITH WEAPON",
                            (x1, y2 + 20),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 0, 255),
                            2)

    # -------- ALERT TEXT --------

    if weapons:

        cv2.putText(frame,
                    "WEAPON DETECTED",
                    (40, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2)

    if attack_detected:

        cv2.putText(frame,
                    "POSSIBLE ATTACK",
                    (40, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2)

    # -------- ALERT SYSTEM --------

    if high_conf_weapon and time.time() - last_alert_time > ALERT_COOLDOWN:

        screenshot = save_screenshot(frame)

        video = record_video(cap, 10)

        log_event("High confidence weapon detected")

        send_alert(screenshot, video)

        last_alert_time = time.time()

    # -------- DISPLAY --------

    cv2.imshow("PantherAI", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()