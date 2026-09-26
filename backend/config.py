"""Centralized env var access. Import `settings` everywhere else."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    snowflake_account: str = os.environ.get("SNOWFLAKE_ACCOUNT", "")
    snowflake_user: str = os.environ.get("SNOWFLAKE_USER", "")
    snowflake_password: str = os.environ.get("SNOWFLAKE_PASSWORD", "")
    snowflake_role: str = os.environ.get("SNOWFLAKE_ROLE", "ACCOUNTADMIN")
    snowflake_warehouse: str = os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
    snowflake_database: str = os.environ.get("SNOWFLAKE_DATABASE", "CAREER_NAVIGATOR")
    snowflake_schema: str = os.environ.get("SNOWFLAKE_SCHEMA", "PUBLIC")

    cortex_model: str = os.environ.get("CORTEX_MODEL", "llama3.1-70b")

    cors_origins: str = os.environ.get("CORS_ORIGINS", "http://localhost:3000")
    app_env: str = os.environ.get("APP_ENV", "development")


settings = Settings()
