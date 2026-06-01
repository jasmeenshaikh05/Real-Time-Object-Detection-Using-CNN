from backend.utils.alert_store import add_alert
import threading
import time

from utils.telegram_alert import send_telegram_alert
from utils.screenshot import save_screenshot
from utils.video_recorder import record_video


# ✅ GLOBAL COOLDOWN (increased)
ALERT_COOLDOWN = 15  # seconds (you can set 10–20 based on demo)

last_alert_time = 0


def trigger_alert(frame, cap=None, record_video_flag=True):

    global last_alert_time

    current_time = time.time()

    # ✅ prevent global spam
    if current_time - last_alert_time < ALERT_COOLDOWN:
        return

    last_alert_time = current_time

    screenshot = save_screenshot(frame)

    # dashboard alert
    add_alert("⚠ Threat detected")

    def background_task():

        if record_video_flag and cap is not None:

            video = record_video(cap)

            send_telegram_alert(screenshot, video)

            add_alert("📤 Telegram alert sent (video + screenshot)")

        else:

            send_telegram_alert(screenshot)

            add_alert("📤 Telegram alert sent (screenshot)")

    # run alert in background (prevents lag)
    threading.Thread(target=background_task, daemon=True).start()