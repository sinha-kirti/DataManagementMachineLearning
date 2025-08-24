import duckdb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
from datetime import datetime
import os

def train_model():
    # ----------------------------
    # 1. Paths & DB connection
    # ----------------------------
    db_file = r"/Users/kirtisinha/DataManagementMachineLearning/transformed_telco.duckdb"
    model_dir = r"/Users/kirtisinha/DataManagementMachineLearning/ModelBuilding"
    os.makedirs(model_dir, exist_ok=True)

    con = duckdb.connect(db_file)

    # ----------------------------
    # 2. Load Features from DuckDB
    # ----------------------------
    query = """
    SELECT customerID, TotalSpend, TenureGroup, AvgSpendPerMonth, Churn
    FROM telco.customer_churn
    """
    df = con.execute(query).fetchdf()
    print(f"✅ Loaded {df.shape[0]} records from feature store")

    # ----------------------------
    # 3. Handle Target Column Robustly
    # ----------------------------
    # Convert to numeric; invalid parsing becomes NaN
    df['Churn'] = pd.to_numeric(df['Churn'], errors='coerce')

    # Drop rows where target is NaN
    df = df.dropna(subset=['Churn'])

    # Convert to integer (0/1)
    df['Churn'] = df['Churn'].astype(int)

    # ----------------------------
    # 4. Handle Feature Missing Values
    # ----------------------------
    # Numeric columns
    num_cols = df.select_dtypes(include=['int64','float64']).columns.tolist()
    if 'Churn' in num_cols:
        num_cols.remove('Churn')

    df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    # Categorical columns
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    # ----------------------------
    # 5. Encode Categorical Features
    # ----------------------------
    df = pd.get_dummies(df, columns=['TenureGroup'], drop_first=True)

    # Features and target
    X = df.drop(columns=['customerID', 'Churn'])
    y = df['Churn']

    # ----------------------------
    # 6. Train-Test Split
    # ----------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # ----------------------------
    # 7. Scale Numeric Features
    # ----------------------------
    scaler = StandardScaler()
    X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
    X_test[num_cols] = scaler.transform(X_test[num_cols])

    # ----------------------------
    # 8. Train Models
    # ----------------------------
    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42)
    }

    results = []

    for name, model in models.items():
        # Train
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        
        # Metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        results.append({
            "Model": name,
            "Accuracy": acc,
            "Precision": prec,
            "Recall": rec,
            "F1_Score": f1
        })
        
        # Save model with timestamp for versioning
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_file = os.path.join(model_dir, f"{name}_{timestamp}.pkl")
        joblib.dump(model, model_file)
        print(f"✅ Saved {name} model to {model_file}")

    # ----------------------------
    # 9. Save Model Performance Report
    # ----------------------------
    results_df = pd.DataFrame(results)
    report_file = os.path.join(model_dir, f"model_performance_{datetime.now().strftime('%Y%m%d')}.csv")
    results_df.to_csv(report_file, index=False)
    print(f"✅ Model performance report saved: {report_file}")

    # ----------------------------
    # 10. Print Results
    # ----------------------------
    print("\n📌 Model Performance Summary:")
    print(results_df)
