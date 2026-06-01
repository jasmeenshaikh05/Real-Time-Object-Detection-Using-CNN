import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Blueprint, Response

from backend.utils.video_stream import generate_stream
from modules.hazard_detection.run_weapon_detection import run_weapon_detection


weapon_bp = Blueprint("weapon", __name__)

@weapon_bp.route("/detect/weapon")
def detect_weapon():

    return Response(
        generate_stream(run_weapon_detection()),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )