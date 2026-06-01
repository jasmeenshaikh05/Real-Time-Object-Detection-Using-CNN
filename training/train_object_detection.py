import torch
from ultralytics import YOLO


def main():

    print("\n========== PantherAI Training ==========\n")
    print("Checking GPU availability...\n")

    if torch.cuda.is_available():

        device = 0
        gpu_name = torch.cuda.get_device_name(0)

        print("GPU detected:", gpu_name)
        print("Using GPU for training\n")

    else:

        device = "cpu"
        print("No GPU detected.")
        print("Training will run on CPU\n")


    print("Loading YOLOv8 model...\n")

    model = YOLO("yolov8s.pt")


    print("Starting training...\n")

    model.train(

        data="datasets/object_detection/data.yaml",

        epochs=150,

        imgsz=640,

        batch=8,

        device=device,

        workers=4,   # safer for Windows

        patience=30,

        amp=True,


        # Augmentations
        mosaic=1.0,
        mixup=0.1,
        degrees=10,
        scale=0.5,
        fliplr=0.5,

        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4
    )


    print("\nTraining complete!\n")
    print("Best model saved at:")
    print("runs/detect/train/weights/best.pt\n")


if __name__ == "__main__":
    main()