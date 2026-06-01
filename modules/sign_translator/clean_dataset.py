import pandas as pd

DATASET_PATH = "datasets/sign_language_landmarks/gesture_dataset.csv"

print("Loading dataset...")

df = pd.read_csv(DATASET_PATH, header=None)

print("Original samples:", len(df))

# remove duplicates
df = df.drop_duplicates()

# remove rows with too many zeros
df = df[(df.iloc[:, :-1] != 0).sum(axis=1) > 80]

print("Cleaned samples:", len(df))

df.to_csv("datasets/sign_language_landmarks/clean_dataset.csv", index=False, header=False)

print("Clean dataset saved.")