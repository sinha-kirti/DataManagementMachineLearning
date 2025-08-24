# 🔹 Step 6 – Model Building

## Objective
Train and evaluate machine learning models using curated feature sets.

## Process
- Train baseline models: Logistic Regression, Decision Tree, Random Forest.  
- Evaluate using: Accuracy, Precision, Recall, F1-score.  
- Store trained models and metrics.  

## Implementation Highlights
- Retraining scheduled via Airflow DAG.  
- Metrics logged for comparison.  
- Supports extension to CI/CD pipelines with MLflow.  

## Challenges & Solutions
- **Challenge:** Imbalanced churn dataset (majority non-churn).  
  **Solution:** Applied SMOTE to balance classes.  

- **Challenge:** Feature drift reducing accuracy.  
  **Solution:** Added monitoring scripts to check feature distributions.  
