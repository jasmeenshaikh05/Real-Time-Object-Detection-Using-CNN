import cv2
from modules.hazard_detection.crowd_risk_analyzer import CrowdRiskAnalyzer


print("Starting PantherAI Crowd Monitor...")

analyzer = CrowdRiskAnalyzer()


def run_crowd_detection():

    from backend.utils.camera_manager import get_camera

    cap = get_camera()
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    cv2.namedWindow("PantherAI Crowd Monitor", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("PantherAI Crowd Monitor", 1280, 720)


    while True:

        ret, frame = cap.read()

        if not ret:
            break

        count, risk, output = analyzer.predict(frame)

        text = f"People: {count} | {risk}"

        cv2.putText(
            output,
            text,
            (20,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0,255,255),
            3
        )

        yield output


    
    cv2.destroyAllWindows()