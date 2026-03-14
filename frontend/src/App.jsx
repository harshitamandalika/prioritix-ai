import React, { useEffect, useState } from "react";
import {
  getFeatureTable,
  getClusters,
  getClusterSamples,
  fetchFeedbackSummary,
} from "./api";

function App() {
  const [featureTable, setFeatureTable] = useState([]);
  const [clusters, setClusters] = useState([]);
  const [selectedClusterId, setSelectedClusterId] = useState(null);
  const [clusterSamples, setClusterSamples] = useState([]);

  const [summaryLoading, setSummaryLoading] = useState(false);
  const [summaryData, setSummaryData] = useState(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true);
        setError("");

        const [featureData, clusterData] = await Promise.all([
          getFeatureTable(),
          getClusters(),
        ]);

        setFeatureTable(featureData);
        setClusters(clusterData);

        if (clusterData.length > 0) {
          const firstClusterId = clusterData[0].cluster_id;
          setSelectedClusterId(firstClusterId);

          const samples = await getClusterSamples(firstClusterId);
          setClusterSamples(samples);
        }
      } catch (err) {
        setError(err.message || "Failed to load dashboard.");
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  const handleClusterClick = async (clusterId) => {
    try {
      setError("");
      setSelectedClusterId(clusterId);
      const samples = await getClusterSamples(clusterId);
      setClusterSamples(samples);
    } catch (err) {
      setError(err.message || "Failed to load cluster samples.");
    }
  };

  const handleGenerateSummary = async () => {
    try {
      setSummaryLoading(true);
      setError("");

      const result = await fetchFeedbackSummary({
        maxReviews: 100,
        includeSampleReviews: true,
      });

      setSummaryData(result);
    } catch (err) {
      setError(err.message || "Failed to generate summary.");
    } finally {
      setSummaryLoading(false);
    }
  };

  return (
    <div style={{ padding: "24px", fontFamily: "Arial, sans-serif" }}>
      <h1>Prioritix AI Dashboard</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <div
        style={{
          border: "1px solid #ddd",
          borderRadius: "12px",
          padding: "16px",
          marginBottom: "24px",
        }}
      >
        <h2>AI Executive Summary</h2>
        <button onClick={handleGenerateSummary} disabled={summaryLoading}>
          {summaryLoading ? "Generating..." : "Generate Summary"}
        </button>

        {summaryData?.structured_summary && (
          <div style={{ marginTop: "16px" }}>
            <h3>Executive Summary</h3>
            <p>{summaryData.structured_summary.executive_summary}</p>

            <h3>Top Pain Points</h3>
            <ul>
              {summaryData.structured_summary.top_pain_points?.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>

            <h3>Urgent Issues</h3>
            <ul>
              {summaryData.structured_summary.urgent_issues?.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>

            <h3>Recommended Priorities</h3>
            <ul>
              {summaryData.structured_summary.recommended_priorities?.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {loading ? (
        <p>Loading dashboard...</p>
      ) : (
        <>
          <div
            style={{
              border: "1px solid #ddd",
              borderRadius: "12px",
              padding: "16px",
              marginBottom: "24px",
            }}
          >
            <h2>Feature Table</h2>
            <table
              style={{
                width: "100%",
                borderCollapse: "collapse",
                marginTop: "12px",
              }}
            >
              <thead>
                <tr>
                  <th style={{ borderBottom: "1px solid #ccc", textAlign: "left", padding: "8px" }}>Feature</th>
                  <th style={{ borderBottom: "1px solid #ccc", textAlign: "left", padding: "8px" }}>Total</th>
                  <th style={{ borderBottom: "1px solid #ccc", textAlign: "left", padding: "8px" }}>Positive</th>
                  <th style={{ borderBottom: "1px solid #ccc", textAlign: "left", padding: "8px" }}>Neutral</th>
                  <th style={{ borderBottom: "1px solid #ccc", textAlign: "left", padding: "8px" }}>Negative</th>
                  <th style={{ borderBottom: "1px solid #ccc", textAlign: "left", padding: "8px" }}>High Urgency</th>
                </tr>
              </thead>
              <tbody>
                {featureTable.map((row, idx) => (
                  <tr key={idx}>
                    <td style={{ borderBottom: "1px solid #eee", padding: "8px" }}>{row.feature_area}</td>
                    <td style={{ borderBottom: "1px solid #eee", padding: "8px" }}>{row.total_reviews}</td>
                    <td style={{ borderBottom: "1px solid #eee", padding: "8px" }}>{row.positive}</td>
                    <td style={{ borderBottom: "1px solid #eee", padding: "8px" }}>{row.neutral}</td>
                    <td style={{ borderBottom: "1px solid #eee", padding: "8px" }}>{row.negative}</td>
                    <td style={{ borderBottom: "1px solid #eee", padding: "8px" }}>{row.high_urgency}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "24px",
            }}
          >
            <div
              style={{
                border: "1px solid #ddd",
                borderRadius: "12px",
                padding: "16px",
              }}
            >
              <h2>Clusters</h2>
              {clusters.length === 0 ? (
                <p>No clusters found.</p>
              ) : (
                clusters.map((cluster) => (
                  <div
                    key={cluster.cluster_id}
                    onClick={() => handleClusterClick(cluster.cluster_id)}
                    style={{
                      padding: "12px",
                      marginBottom: "10px",
                      border:
                        selectedClusterId === cluster.cluster_id
                          ? "2px solid #333"
                          : "1px solid #ddd",
                      borderRadius: "10px",
                      cursor: "pointer",
                    }}
                  >
                    <strong>Cluster {cluster.cluster_id}</strong>
                    <p style={{ margin: "6px 0" }}>
                      Top Features: {cluster.top_features?.join(", ") || "N/A"}
                    </p>
                    <p style={{ margin: 0 }}>
                      Reviews: {cluster.review_count}
                    </p>
                  </div>
                ))
              )}
            </div>

            <div
              style={{
                border: "1px solid #ddd",
                borderRadius: "12px",
                padding: "16px",
              }}
            >
              <h2>Cluster Samples</h2>
              {clusterSamples.length === 0 ? (
                <p>No samples found.</p>
              ) : (
                clusterSamples.map((sample, idx) => (
                  <div
                    key={idx}
                    style={{
                      padding: "12px",
                      marginBottom: "10px",
                      border: "1px solid #eee",
                      borderRadius: "10px",
                    }}
                  >
                    <p style={{ marginBottom: "8px" }}>{sample.review_text}</p>
                    <small>
                      Sentiment: {sample.sentiment} | Urgency: {sample.urgency} | Feature: {sample.feature_area}
                    </small>
                  </div>
                ))
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
