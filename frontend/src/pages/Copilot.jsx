import React, { useState } from "react";

export default function Copilot() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  async function ask() {
    setLoading(true);
    setAnswer("");

    const res = await fetch("http://localhost:8000/copilot/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const data = await res.json();
    setAnswer(data.answer);
    setLoading(false);
  }

  return (
    <div style={{ padding: 16 }}>
      <h3>Prioritix AI Copilot</h3>

      <textarea
        rows={4}
        style={{ width: "100%" }}
        placeholder="Ask: What should we fix first?"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={ask} disabled={loading} style={{ marginTop: 8 }}>
        {loading ? "Thinking..." : "Ask"}
      </button>

      {answer && (
        <pre
          style={{
            marginTop: 16,
            background: "#f3f4f6",
            padding: 12,
            whiteSpace: "pre-wrap",
          }}
        >
          {answer}
        </pre>
      )}
    </div>
  );
}
