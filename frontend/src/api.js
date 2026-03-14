const BASE_URL = "http://127.0.0.1:8000";

export async function getFeatureTable() {
  const res = await fetch(`${BASE_URL}/features/table`);
  if (!res.ok) throw new Error("Failed to fetch feature table");
  return res.json();
}

export async function getClusters() {
  const res = await fetch(`${BASE_URL}/clusters`);
  if (!res.ok) throw new Error("Failed to fetch clusters");
  return res.json();
}

export async function getClusterSamples(clusterId) {
  const res = await fetch(`${BASE_URL}/clusters/${clusterId}/samples?limit=15`);
  if (!res.ok) throw new Error("Failed to fetch cluster samples");
  return res.json();
}

export async function fetchFeedbackSummary(payload = {}) {
  const res = await fetch(`${BASE_URL}/summary/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      max_reviews: payload.maxReviews ?? 100,
      include_sample_reviews: payload.includeSampleReviews ?? true,
    }),
  });

  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || "Failed to generate summary");
  }

  return res.json();
}
