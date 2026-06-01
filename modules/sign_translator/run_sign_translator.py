import os
import cv2
import time
import torch
import pyttsx3
from ultralytics import YOLO
import mediapipe as mp

# --------------------------------------------------
# MODEL PATH
# --------------------------------------------------

MODEL_PATH = r"D:\PantherAI\runs\detect\runs\detect\sign_language_model\weights\best.pt"

# --------------------------------------------------
# GPU CHECK
# --------------------------------------------------

print("\nChecking hardware...")

if torch.cuda.is_available():
    DEVICE = 0
    print("✅ GPU detected:", torch.cuda.get_device_name(0))
else:
    DEVICE = "cpu"
    print("⚠ Running on CPU")

# --------------------------------------------------
# CHECK MODEL
# --------------------------------------------------

if not os.path.exists(MODEL_PATH):
    print("❌ Model not found")
    exit()

print("✅ Model found")

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

model = YOLO(MODEL_PATH)

print("Classes:", model.names)

# --------------------------------------------------
# SPEECH ENGINE
# --------------------------------------------------

engine = pyttsx3.init('sapi5')
engine.setProperty("rate",150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

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

print("✅ Webcam opened")

# lower resolution to reduce lag
cap.set(cv2.CAP_PROP_FRAME_WIDTH,960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

# large window
cv2.namedWindow("PantherAI Sign Translator", cv2.WINDOW_NORMAL)
cv2.resizeWindow("PantherAI Sign Translator",1400,900)

# --------------------------------------------------
# SPEECH CONTROL
# --------------------------------------------------

last_spoken = ""
last_time = 0
cooldown = 1

# --------------------------------------------------
# FRAME SKIP (reduce lag)
# --------------------------------------------------

frame_count = 0

# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

print("\nTranslator running (ESC to exit)\n")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    detected_label = None
    frame_count += 1

    # --------------------------------------------------
    # YOLO DETECTION (every 3 frames)
    # --------------------------------------------------

    if frame_count % 3 == 0:

        results = model(frame, conf=0.35, imgsz=960, device=DEVICE)

        for r in results:
            for box in r.boxes:

                cls = int(box.cls[0])
                label = model.names[cls]

                x1,y1,x2,y2 = map(int, box.xyxy[0])

                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),3)

                cv2.putText(frame,label,(x1,y1-15),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,(0,255,0),3)

                detected_label = label

    # --------------------------------------------------
    # MEDIAPIPE SKELETON
    # --------------------------------------------------

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_results = hands.process(rgb)

    if mp_results.multi_hand_landmarks:

        for hand in mp_results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

    # --------------------------------------------------
    # SPEECH
    # --------------------------------------------------

    if detected_label:

        speech = detected_label.replace("-", " ")
        speech = speech.replace("_"," ")

        current = time.time()

        if current-last_time > cooldown:

            print("Detected:", speech)

            speak(speech)

            last_spoken = speech
            last_time = current

    # --------------------------------------------------
    # DISPLAY
    # --------------------------------------------------

    cv2.imshow("PantherAI Sign Translator", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# --------------------------------------------------
# CLEANUP
# --------------------------------------------------

cap.release()
cv2.destroyAllWindows()
engine.stop()