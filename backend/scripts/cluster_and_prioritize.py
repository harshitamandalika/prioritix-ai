from backend.db import get_conn
from backend.services.clustering import cluster
from backend.services.prioritization import compute

conn = get_conn()
texts = [r["short_summary"] for r in conn.execute(
    "SELECT short_summary FROM enriched_reviews"
)]

labels = cluster(texts)
print("Clusters created:", len(set(labels)))

print("Priorities:")
for f, s in compute():
    print(f, round(s, 2))
