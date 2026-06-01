import os
from datetime import datetime

def log_event(message):

    os.makedirs("logs", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("logs/events.log","a") as f:
        f.write(f"[{timestamp}] {message}\n")

    print("[LOG]", message)