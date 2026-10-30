import pandas as pd
import sqlite3
from pathlib import Path

# project root = the folder above src/
ROOT = Path(__file__).resolve().parent.parent
csv_path = ROOT / "data" / "raw" / "creditcard.csv"
db_path = ROOT / "database" / "fraud.db"

df = pd.read_csv(csv_path)
df = df.loc[:, ~df.columns.str.startswith("Unnamed")]  # drop stray index column

conn = sqlite3.connect(db_path)
df.to_sql("transactions", conn, if_exists="replace", index=False)
conn.close()

print("Rows, columns:", df.shape)
print(df["Class"].value_counts())