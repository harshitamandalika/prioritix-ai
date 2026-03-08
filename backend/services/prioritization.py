from backend.db import get_conn

def compute():
    conn = get_conn()
    rows = conn.execute("""
        SELECT feature_area,
               COUNT(*) as freq,
               AVG(urgency) as urg,
               AVG(sentiment='negative') as neg
        FROM enriched_reviews
        GROUP BY feature_area
    """).fetchall()

    scores = []
    for r in rows:
        score = r["freq"] * r["urg"] * r["neg"]
        scores.append((r["feature_area"], score))
    return sorted(scores, key=lambda x: x[1], reverse=True)
