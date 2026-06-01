import cv2
from modules.hazard_detection.crowd_density_estimator import CrowdDensityEstimator


estimator = CrowdDensityEstimator()

cap = cv2.VideoCapture(0)


while True:

    ret, frame = cap.read()

    if not ret:
        break


    result = estimator.estimate(frame)

    text = f"Crowd: {result['count']}  Density: {result['level']}"

    cv2.putText(frame,text,(10,30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,(0,255,255),2)

    cv2.imshow("Crowd Density",frame)


    if cv2.waitKey(1) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()