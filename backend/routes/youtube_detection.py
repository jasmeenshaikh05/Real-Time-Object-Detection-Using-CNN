import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from flask import Blueprint, Response, request
import yt_dlp
import cv2

youtube_bp = Blueprint("youtube", __name__)


def download_video(url):

    ydl_opts = {
        'format': 'mp4',
        'outtmpl': 'temp_video.mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return "temp_video.mp4"


def generate_frames(video_path):

    cap = cv2.VideoCapture(video_path)

    while True:

        success, frame = cap.read()
        if not success:
            break

        # 🔥 You can plug ANY detector here
        # For now just show raw frames

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()


@youtube_bp.route("/detect/youtube")
def youtube_detect():

    url = request.args.get("url")

    video_path = download_video(url)

    return Response(
        generate_frames(video_path),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )