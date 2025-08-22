import os
import pandas as pd
import duckdb
from datetime import datetime
from sklearn.preprocessing import StandardScaler

# ----------------------------
# 1. Paths
# ----------------------------
base_dir = r"C:\Users\cbonag\OneDrive - wilp.bits-pilani.ac.in\Sem-2\DMML\Assignment"
data_preparation_dir = os.path.join(base_dir, "Data Preparation")
today = datetime.today().strftime("%Y-%m-%d")

cleaned_file = os.path.join(data_preparation_dir, f"cleaned_telco_churn_{today}.csv")
db_file = os.path.join(base_dir, "transformed_telco.duckdb")

# ----------------------------
# 2. Load Clean Data
# ----------------------------
df = pd.read_csv(cleaned_file)
print(f"✅ Cleaned data loaded: {df.shape}")

# ----------------------------
# 3. Feature Engineering
# ----------------------------
# Total Spend
if "tenure" in df.columns and "MonthlyCharges" in df.columns:
    df["TotalSpend"] = df["tenure"] * df["MonthlyCharges"]

# Tenure Group
if "tenure" in df.columns:
    max_tenure = df["tenure"].max()
    base_bins = [0, 12, 24, 48, 60]
    bin_edges = sorted(set(base_bins + [max_tenure]))

    if len(bin_edges) < 2:
        bin_edges = [0, max_tenure]

    labels = [f"{bin_edges[i]}-{bin_edges[i+1]}m" for i in range(len(bin_edges)-1)]

    df["TenureGroup"] = pd.cut(
        df["tenure"],
        bins=bin_edges,
        labels=labels,
        include_lowest=True,
        duplicates="drop"
    )

# Avg Spend Per Month
if "TotalCharges" in df.columns and "tenure" in df.columns:
    df["AvgSpendPerMonth"] = df["TotalCharges"] / df["tenure"].replace(0, 1)

# Normalize numeric columns
num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
if 'Churn' in num_cols:
    num_cols.remove('Churn')
scaler = StandardScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])

print("✅ Feature engineering applied")

# ----------------------------
# 4. Store in DuckDB (Persistent)
# ----------------------------
con = duckdb.connect(db_file)

# Create schema if missing
con.execute("CREATE SCHEMA IF NOT EXISTS telco;")

# Drop & recreate table
con.execute("DROP TABLE IF EXISTS telco.customer_churn;")

# Persist DataFrame as DuckDB table (storage backed)
con.register("df_view", df)  # Register Pandas DataFrame as a view
con.execute("CREATE TABLE telco.customer_churn AS SELECT * FROM df_view;")
con.unregister("df_view")

con.execute("CHECKPOINT;")  # Force flush to disk

print(f"💾 Transformed data stored in {db_file} (table: telco.customer_churn)")

# ----------------------------
# 5. Sample Queries
# ----------------------------
queries = {
    "Customer Count": "SELECT COUNT(*) FROM telco.customer_churn;",
    "Churn Rate": "SELECT AVG(CAST(Churn AS DOUBLE)) AS churn_rate FROM telco.customer_churn;",
    "Avg Spend by Tenure Group": """
        SELECT TenureGroup, AVG(TotalSpend) AS avg_total_spend
        FROM telco.customer_churn
        GROUP BY TenureGroup
        ORDER BY TenureGroup;
    """
}

print("\n📌 Sample Queries:")
for name, q in queries.items():
    print(f"\n{name}:\n{q}")
