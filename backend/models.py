from pydantic import BaseModel


class ProfileRequest(BaseModel):
    """What the intake form collects."""
    major: str                      # "Computer Science" | "Information Systems"
    track: str | None = None
    job_family: str                 # curated interest -> job_family mapping happens in the frontend/form
    residency: str | None = None
    entry_type: str | None = None


class DashboardResponse(BaseModel):
    salary: dict
    typical_first_jobs: list[dict]
    alumni_pathways: list[dict]
    correlated_activities: list[dict]


class ChatRequest(BaseModel):
    question: str
    profile: ProfileRequest  # carried forward so chat stays scoped to the same context


class ChatResponse(BaseModel):
    answer: str
