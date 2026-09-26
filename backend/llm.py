"""DigitalOcean Gradient AI Platform -- serverless inference wrapper.

The pattern here on purpose: the LLM never sees raw CSV rows. Callers pass
in `computed_context` -- numbers already produced by our own SQL/pandas
queries (see backend/queries/) -- and the model's only job is to explain
those numbers in plain language. This keeps every answer traceable back to
an actual aggregate over the data, per the project's honesty requirement.

DigitalOcean's serverless inference API is OpenAI-compatible, so we just
point the standard `openai` client at DigitalOcean's base URL with a model
access key instead of an OpenAI key. Get a model access key from the
DigitalOcean Control Panel (AI Platform -> Serverless Inference -> Model
Access Keys), or via POST /v2/gen-ai/models/api_keys.

Available model names can change -- confirm what your account currently
has access to with:
    GET https://inference.do-ai.run/v1/models
    (Authorization: Bearer <DO_MODEL_ACCESS_KEY>)
before relying on the DO_INFERENCE_MODEL value in .env.
"""

from openai import OpenAI

from backend.config import settings

SYSTEM_INSTRUCTIONS = (
    "You are a career-outcomes assistant for UMBC students, working from a "
    "synthetic (fabricated, not real UMBC data) dataset of alumni and current "
    "students. Answer ONLY using the computed statistics provided below -- "
    "never invent a number, employer, or salary that isn't in them. If the "
    "provided context doesn't answer the question, say so plainly instead of "
    "guessing. Keep answers concise (3-5 sentences) and mention this data is "
    "synthetic if the person seems to be treating it as real."
)

_client = OpenAI(
    base_url=settings.do_inference_base_url,
    api_key=settings.do_model_access_key,
)


def ask(question: str, computed_context: str) -> str:
    """Send a grounded question to DigitalOcean's inference API and return
    the model's text reply.

    `computed_context` should be a short, already-aggregated summary (e.g.
    "Median first-year salary for Software Engineering, Entry level: $78,500
    (n=142). Most common next role: Software Engineer II (61% of promotions)."
    ) -- not raw rows.
    """
    response = _client.chat.completions.create(
        model=settings.do_inference_model,
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": f"COMPUTED CONTEXT:\n{computed_context}\n\nQUESTION: {question}"},
        ],
    )
    return response.choices[0].message.content
