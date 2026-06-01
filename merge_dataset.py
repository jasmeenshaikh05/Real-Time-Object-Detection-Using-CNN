import os
import shutil

# ----------------------------
# Source datasets
# ----------------------------

dataset1 = r"D:\Project\sign_lang\sign_1"
dataset2 = r"D:\Project\sign_lang\sign_2"

# ----------------------------
# Destination dataset
# ----------------------------

dest = r"datasets\sign_language"

train_img = os.path.join(dest, "images", "train")
val_img = os.path.join(dest, "images", "val")

train_lbl = os.path.join(dest, "labels", "train")
val_lbl = os.path.join(dest, "labels", "val")

for p in [train_img, val_img, train_lbl, val_lbl]:
    os.makedirs(p, exist_ok=True)

# ----------------------------
# Class mappings
# ----------------------------

new_classes = {
    "hello":0,
    "i love you":1,
    "no":2,
    "please":3,
    "thank you":4,
    "yes":5
}

# dataset1 mapping
map1 = {
    0:0,  # hello
    1:1,  # i love you
    2:2,  # no
    3:3,  # please
    4:4,  # thank you
    5:5   # yes
}

# dataset2 mapping
map2 = {
    0:0,  # Hello
    1:1,  # I love you
    2:2,  # No
    3:4,  # Thank you
    4:5   # yes
}

# ----------------------------
# Function to copy + relabel
# ----------------------------

def process_dataset(src, mapping):

    splits = {
        "train": ("images/train","labels/train"),
        "valid": ("images/val","labels/val"),
        "test": ("images/val","labels/val")
    }

    for split in splits:

        img_src = os.path.join(src, split, "images")
        lbl_src = os.path.join(src, split, "labels")

        img_dst, lbl_dst = splits[split]

        img_dst = os.path.join(dest, img_dst)
        lbl_dst = os.path.join(dest, lbl_dst)

        if not os.path.exists(img_src):
            continue

        for img in os.listdir(img_src):

            name = os.path.splitext(img)[0]

            src_img = os.path.join(img_src, img)
            src_lbl = os.path.join(lbl_src, name + ".txt")

            dst_img = os.path.join(img_dst, img)
            dst_lbl = os.path.join(lbl_dst, name + ".txt")

            shutil.copy(src_img, dst_img)

            if os.path.exists(src_lbl):

                with open(src_lbl) as f:
                    lines = f.readlines()

                new_lines = []

                for line in lines:

                    parts = line.split()
                    cls = int(parts[0])

                    if cls not in mapping:
                        continue

                    parts[0] = str(mapping[cls])

                    new_lines.append(" ".join(parts))

                with open(dst_lbl, "w") as f:
                    f.write("\n".join(new_lines))

# ----------------------------
# Run merging
# ----------------------------

process_dataset(dataset1, map1)
process_dataset(dataset2, map2)

print("Datasets merged successfully.")