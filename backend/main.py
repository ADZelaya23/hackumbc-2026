"""FastAPI backend.

    uvicorn backend.main:app --reload

Two endpoints:
  POST /api/dashboard  -- the four initial outputs, computed deterministically
  POST /api/chat       -- grounded follow-up Q&A via Snowflake Cortex

Both take the same ProfileRequest so the chat stays anchored to whatever the
dashboard already showed.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.cortex import ask as cortex_ask
from backend.models import ChatRequest, ChatResponse, DashboardResponse, ProfileRequest
from backend.queries.activities import correlated_activities
from backend.queries.career_path import alumni_pathways, typical_first_jobs
from backend.queries.salary import salary_lens

app = FastAPI(title="Career Navigator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok", "env": settings.app_env}


@app.post("/api/dashboard", response_model=DashboardResponse)
def dashboard(profile: ProfileRequest):
    return DashboardResponse(
        salary=salary_lens(profile.job_family),
        typical_first_jobs=typical_first_jobs(profile.major, profile.track),
        alumni_pathways=alumni_pathways(profile.job_family),
        correlated_activities=correlated_activities(profile.job_family),
    )


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Rebuild the same computed context the dashboard used, so the model is
    # answering from numbers that are already on the person's screen.
    d = dashboard(request.profile)
    context = (
        f"Job family: {request.profile.job_family}. "
        f"Entry salary median: {d.salary['entry']['median']} "
        f"(n={d.salary['entry']['n']}). "
        f"Typical first jobs: {d.typical_first_jobs}. "
        f"Common next roles: {d.alumni_pathways}. "
        f"Correlated activities: {d.correlated_activities}."
    )
    answer = cortex_ask(request.question, context)
    return ChatResponse(answer=answer)
