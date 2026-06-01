import cv2
import mediapipe as mp
import csv
import os

# --------------------------------------------------
# DATASET PATH
# --------------------------------------------------

DATASET_DIR = "datasets/sign_language_landmarks"
DATASET_FILE = os.path.join(DATASET_DIR, "gesture_dataset.csv")

os.makedirs(DATASET_DIR, exist_ok=True)

# --------------------------------------------------
# ENTER GESTURE NAME
# --------------------------------------------------

gesture_name = input("Enter gesture label: ")

# --------------------------------------------------
# MEDIAPIPE SETUP
# --------------------------------------------------

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# --------------------------------------------------
# CAMERA
# --------------------------------------------------

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Webcam not detected")
    exit()

print("Recording samples for:", gesture_name)

# --------------------------------------------------
# CSV WRITER
# --------------------------------------------------

file_exists = os.path.exists(DATASET_FILE)

with open(DATASET_FILE, "a", newline="") as f:

    writer = csv.writer(f)

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        landmark_row = []

        if results.multi_hand_landmarks:

            for hand in results.multi_hand_landmarks:

                mp_draw.draw_landmarks(
                    frame,
                    hand,
                    mp_hands.HAND_CONNECTIONS
                )

                for lm in hand.landmark:

                    landmark_row.append(lm.x)
                    landmark_row.append(lm.y)
                    landmark_row.append(lm.z)

        # ensure fixed size for two hands
        while len(landmark_row) < 126:
            landmark_row.append(0)

        if len(landmark_row) == 126:

            landmark_row.append(gesture_name)

            writer.writerow(landmark_row)

            print("Sample recorded")

        cv2.imshow("Gesture Data Collection", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            print("Stopping data collection")
            break

cap.release()
cv2.destroyAllWindows()