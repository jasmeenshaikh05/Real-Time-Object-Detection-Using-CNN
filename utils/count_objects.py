import os
from collections import Counter

label_dir = "datasets/object_detection/raw/labels"

counter = Counter()

for file in os.listdir(label_dir):

    with open(os.path.join(label_dir,file)) as f:
        for line in f:
            cls = int(line.split()[0])
            counter[cls] += 1

print("Class Distribution:\n")

classes = {
0:"person",
1:"pen",
2:"pencil",
3:"water_bottle",
4:"thumbs_up",
5:"cat",
6:"lion",
7:"tiger",
8:"backpack",
9:"bowl"
}

for k,v in counter.items():
    print(classes[k],":",v)