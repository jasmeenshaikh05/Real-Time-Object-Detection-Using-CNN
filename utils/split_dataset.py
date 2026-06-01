import os
import random
import shutil

IMG_SRC = "datasets/object_detection/raw/images"
LBL_SRC = "datasets/object_detection/raw/labels"

IMG_TRAIN = "datasets/object_detection/images/train"
IMG_VAL = "datasets/object_detection/images/val"

LBL_TRAIN = "datasets/object_detection/labels/train"
LBL_VAL = "datasets/object_detection/labels/val"

files = [f for f in os.listdir(IMG_SRC) if f.endswith(".jpg")]

random.shuffle(files)

split = int(len(files)*0.8)

train = files[:split]
val = files[split:]

for f in train:
    shutil.copy(os.path.join(IMG_SRC,f), os.path.join(IMG_TRAIN,f))
    shutil.copy(os.path.join(LBL_SRC,f.replace(".jpg",".txt")), os.path.join(LBL_TRAIN,f.replace(".jpg",".txt")))

for f in val:
    shutil.copy(os.path.join(IMG_SRC,f), os.path.join(IMG_VAL,f))
    shutil.copy(os.path.join(LBL_SRC,f.replace(".jpg",".txt")), os.path.join(LBL_VAL,f.replace(".jpg",".txt")))

print("Dataset split complete")