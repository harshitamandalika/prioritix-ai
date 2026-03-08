from backend.db import get_conn

SQL = """
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    rating INTEGER,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS enriched_reviews (
    review_id INTEGER,
    sentiment TEXT,
    feature_area TEXT,
    issue_type TEXT,
    urgency INTEGER,
    short_summary TEXT
);
"""

if __name__ == "__main__":
    conn = get_conn()
    conn.executescript(SQL)
    conn.commit()
    print("DB initialized")
