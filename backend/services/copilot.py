# backend/services/copilot.py

from backend.db import get_conn

def answer_offline(question: str) -> str:
    """
    Offline copilot: answers using existing analytics (no LLM).
    """

    conn = get_conn()

    # Top priority features
    features = conn.execute("""
        SELECT feature_area,
               COUNT(*) AS freq,
               AVG(urgency) AS avg_urgency
        FROM enriched_reviews
        WHERE issue_type = 'Complaint' 
            AND feature_area != 'Generic Issue'
        GROUP BY feature_area
        ORDER BY freq * avg_urgency DESC
        LIMIT 3
    """).fetchall()

    # Top clusters
    clusters = conn.execute("""
        SELECT cluster_id, label, size
        FROM clusters
        ORDER BY size DESC
        LIMIT 3
    """).fetchall()

    top_cluster_id = clusters[0]["cluster_id"] if clusters else None

    examples = []
    if top_cluster_id is not None:
        ex_rows = conn.execute("""
            SELECT short_summary
            FROM enriched_reviews
            WHERE cluster_id = ?
                AND short_summary IS NOT NULL
            ORDER BY urgency DESC
            LIMIT 5
        """, (int(top_cluster_id),)).fetchall()

        examples = [r["short_summary"] for r in ex_rows]

    lines = []
    lines.append("Top issues based on user feedback:\n")

    for f in features:
        lines.append(
            f"- {f['feature_area']} (frequency={f['freq']}, avg urgency={f['avg_urgency']:.1f})"
        )

    lines.append("\nMajor recurring themes:")
    for c in clusters:
        lines.append(f"- {c['label']} ({c['size']} reviews)")
    if examples:
        lines.append("\nExample high-urgency user complaints (from top theme):")
        for s in examples:
            lines.append(f"- {s}")

    lines.append("\nRecommended action:")
    lines.append("Focus on the highest-frequency, high-urgency issues first.")

    return "\n".join(lines)
