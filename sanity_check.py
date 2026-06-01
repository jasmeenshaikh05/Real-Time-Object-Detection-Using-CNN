import os
import shutil
import random
import hashlib
from collections import Counter, defaultdict

dataset_root = "D:/PantherAI/datasets/object_detection"

raw_images = os.path.join(dataset_root,"raw/images")
raw_labels = os.path.join(dataset_root,"raw/labels")

train_images = os.path.join(dataset_root,"images/train")
val_images = os.path.join(dataset_root,"images/val")

train_labels = os.path.join(dataset_root,"labels/train")
val_labels = os.path.join(dataset_root,"labels/val")

TARGET = 6000
split_ratio = 0.8

os.makedirs(train_images,exist_ok=True)
os.makedirs(val_images,exist_ok=True)
os.makedirs(train_labels,exist_ok=True)
os.makedirs(val_labels,exist_ok=True)

print("\nSTEP 1 — Cleaning dataset")

image_files = {os.path.splitext(f)[0] for f in os.listdir(raw_images)}
label_files = {os.path.splitext(f)[0] for f in os.listdir(raw_labels)}

missing_labels = image_files - label_files
missing_images = label_files - image_files

for name in missing_labels:
    img = os.path.join(raw_images,name+".jpg")
    if os.path.exists(img):
        os.remove(img)

for name in missing_images:
    lbl = os.path.join(raw_labels,name+".txt")
    if os.path.exists(lbl):
        os.remove(lbl)

print("Removed images without labels:",len(missing_labels))
print("Removed labels without images:",len(missing_images))


print("\nSTEP 2 — Removing duplicate images")

hashes={}
duplicates=0

for file in os.listdir(raw_images):

    path=os.path.join(raw_images,file)

    with open(path,"rb") as f:
        filehash=hashlib.md5(f.read()).hexdigest()

    if filehash in hashes:

        duplicates+=1

        os.remove(path)

        lbl=os.path.join(raw_labels,os.path.splitext(file)[0]+".txt")
        if os.path.exists(lbl):
            os.remove(lbl)

    else:
        hashes[filehash]=file

print("Duplicates removed:",duplicates)


print("\nSTEP 3 — Checking class distribution")

counter=Counter()

for file in os.listdir(raw_labels):

    with open(os.path.join(raw_labels,file)) as f:

        for line in f:

            cls=int(line.split()[0])
            counter[cls]+=1

print(counter)


print("\nSTEP 4 — Balancing dataset")

class_files=defaultdict(list)

for file in os.listdir(raw_labels):

    path=os.path.join(raw_labels,file)

    with open(path) as f:
        line=f.readline()

        if not line:
            continue

        cls=int(line.split()[0])

    img=os.path.splitext(file)[0]+".jpg"

    if os.path.exists(os.path.join(raw_images,img)):
        class_files[cls].append((img,file))


counter_id=0

for cls,files in class_files.items():

    if len(files)>=TARGET:
        continue

    needed=TARGET-len(files)

    for i in range(needed):

        img,label=random.choice(files)

        src_img=os.path.join(raw_images,img)
        src_lbl=os.path.join(raw_labels,label)

        new_img=f"aug_{cls}_{counter_id}.jpg"
        new_lbl=f"aug_{cls}_{counter_id}.txt"

        shutil.copy(src_img,os.path.join(raw_images,new_img))
        shutil.copy(src_lbl,os.path.join(raw_labels,new_lbl))

        counter_id+=1


print("Balancing complete")


print("\nSTEP 5 — Creating train/val split")

images=[f for f in os.listdir(raw_images) if f.lower().endswith((".jpg",".jpeg",".png"))]

random.shuffle(images)

split_index=int(len(images)*split_ratio)

train_set=images[:split_index]
val_set=images[split_index:]


for img in train_set:

    img_src=os.path.join(raw_images,img)
    lbl_src=os.path.join(raw_labels,os.path.splitext(img)[0]+".txt")

    shutil.copy(img_src,os.path.join(train_images,img))

    if os.path.exists(lbl_src):
        shutil.copy(lbl_src,os.path.join(train_labels,os.path.basename(lbl_src)))


for img in val_set:

    img_src=os.path.join(raw_images,img)
    lbl_src=os.path.join(raw_labels,os.path.splitext(img)[0]+".txt")

    shutil.copy(img_src,os.path.join(val_images,img))

    if os.path.exists(lbl_src):
        shutil.copy(lbl_src,os.path.join(val_labels,os.path.basename(lbl_src)))


print("\nDataset ready for training")

print("Train images:",len(train_set))
print("Validation images:",len(val_set))