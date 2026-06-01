import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from flask import Flask
from flask_cors import CORS
from routes.object_detection import object_bp
from routes.weapon_detection import weapon_bp
from routes.fire_detection import fire_bp
from routes.crowd_detection import crowd_bp
from routes.alerts import alerts_bp
from routes.youtube_detection import youtube_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(object_bp)
app.register_blueprint(weapon_bp)
app.register_blueprint(fire_bp)
app.register_blueprint(crowd_bp)
app.register_blueprint(alerts_bp)
app.register_blueprint(youtube_bp)


@app.route("/")
def home():
    return "PantherAI Backend Running"

if __name__ == "__main__":
    app.run(debug=True)