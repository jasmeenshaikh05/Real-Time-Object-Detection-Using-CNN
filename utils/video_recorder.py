import cv2
import time
import os

def record_video(cap, duration=10):

    os.makedirs("alerts", exist_ok=True)

    filename = f"alerts/event_{int(time.time())}.mp4"

    fps = 20
    width = int(cap.get(3))
    height = int(cap.get(4))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    out = cv2.VideoWriter(filename, fourcc, fps, (width,height))

    start = time.time()

    while time.time() - start < duration:

        ret, frame = cap.read()

        if not ret:
            break

        out.write(frame)

    out.release()

    return filename