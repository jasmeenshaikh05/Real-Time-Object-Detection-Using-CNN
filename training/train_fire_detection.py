import torch
import shutil
import os
from ultralytics import YOLO


def main():

    device = 0 if torch.cuda.is_available() else "cpu"
    print("Using device:", device)

    # load base model
    model = YOLO("yolov8s.pt")

    # train
    results = model.train(
        data="datasets/fire_detection/data.yaml",
        epochs=80,
        imgsz=640,
        batch=8,
        device=device,
        workers=4,
        project="runs/detect",
        name="train_fire"
    )

    # path to best model
    best_model = os.path.join("runs", "detect", "train_fire", "weights", "best.pt")

    # destination path
    dest_model = os.path.join("models", "hazard", "fire_model.pt")

    # copy model
    if os.path.exists(best_model):

        shutil.copy(best_model, dest_model)

        print("Fire model saved to:", dest_model)

    else:

        print("Best model not found!")


if __name__ == "__main__":
    main()