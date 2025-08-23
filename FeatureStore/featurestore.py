import os
import duckdb
import pandas as pd
from datetime import datetime

# ----------------------------
# 1. Connect to DuckDB
# ----------------------------
db_file = r"/Users/kirtisinha/DataManagementMachineLearning/transformed_telco.duckdb"
con = duckdb.connect(db_file)

# ----------------------------
# 2. Feature Metadata Table
# ----------------------------
con.execute("""
CREATE TABLE IF NOT EXISTS feature_metadata (
    feature_name TEXT,
    description TEXT,
    source_column TEXT,
    version INTEGER,
    created_at TIMESTAMP
);
""")

# Insert metadata (example)
metadata = [
    ("TotalSpend", "Total spend by customer", "tenure * MonthlyCharges", 1, datetime.now()),
    ("TenureGroup", "Customer tenure grouped in months", "tenure", 1, datetime.now()),
    ("AvgSpendPerMonth", "Average monthly spend", "TotalCharges / tenure", 1, datetime.now())
]

con.executemany("INSERT INTO feature_metadata VALUES (?, ?, ?, ?, ?)", metadata)

# ----------------------------
# 3. Feature Store Table
# ----------------------------
con.execute("DROP TABLE IF EXISTS feature_store_customer;")
con.execute("""
CREATE TABLE feature_store_customer AS
SELECT customerID, TotalSpend, TenureGroup, AvgSpendPerMonth
FROM telco.customer_churn;
""")

print("✅ Feature store table created")

# ----------------------------
# 4. Automated Retrieval Function
# ----------------------------
def get_features(feature_list, filters=None):
    """
    Retrieve selected features from the feature store
    """
    feature_str = ", ".join(["customerID"] + feature_list)
    query = f"SELECT {feature_str} FROM feature_store_customer"
    if filters:
        query += f" WHERE {filters}"
    return con.execute(query).fetchdf()

# ----------------------------
# 5. Example Usage
# ----------------------------
print("\n📌 Available Metadata:")
print(con.execute("SELECT * FROM feature_metadata;").fetchdf())

print("\n📌 Sample Feature Retrieval:")
df_features = get_features(["TotalSpend", "TenureGroup"], filters="TotalSpend > 0")
print(df_features.head())
