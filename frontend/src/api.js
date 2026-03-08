const BASE_URL = "http://localhost:8000";

export async function getFeatureTable() {
  const res = await fetch(`${BASE_URL}/features/table`);
  return res.json();
}

export async function getClusters() {
  const res = await fetch(`${BASE_URL}/clusters`);
  return res.json();
}

export async function getClusterSamples(clusterId) {
  const res = await fetch(
    `${BASE_URL}/clusters/${clusterId}/samples?limit=15`
  );
  return res.json();
}
