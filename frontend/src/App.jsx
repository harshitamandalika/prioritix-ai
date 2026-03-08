import React, { useState } from "react";
import Dashboard from "./pages/Dashboard";
import Clusters from "./pages/Clusters";
import Copilot from "./pages/Copilot";


export default function App() {
  const [tab, setTab] = useState("dashboard");

  return (
    <div>
      <header style={{ padding: 12, background: "#111827", color: "white" }}>
        <h2>Prioritix AI</h2>
      </header>

      <nav style={{ padding: 12, borderBottom: "1px solid #ddd" }}>
        <button onClick={() => setTab("dashboard")}>Dashboard</button>{" "}
        <button onClick={() => setTab("clusters")}>Clusters</button>
        <button onClick={() => setTab("copilot")}>Copilot</button>
      </nav>

      {tab === "dashboard" && <Dashboard />}
      {tab === "clusters" && <Clusters />}
      {tab === "copilot" && <Copilot />}
    </div>
  );
}
