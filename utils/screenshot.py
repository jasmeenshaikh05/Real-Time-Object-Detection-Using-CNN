import cv2
import time
import os

def save_screenshot(frame):
    os.makedirs("alerts", exist_ok=True)
    filename = f"alerts/event_{int(time.time())}.jpg"
    cv2.imwrite(filename, frame)
    return filename