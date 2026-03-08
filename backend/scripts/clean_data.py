import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

df = pd.read_csv(BASE / "data" / "reviews_raw.csv")

df = df.rename(columns={
    "content": "text",
    "score": "rating",
    "at": "created_at"
})

df = df[["text", "rating", "created_at"]]
df = df.dropna(subset=["text"])
df = df[df["text"].str.len() > 20]

df.to_csv(BASE / "data" / "reviews_clean.csv", index=False)
print("Cleaned:", len(df))
