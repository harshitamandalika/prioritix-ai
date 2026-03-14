from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from summary_routes import router as summary_router
from dashboard_routes import router as dashboard_router

app = FastAPI(title="Prioritix AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(summary_router)
app.include_router(dashboard_router)


@app.get("/")
def health_check():
    return {"status": "ok"}