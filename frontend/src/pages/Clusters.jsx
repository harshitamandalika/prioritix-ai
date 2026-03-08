import React, { useEffect, useState } from "react";
import { getClusters, getClusterSamples } from "../api";

export default function Clusters() {
  const [clusters, setClusters] = useState([]);
  const [selected, setSelected] = useState(null);
  const [samples, setSamples] = useState([]);

  useEffect(() => {
    (async () => {
      const res = await getClusters();
      setClusters(res);
    })();
  }, []);

  async function selectCluster(c) {
    setSelected(c);
    const res = await getClusterSamples(c.cluster_id);
    setSamples(res);
  }

  return (
    <div
      style={{
        padding: 16,
        display: "grid",
        gridTemplateColumns: "1fr 2fr",
        gap: 16,
      }}
    >
      <div>
        <h3>Clusters</h3>
        {clusters.map((c) => (
          <div key={c.cluster_id} style={{ marginBottom: 6 }}>
            <button onClick={() => selectCluster(c)}>
              Cluster {c.cluster_id} ({c.size})
            </button>
          </div>
        ))}
      </div>

      <div>
        <h3>Samples</h3>
        {!selected && <p>Select a cluster to view reviews.</p>}

        {samples.map((s, i) => (
          <div
            key={i}
            style={{
              border: "1px solid #ddd",
              padding: 10,
              marginBottom: 10,
              background: "white",
            }}
          >
            <div style={{ fontSize: 12, color: "#555" }}>
              {s.feature_area} | {s.issue_type} | urgency {s.urgency} |{" "}
              {s.sentiment}
            </div>
            <div style={{ marginTop: 6 }}>{s.short_summary}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
