from backend.db import get_conn
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

MIN_TRAIN_PER_CLASS = 80     # ignore tiny classes
CONF_THRESHOLD = 0.25        # increase if you want higher precision
MAX_FEATURES = 20000

def fetch_data(conn):
    # Join to get full text; this helps a lot vs short_summary
    labeled = conn.execute("""
        SELECT r.text, e.feature_area
        FROM enriched_reviews e
        JOIN reviews r ON r.id = e.review_row_id
        WHERE e.feature_area IS NOT NULL AND e.feature_area != 'Other'
    """).fetchall()

    other = conn.execute("""
        SELECT e.review_row_id, r.text
        FROM enriched_reviews e
        JOIN reviews r ON r.id = e.review_row_id
        WHERE e.feature_area = 'Generic Issue'
    """).fetchall()

    return labeled, other

if __name__ == "__main__":
    conn = get_conn()
    labeled, other = fetch_data(conn)

    X_text = [row["text"] for row in labeled]
    y = [row["feature_area"] for row in labeled]

    # Filter classes with too few examples
    from collections import Counter
    cnt = Counter(y)
    keep_classes = {c for c, n in cnt.items() if n >= MIN_TRAIN_PER_CLASS}

    X_text = [t for t, c in zip(X_text, y) if c in keep_classes]
    y = [c for c in y if c in keep_classes]

    print("Training rows:", len(y), "Classes:", len(keep_classes))

    from sklearn.feature_extraction.text import TfidfVectorizer
    from scipy.sparse import hstack

    # word ngrams
    vec_word = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    min_df=2,
    max_features=20000,
    )

    # character ngrams (great for typos/variants)
    vec_char = TfidfVectorizer(
    analyzer="char_wb",
    ngram_range=(3, 5),
    min_df=2,
    max_features=30000,
    )

    Xw = vec_word.fit_transform(X_text)
    Xc = vec_char.fit_transform(X_text)
    X = hstack([Xw, Xc])


    clf = LogisticRegression(
        max_iter=2000,
        class_weight="balanced"
    )
    clf.fit(X, y)

    other_ids = [row["review_row_id"] for row in other]
    other_text = [row["text"] for row in other]

    if not other_text:
        print("No 'Other' rows to relabel.")
        exit()

    Xo = hstack([vec_word.transform(other_text), vec_char.transform(other_text)])

    probs = clf.predict_proba(Xo)
    pred = clf.classes_[np.argmax(probs, axis=1)]
    conf = np.max(probs, axis=1)

    from collections import Counter
    print("Prediction confidence buckets:")
    print(Counter(int(c * 10) / 10 for c in conf))
    
    updates = 0
    for rid, p, c in zip(other_ids, pred, conf):
        if c >= CONF_THRESHOLD:
            conn.execute(
                "UPDATE enriched_reviews SET feature_area=? WHERE review_row_id=?",
                (str(p), int(rid)),
            )
            updates += 1

    conn.commit()
    print("Relabeled from Other:", updates, "out of", len(other_ids))
