import os
import shutil

# Source dataset
dataset = "D:/Project/backpack_1"

# dataset splits
subsets = ["train", "valid", "test"]

# destination master dataset
dest_images = "D:/PantherAI/datasets/object_detection/raw/images"
dest_labels = "D:/PantherAI/datasets/object_detection/raw/labels"

os.makedirs(dest_images, exist_ok=True)
os.makedirs(dest_labels, exist_ok=True)

counter = 0

for subset in subsets:

    img_folder = os.path.join(dataset, subset, "images")
    lbl_folder = os.path.join(dataset, subset, "labels")

    if not os.path.exists(img_folder):
        continue

    for img_file in os.listdir(img_folder):

        if not img_file.lower().endswith((".jpg",".jpeg",".png")):
            continue

        img_path = os.path.join(img_folder, img_file)
        label_name = os.path.splitext(img_file)[0] + ".txt"
        label_path = os.path.join(lbl_folder, label_name)

        new_name = f"backpack_new{counter}.jpg"

        shutil.copy(img_path, os.path.join(dest_images, new_name))

        if os.path.exists(label_path):

            with open(label_path, "r") as f:
                lines = f.readlines()

            new_lines = []

            for line in lines:
                parts = line.strip().split()

                if len(parts) > 0:
                    parts[0] = "8"   # convert class id to cat

                new_lines.append(" ".join(parts) + "\n")

            new_label = os.path.splitext(new_name)[0] + ".txt"

            with open(os.path.join(dest_labels,new_label),"w") as f:
                f.writelines(new_lines)

        counter += 1

print("Backpack dataset merged successfully.")