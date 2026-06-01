import json
import os
import pandas as pd

dataset = "datasets/crowd_density"

def process_split(split):

    annotation_file = os.path.join(dataset, "annotations", split, "_annotations.coco.json")

    with open(annotation_file) as f:
        data = json.load(f)

    images = {img["id"]: img["file_name"] for img in data["images"]}

    counts = {}

    for ann in data["annotations"]:
        img_id = ann["image_id"]
        counts[img_id] = counts.get(img_id, 0) + 1

    rows = []

    for img_id, filename in images.items():

        count = counts.get(img_id, 0)

        rows.append({
            "image": os.path.join(dataset, "images", split, filename),
            "count": count
        })

    return rows


train_rows = process_split("train")
val_rows = process_split("val")

df = pd.DataFrame(train_rows + val_rows)

output = os.path.join(dataset, "crowd_counts.csv")

df.to_csv(output, index=False)

print("Crowd count dataset created")
print("Total samples:", len(df))