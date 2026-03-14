from typing import List, Dict, Any
from services.db_service import get_db_connection


def get_reviews_for_summary(max_reviews: int = 100) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.id,
            r.text AS review_text,
            r.rating,
            r.created_at,
            e.sentiment,
            e.feature_area,
            e.issue_type,
            e.urgency,
            e.short_summary,
            e.cluster_id
        FROM reviews r
        JOIN enriched_reviews e
            ON r.id = e.review_row_id
        LIMIT ?
    """, (max_reviews,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]
