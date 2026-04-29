import pandas as pd
import sqlite3
import glob

# Step 1: read all CSVs and combine
files = glob.glob("data/raw/*.csv")
df = pd.concat([pd.read_csv(f) for f in files])
print(f"Total rows loaded: {len(df)}")

# Step 2: connect to SQLite
conn = sqlite3.connect("jobs.db")

# Step 3: load into table called "jobs"
df.to_sql("jobs", conn, if_exists="replace", index=False)
print("Data loaded into jobs.db!")

# Step 4: verify
result = pd.read_sql("SELECT COUNT(*) FROM jobs", conn)
print(result)

conn.close()