import pandas as pd
import sqlite3

conn = sqlite3.connect("jobs.db")

# --- INSIGHT 1: Top skills ---
df = pd.read_sql("SELECT skills FROM jobs", conn)
all_skills = []
for skills_str in df['skills']:
    if pd.notna(skills_str):
        skills_list = [s.strip() for s in skills_str.split(",")]
        all_skills.extend(skills_list)
skills_df = pd.Series(all_skills).value_counts().reset_index()
skills_df.columns = ['skill', 'count']
print("TOP 20 MOST DEMANDED SKILLS:")
print(skills_df.head(20))

# --- INSIGHT 2: Top cities ---
q2 = pd.read_sql("""
    SELECT location, COUNT(*) as job_count
    FROM jobs
    GROUP BY location
    ORDER BY job_count DESC
    LIMIT 10
""", conn)
print("\nTOP CITIES:")
print(q2)

# --- INSIGHT 3: Experience distribution ---
q3 = pd.read_sql("""
    SELECT experience, COUNT(*) as count
    FROM jobs
    GROUP BY experience
    ORDER BY count DESC
""", conn)
print("\nEXPERIENCE DISTRIBUTION:")
print(q3)

conn.close()