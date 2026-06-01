from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO("yolov8n-pose.pt")

cap = cv2.VideoCapture(0)

cv2.namedWindow("Violence Detector", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Violence Detector", 1400, 900)

previous_keypoints = []

MOTION_THRESHOLD = 80
MIN_MOVEMENT = 12
VIOLENT_FRAME_THRESHOLD = 5

violent_frames = 0


while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.resize(frame,(1400,900))

    results = model(frame)

    annotated = results[0].plot()

    persons = []

    if results[0].keypoints is not None:

        for person in results[0].keypoints.xy:

            persons.append(person.cpu().numpy())


    motion_scores = []

    if previous_keypoints and persons:

        for prev,curr in zip(previous_keypoints,persons):

            velocity = np.linalg.norm(curr-prev,axis=1)

            velocity = np.where(velocity < MIN_MOVEMENT,0,velocity)

            motion_score = np.mean(velocity)

            motion_scores.append(motion_score)


    violent_motion = False

    if motion_scores:

        if max(motion_scores) > MOTION_THRESHOLD:

            violent_frames += 1

        else:

            violent_frames = max(0,violent_frames-1)


    previous_keypoints = persons


    if violent_frames >= VIOLENT_FRAME_THRESHOLD:

        violent_motion = True


    if violent_motion:

        cv2.putText(
            annotated,
            "VIOLENT MOTION DETECTED",
            (50,70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0,0,255),
            3
        )


    cv2.imshow("Violence Detector", annotated)

    if cv2.waitKey(1) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()