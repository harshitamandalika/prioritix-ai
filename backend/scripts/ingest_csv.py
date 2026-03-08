import pandas as pd
from pathlib import Path
from backend.db import get_conn

BASE = Path(__file__).resolve().parents[2]
df = pd.read_csv(BASE / "data" / "reviews_clean.csv")

conn = get_conn()
for _, r in df.iterrows():
    conn.execute(
        "INSERT INTO reviews (text, rating, created_at) VALUES (?, ?, ?)",
        (r["text"], int(r["rating"]), r["created_at"])
    )

conn.commit()
print("Inserted:", len(df))
