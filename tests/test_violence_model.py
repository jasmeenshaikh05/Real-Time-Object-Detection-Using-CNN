import cv2
import torch
import numpy as np
from torchvision.models.video import r3d_18
from torchvision import transforms
from collections import deque


# Load pretrained video action model
model = r3d_18(pretrained=True)
model.eval()


# Kinetics labels for violent actions
violent_actions = [
    "punching bag",
    "punching person",
    "kicking",
    "headbutting",
    "slapping"
]


# Frame preprocessing
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((112,112))
])


# Buffer to hold frames
frame_buffer = deque(maxlen=16)


cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("videos/fight.mp4")


while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_buffer.append(frame)

    label = "Collecting frames..."
    prob = 0

    if len(frame_buffer) == 16:

        frames = []

        for f in frame_buffer:

            img = transform(f)
            frames.append(img)

        frames = torch.stack(frames)

        frames = frames.permute(1,0,2,3).unsqueeze(0)

        with torch.no_grad():

            outputs = model(frames)

        probs = torch.softmax(outputs,dim=1)

        prob, action = torch.max(probs,1)

        prob = prob.item()

        action = action.item()

        label = f"Action ID: {action}"

        if prob > 0.6:

            label = "Possible Violence"


    color = (0,0,255) if "Violence" in label else (0,255,0)

    cv2.putText(frame,
                f"{label} {prob:.2f}",
                (40,60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                color,
                3)

    cv2.imshow("Violence Detection",frame)

    if cv2.waitKey(1) == 27:
        break


cap.release()
cv2.destroyAllWindows()