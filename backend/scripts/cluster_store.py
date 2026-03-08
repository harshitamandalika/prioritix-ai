from backend.db import get_conn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

K = 10  # number of clusters

if __name__ == "__main__":
    conn = get_conn()

    rows = conn.execute("""
        SELECT e.review_row_id, r.text
        FROM enriched_reviews e
        JOIN reviews r ON r.id = e.review_row_id
        WHERE r.text IS NOT NULL
        AND e.sentiment = 'negative'
        AND e.urgency >= 4
        AND e.feature_area != 'Generic Issue'


    """).fetchall()

    if not rows:
        print("No enriched reviews found")
        exit()

    review_ids = [r["review_row_id"] for r in rows]
    texts = [r["text"] for r in rows]

    vectorizer = TfidfVectorizer(stop_words="english", 
                ngram_range=(1,2), max_features=15000, min_df=3)

    X = vectorizer.fit_transform(texts)

    kmeans = KMeans(
        n_clusters=K,
        random_state=42,
        n_init=10
    )
    cluster_ids = kmeans.fit_predict(X)

    # Save cluster_id per review
    conn.executemany(
        "UPDATE enriched_reviews SET cluster_id=? WHERE review_row_id=?",
        [(int(cid), int(rid)) for rid, cid in zip(review_ids, cluster_ids)]
    )

    # Create / refresh clusters table
    conn.execute("DELETE FROM clusters")
    for cid in range(K):
        size = conn.execute(
            "SELECT COUNT(*) FROM enriched_reviews WHERE cluster_id=? AND cluster_id IS NOT NULL",
            (cid,)
        ).fetchone()[0]

        conn.execute(
            "INSERT INTO clusters (cluster_id, label, size) VALUES (?, ?, ?)",
            (cid, f"Cluster {cid}", int(size))
        )

    conn.commit()
    print(f"Clusters created and stored: {K}")
