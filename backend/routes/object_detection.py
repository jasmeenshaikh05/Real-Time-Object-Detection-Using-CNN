import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from flask import Blueprint, Response

from backend.utils.video_stream import generate_stream
from modules.object_detection.run_detection import run_object_detection

object_bp = Blueprint("object", __name__)

@object_bp.route("/detect/object")
def detect_object():

    return Response(
        generate_stream(run_object_detection()),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )