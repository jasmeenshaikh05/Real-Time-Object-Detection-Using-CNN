import torch
from ultralytics import YOLO

torch.backends.cudnn.benchmark = True

def main():

    print("Starting PantherAI Weapon Detection Training")

    model = YOLO("yolov8s.pt")

    model.train(

        # dataset
        data="datasets/weapon_detection/data.yaml",

        # training schedule
        epochs=60,
        patience=10,

        # image size
        imgsz=640,

        # GPU
        batch=16,
        device=0,
        amp=True,

        # dataloader
        workers=8,
        cache=False,

        # optimizer
        optimizer="AdamW",
        lr0=0.001,
        cos_lr=True,

        # logging
        project="runs/detect",
        name="weapon_detector",

        save=True
    )

    print("Training Finished")

if __name__ == "__main__":
    main()