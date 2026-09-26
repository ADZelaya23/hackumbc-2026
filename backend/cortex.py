"""Snowflake Cortex COMPLETE wrapper.

The pattern here on purpose: the LLM never sees raw CSV rows. Callers pass
in `computed_context` -- numbers already produced by our own SQL/pandas
queries (see backend/queries/) -- and the model's only job is to explain
those numbers in plain language. This keeps every answer traceable back to
an actual aggregate over the data, per the project's honesty requirement.

Model availability varies by Snowflake account/region and changes over
time -- confirm the exact model name your account can see with:
    SHOW MODELS IN SNOWFLAKE.CORTEX;
before relying on the CORTEX_MODEL value in .env.
"""

from backend.config import settings
from backend.snowflake_client import run_sql

SYSTEM_INSTRUCTIONS = (
    "You are a career-outcomes assistant for UMBC students, working from a "
    "synthetic (fabricated, not real UMBC data) dataset of alumni and current "
    "students. Answer ONLY using the computed statistics provided below -- "
    "never invent a number, employer, or salary that isn't in them. If the "
    "provided context doesn't answer the question, say so plainly instead of "
    "guessing. Keep answers concise (3-5 sentences) and mention this data is "
    "synthetic if the person seems to be treating it as real."
)


def ask(question: str, computed_context: str) -> str:
    """Send a grounded question to Cortex and return the model's text reply.

    `computed_context` should be a short, already-aggregated summary (e.g.
    "Median first-year salary for Software Engineering, Entry level: $78,500
    (n=142). Most common next role: Software Engineer II (61% of promotions)."
    ) -- not raw rows.
    """
    prompt = (
        f"{SYSTEM_INSTRUCTIONS}\n\n"
        f"COMPUTED CONTEXT:\n{computed_context}\n\n"
        f"QUESTION: {question}"
    )

    rows = run_sql(
        "SELECT SNOWFLAKE.CORTEX.COMPLETE(%(model)s, %(prompt)s)",
        {"model": settings.cortex_model, "prompt": prompt},
    )
    return rows[0][0] if rows else ""
