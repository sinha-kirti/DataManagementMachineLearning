# Data Preparation & EDA for Telco Customer Churn (Kaggle + GitHub)

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from sklearn.preprocessing import LabelEncoder, StandardScaler

# -------------------------------
# 1. Paths & Sources
# -------------------------------
base_dir = r"/Users/kirtisinha/DataManagementMachineLearning"
data_raw_dir = os.path.join(base_dir, "DataIngestion", "data_raw")
data_preparation_dir = os.path.join(base_dir, "DataPreparation")

today = datetime.today().strftime("%Y-%m-%d")

sources = {
    "github": os.path.join(data_raw_dir, "github", today, "IBM_Telco-Customer-Churn.csv"),
    "kaggle": os.path.join(data_raw_dir, "kaggle", today, "WA_Fn-UseC_-Telco-Customer-Churn.csv")
}

# -------------------------------
# 2. Load Data
# -------------------------------
dfs = []
for name, path in sources.items():
    if os.path.exists(path):
        df = pd.read_csv(path)
        df["source"] = name   # track origin
        dfs.append(df)
        print(f"{name} dataset loaded: {df.shape}")
    else:
        print(f"⚠️ {name} dataset not found at {path}")

if not dfs:
    raise FileNotFoundError("No datasets found in sources.")

# Merge datasets
df = pd.concat(dfs, ignore_index=True)
print(f"\n✅ Combined dataset shape: {df.shape}")

# -------------------------------
# 3. Basic EDA + Save Visualizations
# -------------------------------
os.makedirs(data_preparation_dir, exist_ok=True)

# Churn distribution
plt.figure(figsize=(5,4))
sns.countplot(x="Churn", data=df)
plt.title("Churn Distribution")
plt.savefig(os.path.join(data_preparation_dir, f"churn_distribution_{today}.png"))
plt.close()

# Numeric histograms
num_cols = df.select_dtypes(include=[np.number]).columns
df[num_cols].hist(figsize=(12,10), bins=20)
plt.suptitle("Numeric Feature Distributions")
plt.savefig(os.path.join(data_preparation_dir, f"numeric_distributions_{today}.png"))
plt.close()

# Correlation Heatmap
plt.figure(figsize=(12,8))
sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.savefig(os.path.join(data_preparation_dir, f"correlation_heatmap_{today}.png"))
plt.close()

print(f"📊 Visualizations saved to {data_preparation_dir}")

# -------------------------------
# 4. Data Cleaning
# -------------------------------
df.replace(" ", np.nan, inplace=True)

# Handle TotalCharges conversion
if "TotalCharges" in df.columns:
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"].fillna(df["TotalCharges"].median(), inplace=True)

# Drop missing rows (basic strategy)
df = df.dropna()

# Encode categorical variables
exclude_cols = ["customerID", "Churn", "source"]
cat_cols = df.select_dtypes(include=["object"]).drop(columns=[c for c in exclude_cols if c in df.columns]).columns

le = LabelEncoder()
for col in cat_cols:
    df[col] = le.fit_transform(df[col])

# Encode target (Churn Yes/No → 1/0)
if "Churn" in df.columns:
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

# Normalize numeric columns
if 'Churn' in num_cols:
    num_cols.remove('Churn')
scaler = StandardScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])

print("\n✅ Data cleaned and preprocessed")

# -------------------------------
# 5. Save Clean Data
# -------------------------------
clean_data_path = os.path.join(data_preparation_dir, f"cleaned_telco_churn_{today}.csv")
df.to_csv(clean_data_path, index=False)
print(f"✅ Clean dataset saved to {clean_data_path}")
