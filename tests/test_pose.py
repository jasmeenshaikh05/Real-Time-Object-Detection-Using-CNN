from ultralytics import YOLO
import cv2


# load pose model
model = YOLO("yolov8n-pose.pt")


# open webcam
cap = cv2.VideoCapture(0)


while True:

    ret, frame = cap.read()

    if not ret:
        break


    # run pose detection
    results = model(frame)


    # draw skeleton
    annotated = results[0].plot()


    # show frame
    cv2.imshow("Pose Detection", annotated)


    # press ESC to exit
    if cv2.waitKey(1) == 27:
        break


cap.release()
cv2.destroyAllWindows()