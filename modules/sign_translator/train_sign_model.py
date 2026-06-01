from ultralytics import YOLO

def train():

    model = YOLO("yolov8s.pt")

    model.train(

        data="datasets/sign_language/data.yaml",

        # training length
        epochs=80,

        # image resolution
        imgsz=640,

        # batch size for RTX 3050
        batch=8,

        # GPU
        device=0,

        # workers for dataloader
        workers=4,

        # save directory
        project="runs/detect",
        name="sign_language_model",

        # augmentations (important for gestures)
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,

        degrees=10,
        translate=0.1,
        scale=0.5,
        shear=2,

        flipud=0.0,
        fliplr=0.5,

        mosaic=1.0,
        mixup=0.2,

        # optimizer improvements
        optimizer="AdamW",

        # early stopping
        patience=20,

        # cache dataset in RAM
        cache=True
    )


if __name__ == "__main__":
    train()