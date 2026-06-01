import os
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import cv2
from torch.utils.data import Dataset, DataLoader
from torchvision import models
from torch.cuda.amp import GradScaler, autocast


DATASET_CSV = "datasets/crowd_density/crowd_counts.csv"

IMG_SIZE = 192
BATCH_SIZE = 16
EPOCHS = 20


class CrowdDataset(Dataset):

    def __init__(self, df):

        self.df = df.reset_index(drop=True)

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):

        row = self.df.iloc[idx]

        img = cv2.imread(row["image"])

        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

        img = img / 255.0

        img = torch.tensor(img).permute(2,0,1).float()

        count = torch.tensor(row["count"]).float()

        return img, count


print("Loading dataset...")

df = pd.read_csv(DATASET_CSV)

train_df = df.sample(frac=0.8, random_state=42)
val_df = df.drop(train_df.index)

train_dataset = CrowdDataset(train_df)
val_dataset = CrowdDataset(val_df)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE)


print("Building model...")

model = models.resnet18(pretrained=True)

# freeze backbone
for param in model.parameters():
    param.requires_grad = False

# new regression head
model.fc = nn.Sequential(
    nn.Linear(model.fc.in_features, 128),
    nn.ReLU(),
    nn.Linear(128, 1)
)

device = "cuda" if torch.cuda.is_available() else "cpu"

model = model.to(device)


criterion = nn.MSELoss()

optimizer = optim.Adam(model.fc.parameters(), lr=0.0003)


scaler = GradScaler()


best_val_loss = float("inf")


print("Starting training...")

for epoch in range(EPOCHS):

    model.train()

    train_loss = 0

    for imgs, counts in train_loader:

        imgs = imgs.to(device)
        counts = counts.to(device)

        optimizer.zero_grad()

        with autocast():

            preds = model(imgs).squeeze()

            loss = criterion(preds, counts)

        scaler.scale(loss).backward()

        scaler.step(optimizer)

        scaler.update()

        train_loss += loss.item()


    model.eval()

    val_loss = 0

    with torch.no_grad():

        for imgs, counts in val_loader:

            imgs = imgs.to(device)
            counts = counts.to(device)

            preds = model(imgs).squeeze()

            loss = criterion(preds, counts)

            val_loss += loss.item()


    print(
        f"Epoch {epoch+1}/{EPOCHS} | "
        f"Train Loss: {train_loss:.2f} | "
        f"Val Loss: {val_loss:.2f}"
    )


    if val_loss < best_val_loss:

        best_val_loss = val_loss

        os.makedirs("models/hazard", exist_ok=True)

        torch.save(model.state_dict(), "models/hazard/crowd_model.pth")

        print("Model improved — saved.")


print("Training complete.")