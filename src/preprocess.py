import pandas as pd

# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_excel("dataset/career_dataset_large.xlsx")

print("Original dataset shape:", df.shape)


# ==========================================
# 2. REMOVE DUPLICATES
# ==========================================

df = df.drop_duplicates()

print("After removing duplicates:", df.shape)


# ==========================================
# 3. HANDLE MISSING CERTIFICATIONS
# ==========================================

df["Certifications"] = df["Certifications"].fillna("None")


# ==========================================
# 4. CLEAN TEXT COLUMNS
# ==========================================

text_columns = [
    "Education Level",
    "Specialization",
    "Skills",
    "Certifications",
    "Recommended Career"
]

for column in text_columns:
    df[column] = df[column].astype(str).str.strip()


# ==========================================
# 5. CHECK DATA
# ==========================================

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nDataset shape after cleaning:")
print(df.shape)


# ==========================================
# 6. SHOW CAREER DISTRIBUTION
# ==========================================

print("\nCareer Distribution:")
print(df["Recommended Career"].value_counts())


# ==========================================
# 7. SAVE CLEAN DATASET
# ==========================================

df.to_csv("dataset/cleaned_career_dataset.csv", index=False)

print("\nCleaned dataset saved successfully!")