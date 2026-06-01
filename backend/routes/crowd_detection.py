import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from flask import Blueprint, Response

from backend.utils.video_stream import generate_stream
from modules.hazard_detection.run_crowd_risk import run_crowd_detection


crowd_bp = Blueprint("crowd", __name__)


@crowd_bp.route("/detect/crowd")
def detect_crowd():

    return Response(
        generate_stream(run_crowd_detection()),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )