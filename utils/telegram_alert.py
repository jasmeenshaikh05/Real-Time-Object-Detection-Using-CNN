import requests

BOT_TOKEN = "8637577046:AAFmb5PfJnfWQ-PLiLk7lNhCIIafzOHV1V8"
CHAT_ID = "6562048894"


def send_telegram_alert(image_path, video_path=None):

    message = "⚠ PantherAI ALERT"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url,data={
        "chat_id": CHAT_ID,
        "text": message
    })

    if image_path:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

        with open(image_path,"rb") as img:
            requests.post(url,data={"chat_id":CHAT_ID},files={"photo":img})

    if video_path:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"

        with open(video_path,"rb") as vid:
            requests.post(url,data={"chat_id":CHAT_ID},files={"video":vid})
