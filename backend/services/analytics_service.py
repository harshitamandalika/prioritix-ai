from collections import Counter
from typing import List, Dict, Any


def build_summary_input(reviews: List[Dict[str, Any]], include_sample_reviews: bool = True) -> Dict[str, Any]:
    sentiment_counts = Counter()
    urgency_counts = Counter()
    feature_counts = Counter()
    high_urgency_negative_reviews = []

    for review in reviews:
        sentiment = (review.get("sentiment") or "unknown").lower()
        urgency = review.get("urgency") or 0
        feature_area = review.get("feature_area") or "unknown"
        text = review.get("review_text", "")

        sentiment_counts[sentiment] += 1
        urgency_counts[str(urgency)] += 1
        feature_counts[feature_area] += 1

        if sentiment == "negative" and urgency >= 4:
            high_urgency_negative_reviews.append({
                "feature_area": feature_area,
                "review_text": text
            })

    summary_input = {
        "total_reviews": len(reviews),
        "sentiment_breakdown": dict(sentiment_counts),
        "urgency_breakdown": dict(urgency_counts),
        "top_feature_areas": dict(feature_counts.most_common(10)),
        "high_urgency_negative_count": len(high_urgency_negative_reviews),
        "high_urgency_negative_examples": high_urgency_negative_reviews[:10],
    }

    if include_sample_reviews:
        summary_input["sample_reviews"] = [
            {
                "feature_area": r.get("feature_area") or "unknown",
                "sentiment": r.get("sentiment") or "unknown",
                "urgency": r.get("urgency") or 0,
                "review_text": r.get("review_text", "")
            }
            for r in reviews[:20]
        ]

    return summary_input