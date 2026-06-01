from ultralytics import YOLO
import cv2
import numpy as np

# Load pose model
model = YOLO("yolov8n-pose.pt")

# Webcam or video
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("videos/test.mp4")

cv2.namedWindow("PantherAI Strike Detector", cv2.WINDOW_NORMAL)
cv2.resizeWindow("PantherAI Strike Detector", 1400, 900)

previous_extensions = []
strike_frames = 0

# Tuned parameters
EXTENSION_SPEED_THRESHOLD = 35
MIN_EXTENSION = 40
STRIKE_FRAME_THRESHOLD = 3

while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1400, 900))

    results = model(frame)

    annotated = results[0].plot()

    persons = []

    if results[0].keypoints is not None:
        for person in results[0].keypoints.xy:

            kp = person.cpu().numpy()

            shoulder = kp[6]  # right shoulder
            elbow = kp[8]     # right elbow
            wrist = kp[10]    # right wrist
            hip = kp[12]
            knee = kp[14]

            persons.append((shoulder, elbow, wrist, hip, knee))

    extensions = []

    for p in persons:

        shoulder, elbow, wrist, hip, knee = p

        # Ignore seated people
        if knee[1] < hip[1]:
            continue

        extension = np.linalg.norm(wrist - shoulder)

        extensions.append(extension)

        x, y = int(wrist[0]), int(wrist[1])
        cv2.circle(annotated, (x, y), 6, (0,255,255), -1)

    violent_motion = False

    if previous_extensions and extensions:

        for prev, curr in zip(previous_extensions, extensions):

            extension_speed = abs(curr - prev)

            if curr > MIN_EXTENSION and extension_speed > EXTENSION_SPEED_THRESHOLD:
                strike_frames += 1
            else:
                strike_frames = max(0, strike_frames - 1)

    previous_extensions = extensions

    if strike_frames >= STRIKE_FRAME_THRESHOLD:
        violent_motion = True

    if violent_motion:

        cv2.putText(
            annotated,
            "⚠ POSSIBLE STRIKE DETECTED",
            (40,70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0,0,255),
            3
        )

    cv2.imshow("PantherAI Strike Detector", annotated)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()