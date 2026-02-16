# 🔹 Step 5 – Feature Store

## Objective
Provide centralized, reusable features for ML models.

## Process
- Engineer derived features such as:  
  - Customer tenure groupings.  
  - Average monthly spend.  
  - Binary contract indicators.  
- Store final feature set in DuckDB and parquet format.  
- Maintain versioning for reproducibility.  

## Implementation Highlights
- Metadata tracked: feature name, description, creation date.  
- Supports **feature views** (subsets for specific models).  
- Enables consistency across experiments.  

## Challenges & Solutions
- **Challenge:** Different models required different features.  
  **Solution:** Created multiple feature views from the same store.  

- **Challenge:** Keeping features updated with new data.  
  **Solution:** Airflow DAG refreshes features incrementally.  
