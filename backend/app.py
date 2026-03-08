from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.db import get_conn
from pydantic import BaseModel
from backend.services.copilot import answer_offline


app = FastAPI(title="Prioritix AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/features/table")
def feature_table():
    conn = get_conn()
    rows = conn.execute("""
        SELECT feature_area,
               COUNT(*) AS frequency,
               AVG(CASE WHEN sentiment='negative' THEN 1.0 ELSE 0.0 END) AS negative_ratio,
               AVG(urgency) AS avg_urgency
        FROM enriched_reviews
        GROUP BY feature_area
    """).fetchall()

    out = []
    for r in rows:
        priority = float(r["frequency"]) * float(r["avg_urgency"]) * float(r["negative_ratio"])
        out.append({
            "feature_area": r["feature_area"],
            "frequency": int(r["frequency"]),
            "negative_ratio": float(r["negative_ratio"]),
            "avg_urgency": float(r["avg_urgency"]),
            "priority_score": float(priority),
        })

    out.sort(key=lambda x: x["priority_score"], reverse=True)
    return out

@app.get("/clusters")
def clusters():
    conn = get_conn()
    rows = conn.execute("""
        SELECT cluster_id, label, size
        FROM clusters
        ORDER BY size DESC
    """).fetchall()
    return [dict(r) for r in rows]

@app.get("/clusters/{cluster_id}/samples")
def cluster_samples(cluster_id: int, limit: int = 15):
    conn = get_conn()
    rows = conn.execute("""
        SELECT short_summary, feature_area, issue_type, urgency, sentiment
        FROM enriched_reviews
        WHERE cluster_id = ?
        ORDER BY urgency DESC
        LIMIT ?
    """, (cluster_id, limit)).fetchall()
    return [dict(r) for r in rows]

class CopilotRequest(BaseModel):
    question: str


@app.post("/copilot/chat")
def copilot_chat(req: CopilotRequest):
    answer = answer_offline(req.question)
    return {"answer": answer}
