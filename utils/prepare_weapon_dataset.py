import os
import shutil
import random
from pathlib import Path

# -------------------------------------------------
# DATASET PATHS
# -------------------------------------------------

DATASET1 = r"D:\Project\weapon_dataset\weapons"
DATASET2 = r"D:\Project\weapon_dataset\weapons_cctv"

OUTPUT = r"D:\PantherAI\datasets\weapon_detection"

RAW_IMAGES = os.path.join(OUTPUT, "raw", "images")
RAW_LABELS = os.path.join(OUTPUT, "raw", "labels")

TRAIN_IMAGES = os.path.join(OUTPUT, "images", "train")
VAL_IMAGES = os.path.join(OUTPUT, "images", "val")

TRAIN_LABELS = os.path.join(OUTPUT, "labels", "train")
VAL_LABELS = os.path.join(OUTPUT, "labels", "val")

SPLIT_RATIO = 0.8

# -------------------------------------------------
# CREATE DIRECTORIES
# -------------------------------------------------

dirs = [
    RAW_IMAGES, RAW_LABELS,
    TRAIN_IMAGES, VAL_IMAGES,
    TRAIN_LABELS, VAL_LABELS
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

# -------------------------------------------------
# LABEL CONVERTER: WEAPONS DATASET
# -------------------------------------------------

def convert_weapons_dataset(label_path):

    new_lines = []

    with open(label_path) as f:
        lines = f.readlines()

    for line in lines:

        parts = line.strip().split()

        # convert class 0,1,2 → weapon (1)
        parts[0] = "1"

        new_lines.append(" ".join(parts))

    return new_lines


# -------------------------------------------------
# LABEL CONVERTER: CCTV DATASET
# -------------------------------------------------

def convert_cctv_dataset(label_path):

    # keep labels unchanged
    with open(label_path) as f:
        return [l.strip() for l in f.readlines()]


# -------------------------------------------------
# MERGE DATASET FUNCTION
# -------------------------------------------------

def merge_dataset(dataset_path, converter, prefix):

    counter = 0

    for split in ["train", "valid", "test"]:

        img_dir = os.path.join(dataset_path, split, "images")
        lbl_dir = os.path.join(dataset_path, split, "labels")

        if not os.path.exists(img_dir):
            continue

        for img in os.listdir(img_dir):

            if not img.lower().endswith((".jpg",".jpeg",".png")):
                continue

            name = Path(img).stem
            new_name = f"{prefix}_{counter}"

            src_img = os.path.join(img_dir, img)
            src_lbl = os.path.join(lbl_dir, name + ".txt")

            dst_img = os.path.join(RAW_IMAGES, new_name + ".jpg")
            dst_lbl = os.path.join(RAW_LABELS, new_name + ".txt")

            shutil.copy(src_img, dst_img)

            if os.path.exists(src_lbl):

                labels = converter(src_lbl)

                with open(dst_lbl, "w") as f:
                    f.write("\n".join(labels))

            counter += 1


# -------------------------------------------------
# MERGE BOTH DATASETS
# -------------------------------------------------

print("Merging weapons dataset...")
merge_dataset(DATASET1, convert_weapons_dataset, "w")

print("Merging CCTV dataset...")
merge_dataset(DATASET2, convert_cctv_dataset, "cctv")

print("Merge completed")


# -------------------------------------------------
# SPLIT DATASET
# -------------------------------------------------

images = os.listdir(RAW_IMAGES)

random.shuffle(images)

split_index = int(len(images) * SPLIT_RATIO)

train_files = images[:split_index]
val_files = images[split_index:]


def move_files(files, img_dst, lbl_dst):

    for img in files:

        name = Path(img).stem

        src_img = os.path.join(RAW_IMAGES, img)
        src_lbl = os.path.join(RAW_LABELS, name + ".txt")

        shutil.copy(src_img, os.path.join(img_dst, img))

        if os.path.exists(src_lbl):
            shutil.copy(src_lbl, os.path.join(lbl_dst, name + ".txt"))


move_files(train_files, TRAIN_IMAGES, TRAIN_LABELS)
move_files(val_files, VAL_IMAGES, VAL_LABELS)

print("Dataset split completed")


# -------------------------------------------------
# CREATE DATA.YAML
# -------------------------------------------------

yaml_content = """
path: datasets/weapon_detection

train: images/train
val: images/val

names:
  0: person
  1: weapon
"""

with open(os.path.join(OUTPUT, "data.yaml"), "w") as f:
    f.write(yaml_content)

print("data.yaml created")

# -------------------------------------------------
# SUMMARY
# -------------------------------------------------

print("\nPantherAI Weapon Dataset Ready")
print("Total images:", len(images))
print("Train images:", len(train_files))
print("Validation images:", len(val_files))