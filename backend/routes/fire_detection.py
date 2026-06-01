import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from flask import Blueprint, Response

from backend.utils.video_stream import generate_stream
from modules.hazard_detection.run_fire_detection import run_fire_detection

fire_bp = Blueprint("fire", __name__)

@fire_bp.route("/detect/fire")
def detect_fire():

    return Response(
        generate_stream(run_fire_detection()),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )