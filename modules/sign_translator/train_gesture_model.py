import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

DATASET_PATH = "datasets/sign_language_landmarks/gesture_dataset.csv"

print("Loading dataset...")

df = pd.read_csv(DATASET_PATH, header=None)

print("Original samples:", len(df))

# --------------------------------------------------
# DATA CLEANING
# --------------------------------------------------

df = df.drop_duplicates()

df = df[(df.iloc[:, :-1] != 0).sum(axis=1) > 80]

print("Samples after cleaning:", len(df))

# --------------------------------------------------
# REMOVE CLASSES WITH VERY FEW SAMPLES
# --------------------------------------------------

label_counts = df.iloc[:, -1].value_counts()

print("\nClass distribution before filtering:")
print(label_counts)

valid_labels = label_counts[label_counts >= 20].index

df = df[df.iloc[:, -1].isin(valid_labels)]

print("\nClasses kept:")
print(valid_labels)

print("Samples after filtering:", len(df))

# --------------------------------------------------
# FEATURES / LABELS
# --------------------------------------------------

X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# normalize hand position
X = X.sub(X.mean(axis=1), axis=0)

# --------------------------------------------------
# TRAIN TEST SPLIT
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

# --------------------------------------------------
# MODEL
# --------------------------------------------------

model = Pipeline([
    ("scaler", StandardScaler()),
    ("mlp", MLPClassifier(
        hidden_layer_sizes=(256,128),
        activation="relu",
        max_iter=500,
        random_state=42
    ))
])

print("\nTraining model...")

model.fit(X_train, y_train)

# --------------------------------------------------
# EVALUATE
# --------------------------------------------------

pred = model.predict(X_test)

accuracy = accuracy_score(y_test, pred)

print("\nModel accuracy:", accuracy)

# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

joblib.dump(model, "models/gesture_classifier.pkl")

print("\nModel saved to models/gesture_classifier.pkl")