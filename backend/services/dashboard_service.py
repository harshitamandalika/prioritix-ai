from collections import defaultdict, Counter
from services.db_service import get_db_connection


def get_all_reviews():
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
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_feature_table_data():
    reviews = get_all_reviews()

    feature_map = defaultdict(lambda: {
        "feature_area": "",
        "total_reviews": 0,
        "positive": 0,
        "neutral": 0,
        "negative": 0,
        "high_urgency": 0,
    })

    for review in reviews:
        feature = review.get("feature_area") or "unknown"
        sentiment = (review.get("sentiment") or "").lower()
        urgency = review.get("urgency") or 0

        row = feature_map[feature]
        row["feature_area"] = feature
        row["total_reviews"] += 1

        if sentiment in ("positive", "neutral", "negative"):
            row[sentiment] += 1

        if urgency >= 4:
            row["high_urgency"] += 1

    return list(feature_map.values())


def get_clusters_data():
    reviews = get_all_reviews()

    cluster_map = defaultdict(lambda: {
        "cluster_id": None,
        "cluster_name": "",
        "review_count": 0,
        "feature_area": "",
        "top_features": [],
    })

    cluster_feature_counts = defaultdict(Counter)

    for review in reviews:
        cid = review.get("cluster_id")
        if cid is None:
            continue

        feature = review.get("feature_area") or "unknown"

        row = cluster_map[cid]
        row["cluster_id"] = cid
        row["review_count"] += 1

        cluster_feature_counts[cid][feature] += 1

    for cid, row in cluster_map.items():
        top_features = cluster_feature_counts[cid].most_common(3)
        top_feature_names = [feature for feature, _ in top_features]

        row["top_features"] = top_feature_names
        row["feature_area"] = top_feature_names[0] if top_feature_names else "unknown"
        row["cluster_name"] = " / ".join(top_feature_names) if top_feature_names else f"Cluster {cid}"

    return sorted(cluster_map.values(), key=lambda x: x["review_count"], reverse=True)


def get_cluster_samples_data(cluster_id: int, limit: int = 15):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.text AS review_text,
            e.sentiment,
            e.urgency,
            e.feature_area,
            e.short_summary,
            e.issue_type
        FROM reviews r
        JOIN enriched_reviews e
            ON r.id = e.review_row_id
        WHERE e.cluster_id = ?
        LIMIT ?
    """, (cluster_id, limit))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]
