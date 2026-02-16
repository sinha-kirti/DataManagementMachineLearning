# 🔹 Step 3 – Data Transformation & Storage

## Objective
Apply feature transformations and persist data into an efficient storage system.

## Process
- Encode categorical variables:  
  - One-hot encoding for small categories.  
  - Label encoding for high-cardinality features.  
- Normalize/scale numeric features.  
- Store transformed data in **DuckDB** (`transformed_telco.duckdb`).  

## Implementation Highlights
- DuckDB provides SQL-like queries directly in Python.  
- Transformation pipeline is modular and version-controlled.  
- Partitioned storage for historical versions.  

## Challenges & Solutions
- **Challenge:** Pandas transformations slowed down on large datasets.  
  **Solution:** Moved transformations into **DuckDB SQL queries** for faster execution.  

- **Challenge:** Maintaining reproducibility.  
  **Solution:** Version-controlled transformation scripts and datasets.  
