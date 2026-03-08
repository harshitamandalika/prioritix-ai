import React, { useEffect, useState } from "react";
import { getFeatureTable } from "../api";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function Dashboard() {
  const [data, setData] = useState([]);

  useEffect(() => {
    (async () => {
      const res = await getFeatureTable();
      setData(res);
    })();
  }, []);

  return (
    <div style={{ padding: 16 }}>
      <h3>Feature Priorities</h3>

      <div style={{ height: 300 }}>
        <ResponsiveContainer>
          <BarChart data={data.slice(0, 10)}>
            <XAxis dataKey="feature_area" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="priority_score" fill="#2563eb" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <h3 style={{ marginTop: 20 }}>Detailed Table</h3>
      <table>
        <thead>
          <tr>
            <th>Feature</th>
            <th>Frequency</th>
            <th>Negative %</th>
            <th>Avg Urgency</th>
            <th>Priority Score</th>
          </tr>
        </thead>
        <tbody>
          {data.map((r) => (
            <tr key={r.feature_area}>
              <td>{r.feature_area}</td>
              <td>{r.frequency}</td>
              <td>{(r.negative_ratio * 100).toFixed(1)}%</td>
              <td>{r.avg_urgency.toFixed(2)}</td>
              <td>{r.priority_score.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
