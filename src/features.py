import pandas as pd
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
db_path = ROOT / "database" / "fraud.db"
sql_path = ROOT / "sql" / "queries.sql"
out_path = ROOT / "data" / "processed" / "features.csv"
out_path.parent.mkdir(parents=True, exist_ok=True)

# split the .sql file into separate queries
queries = [q.strip() for q in sql_path.read_text().split(";") if q.strip()]

conn = sqlite3.connect(db_path)

# show the two analysis queries
print("=== Fraud vs normal ===")
print(pd.read_sql_query(queries[0], conn))
print("\n=== Fraud rate by hour ===")
print(pd.read_sql_query(queries[1], conn))

# run the feature query and join the V1..V28 columns back in
feat = pd.read_sql_query(queries[2], conn)
v_cols = ", ".join([f"V{i}" for i in range(1, 29)])
v = pd.read_sql_query(f"SELECT rowid AS txn_id, {v_cols} FROM transactions", conn)
conn.close()

df = feat.merge(v, on="txn_id")

# first rows have no history, so fill the gaps
df["avg_amount_last_100"] = df["avg_amount_last_100"].fillna(df["Amount"])
df["txns_last_60s"] = df["txns_last_60s"].fillna(0)

# a readable feature: how big is this amount compared to recent average?
df["amount_ratio"] = df["Amount"] / (df["avg_amount_last_100"] + 1e-6)

df.to_csv(out_path, index=False)
print("\nSaved:", out_path, df.shape)