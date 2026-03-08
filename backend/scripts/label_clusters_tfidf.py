from backend.db import get_conn
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
BLOCK = {
    "app","use","using","like","just","time","really","dont","don","does","work","phone",
    "great","good","best","love","nice","version", "pay", "paid", "payment", "money"

}

TOP_N = 12

if __name__ == "__main__":
    conn = get_conn()

    rows = conn.execute("""
        SELECT e.cluster_id, r.text
        FROM enriched_reviews e
        JOIN reviews r ON r.id = e.review_row_id
        WHERE e.cluster_id IS NOT NULL AND r.text IS NOT NULL
    """).fetchall()

    if not rows:
        print("No clustered rows found. Run cluster_store first.")
        exit()

    cluster_ids = [r["cluster_id"] for r in rows]
    texts = [r["text"] for r in rows]

    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=3, max_features=20000)
    X = vec.fit_transform(texts)
    terms = np.array(vec.get_feature_names_out())

    # Average TF-IDF vector per cluster -> top terms
    unique_clusters = sorted(set(cluster_ids))
    for cid in unique_clusters:
        idx = [i for i, c in enumerate(cluster_ids) if c == cid]
        if not idx:
            continue
        Xc = X[idx].mean(axis=0)
        Xc = np.asarray(Xc).ravel()
        top_idx = np.argsort(-Xc)[:TOP_N]
        cand = [t for t in terms[top_idx] if t not in BLOCK]

        # ensure label has at least 3 terms
        if len(cand) < 3:
            # add some unblocked terms from a larger pool
            top_idx2 = np.argsort(-Xc)[:30]
            more = [t for t in terms[top_idx2] if t not in BLOCK and t not in cand]
            cand.extend(more)

        label = ", ".join(cand[:6]) if cand else ", ".join(terms[top_idx][:6])


        size = conn.execute(
            "SELECT COUNT(*) FROM enriched_reviews WHERE cluster_id=?",
            (cid,)
        ).fetchone()[0]

        conn.execute(
            "UPDATE clusters SET label=?, size=? WHERE cluster_id=?",
            (label, int(size), int(cid))
        )

    conn.commit()
    print("Cluster labels updated.")
