"""Centralized env var access. Import `settings` everywhere else."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    # DigitalOcean Managed PostgreSQL -- the full connection string from the
    # cluster's "Connection Details" panel, e.g.:
    # postgresql://doadmin:PASSWORD@app-xxxx-do-user-1234-0.db.ondigitalocean.com:25060/defaultdb?sslmode=require
    database_url: str = os.environ.get("DATABASE_URL", "")

    # DigitalOcean Gradient AI Platform -- serverless inference (OpenAI-compatible)
    do_model_access_key: str = os.environ.get("DO_MODEL_ACCESS_KEY", "")
    do_inference_base_url: str = os.environ.get("DO_INFERENCE_BASE_URL", "https://inference.do-ai.run/v1/")
    do_inference_model: str = os.environ.get("DO_INFERENCE_MODEL", "llama3.3-70b-instruct")

    # DigitalOcean Spaces -- optional raw-CSV data lake
    do_spaces_key: str = os.environ.get("DO_SPACES_KEY", "")
    do_spaces_secret: str = os.environ.get("DO_SPACES_SECRET", "")
    do_spaces_region: str = os.environ.get("DO_SPACES_REGION", "nyc3")
    do_spaces_bucket: str = os.environ.get("DO_SPACES_BUCKET", "")
    do_spaces_endpoint: str = os.environ.get("DO_SPACES_ENDPOINT", "")

    cors_origins: str = os.environ.get("CORS_ORIGINS", "http://localhost:3000")
    app_env: str = os.environ.get("APP_ENV", "development")


settings = Settings()
