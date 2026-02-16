import duckdb

con = duckdb.connect("C:/Users/cbonag/OneDrive - wilp.bits-pilani.ac.in/Sem-2/DMML/Assignment/transformed_telco.duckdb")

# List all tables
print(con.execute("SHOW TABLES").fetchdf())

# Preview transformed data
df = con.execute("SELECT * FROM telco.customer_churn  LIMIT 10").fetchdf()
print(df['Churn'].unique())
print(df['Churn'].unique())        # Should show only 0 and 1
print(df['Churn'].isna().sum())    # Should be 0
print(df['Churn'].dtype)  
print(df)