import pandas as pd
import os
import joblib
import scipy.sparse as sp

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# ==========================================
# 1. LOAD CLEANED DATASET
# ==========================================

dataset_path = "dataset/cleaned_career_dataset.csv"

df = pd.read_csv(dataset_path)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# ==========================================
# 2. REMOVE DUPLICATES
# ==========================================

df = df.drop_duplicates().reset_index(drop=True)

print("After removing duplicates:", df.shape)


# ==========================================
# 3. HANDLE MISSING VALUES
# ==========================================

text_columns = [
    "Education Level",
    "Specialization",
    "Skills",
    "Certifications"
]

for column in text_columns:
    df[column] = df[column].fillna("None").astype(str)


# ==========================================
# 4. CLEAN TEXT
# ==========================================

for column in text_columns:
    df[column] = df[column].str.strip()


# ==========================================
# 5. HANDLE CGPA / PERCENTAGE
# ==========================================

df["CGPA/Percentage"] = pd.to_numeric(
    df["CGPA/Percentage"],
    errors="coerce"
)

# Replace missing CGPA values with median
df["CGPA/Percentage"] = df["CGPA/Percentage"].fillna(
    df["CGPA/Percentage"].median()
)


# ==========================================
# 6. HANDLE TARGET COLUMN
# ==========================================

df["Recommended Career"] = (
    df["Recommended Career"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)

# Remove rows where career is unknown
df = df[df["Recommended Career"] != "Unknown"]


# ==========================================
# 7. CREATE PROFILE TEXT
# ==========================================

df["Profile_Text"] = (
    df["Education Level"] + " " +
    df["Specialization"] + " " +
    df["Skills"] + " " +
    df["Certifications"]
)

# Make sure there are absolutely no NaN values
df["Profile_Text"] = (
    df["Profile_Text"]
    .fillna("")
    .astype(str)
)


# ==========================================
# 8. CHECK DATA
# ==========================================

print("\nMissing values:")
print(df[
    [
        "Education Level",
        "Specialization",
        "Skills",
        "Certifications",
        "CGPA/Percentage",
        "Recommended Career",
        "Profile_Text"
    ]
].isnull().sum())


# ==========================================
# 9. DISPLAY CAREER DISTRIBUTION
# ==========================================

print("\nCareer Distribution:")
print(df["Recommended Career"].value_counts())


# ==========================================
# 10. TF-IDF TEXT VECTORIZATION
# ==========================================

print("\nCreating TF-IDF features...")

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    max_features=3000
)

X_text = vectorizer.fit_transform(
    df["Profile_Text"]
)

print("TF-IDF features created:", X_text.shape)


# ==========================================
# 11. ADD CGPA TO FEATURES
# ==========================================

cgpa_values = df[
    ["CGPA/Percentage"]
].values

X = sp.hstack(
    [
        X_text,
        cgpa_values
    ]
)

print("Final feature matrix:", X.shape)


# ==========================================
# 12. TARGET VARIABLE
# ==========================================

y = df["Recommended Career"]


# ==========================================
# 13. TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])


# ==========================================
# 14. CREATE RANDOM FOREST MODEL
# ==========================================

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)


# ==========================================
# 15. TRAIN MODEL
# ==========================================

print("\n======================================")
print("TRAINING RANDOM FOREST MODEL")
print("======================================")

model.fit(
    X_train,
    y_train
)

print("Training completed successfully!")


# ==========================================
# 16. MAKE PREDICTIONS
# ==========================================

print("\nMaking predictions...")

y_pred = model.predict(X_test)


# ==========================================
# 17. CALCULATE ACCURACY
# ==========================================

accuracy = accuracy_score(
    y_test,
    y_pred
)


# ==========================================
# 18. DISPLAY MODEL PERFORMANCE
# ==========================================

print("\n======================================")
print("MODEL PERFORMANCE")
print("======================================")

print(
    "Accuracy:",
    round(accuracy * 100, 2),
    "%"
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# ==========================================
# 19. CREATE MODELS FOLDER
# ==========================================

os.makedirs(
    "models",
    exist_ok=True
)


# ==========================================
# 20. SAVE RANDOM FOREST MODEL
# ==========================================

model_path = "models/career_model.pkl"

joblib.dump(
    model,
    model_path
)


# ==========================================
# 21. SAVE TF-IDF VECTORIZER
# ==========================================

vectorizer_path = "models/tfidf_vectorizer.pkl"

joblib.dump(
    vectorizer,
    vectorizer_path
)


# ==========================================
# 22. SAVE FEATURE INFORMATION
# ==========================================

feature_info = {
    "cgpa_column": "CGPA/Percentage",
    "text_columns": text_columns,
    "target_column": "Recommended Career"
}

joblib.dump(
    feature_info,
    "models/feature_info.pkl"
)


# ==========================================
# 23. FINAL MESSAGE
# ==========================================

print("\n======================================")
print("MODEL SAVED SUCCESSFULLY")
print("======================================")

print("\nSaved files:")

print("1. models/career_model.pkl")
print("2. models/tfidf_vectorizer.pkl")
print("3. models/feature_info.pkl")

print("\nRoadmapX AI model training completed! 🚀")