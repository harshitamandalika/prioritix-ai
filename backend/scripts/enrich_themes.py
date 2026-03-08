from backend.db import get_conn
from backend.services.offline_extraction import extract_offline

def sentiment(r):
    if r >= 4: return "positive"
    if r == 3: return "neutral"
    return "negative"

conn = get_conn()
rows = conn.execute("SELECT id, text, rating FROM reviews").fetchall()

for r in rows:
    out = extract_offline(r["text"], r["rating"])
    conn.execute(
    """INSERT OR REPLACE INTO enriched_reviews
    (review_row_id, sentiment, feature_area, issue_type, urgency, short_summary)
    VALUES (?, ?, ?, ?, ?, ?)""",
    (
        r["id"],
        sentiment(r["rating"]),
        out["feature_area"],
        out["issue_type"],
        out["urgency"],
        out["short_summary"],
    ),
)


conn.commit()
print("Enriched:", len(rows))
