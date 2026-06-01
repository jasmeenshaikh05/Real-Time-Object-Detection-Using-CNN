import cv2
import mediapipe as mp
import numpy as np
import joblib
import pyttsx3
from collections import deque

MODEL_PATH = "models/gesture_classifier.pkl"

print("Loading gesture classifier...")

model = joblib.load(MODEL_PATH)

print("Model loaded.")

# --------------------------------------------------
# Speech engine
# --------------------------------------------------

engine = pyttsx3.init('sapi5')
engine.setProperty("rate",150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# --------------------------------------------------
# MediaPipe setup
# --------------------------------------------------

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# --------------------------------------------------
# Webcam
# --------------------------------------------------

cap = cv2.VideoCapture(0)

cv2.namedWindow("PantherAI Sign Translator", cv2.WINDOW_NORMAL)
cv2.resizeWindow("PantherAI Sign Translator",1400,900)

# --------------------------------------------------
# Prediction smoothing
# --------------------------------------------------

pred_buffer = deque(maxlen=10)

last_spoken = ""

print("Translator running... Press ESC to exit")

# --------------------------------------------------
# Main loop
# --------------------------------------------------

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

    while len(landmark_row) < 126:
        landmark_row.append(0)

    if len(landmark_row) == 126:

        X = np.array(landmark_row).reshape(1, -1)

        # same normalization used during training
        X = X - X.mean(axis=1).reshape(-1,1)

        prediction = model.predict(X)[0]

        pred_buffer.append(prediction)

        if len(pred_buffer) == 10:

            final_prediction = max(set(pred_buffer), key=pred_buffer.count)

            cv2.putText(
                frame,
                final_prediction,
                (50,100),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (0,255,0),
                3
            )

            # speak only if gesture changed
            if final_prediction != last_spoken:

                print("Detected:", final_prediction)

                speak(final_prediction.replace("_"," "))

                last_spoken = final_prediction

    cv2.imshow("PantherAI Sign Translator", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
engine.stop()