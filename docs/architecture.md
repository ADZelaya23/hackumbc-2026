# Architecture

## Why this shape

The project has two phases with different honesty requirements:

1. **The initial dashboard** (salary lens, typical first job, alumni
   pathways, correlated activities) must be exactly reproducible from the
   data -- these are aggregates, not opinions. So this phase is pure
   SQL/pandas, no LLM involved.
2. **The follow-up chat** is where an LLM adds value (natural language,
   flexible questions) -- but per the dataset's own judging criteria
   ("grounded in these rows, citing the records behind every claim"), the
   model must not be allowed to invent numbers. So the chat endpoint always
   recomputes the same aggregates the dashboard used and hands them to the
   model as `computed_context`; the model's job is explanation, not
   retrieval.

Same backend query functions power both phases -- the dashboard just calls
them directly, and the chat endpoint calls them to build context before
asking the LLM.

## Why DigitalOcean end-to-end

For this hackathon, DigitalOcean is provided via MLH, and it covers every
role the app needs:

- **Data warehouse:** DigitalOcean Managed PostgreSQL. The six CSVs are
  bulk-loaded via Postgres's native `COPY` command.
- **LLM:** DigitalOcean Gradient AI Platform's serverless inference. Its API
  is OpenAI-compatible (`/v1/chat/completions`), so the backend just points
  the standard `openai` Python client at DigitalOcean's base URL with a
  model access key instead of an OpenAI key.
- **Optional data lake:** DigitalOcean Spaces (S3-compatible object storage)
  can hold a raw backup copy of the CSVs, independent of what's loaded into
  Postgres.
- **Hosting:** DigitalOcean App Platform, auto-deploying from this GitHub
  repo on every push to `main`.

## Data flow

```
data/*.csv (from the hackumbc-2026 dataset repo)
      │
      ├── ingest/upload_to_spaces.py   ──▶  DigitalOcean Spaces (raw backup, optional)
      │
      └── ingest/load_to_postgres.py   ──▶  DigitalOcean Managed PostgreSQL
                                                   (ingest/schema.sql)
                                                   │
                                      backend/queries/*.py (SQL via
                                      psycopg2 -> pandas)
                                                   │
                        ┌──────────────────────────┴─────────────────────────┐
                        ▼                                                    ▼
              POST /api/dashboard                                  POST /api/chat
              (deterministic aggregates)                 (same aggregates -> DigitalOcean
                                                            Gradient AI -> natural-language answer)
                        │                                                    │
                        └────────────────────────┬───────────────────────────┘
                                                  ▼
                                           frontend/ (GUI)
```

## Deploying

1. Create a DigitalOcean App Platform app pointed at this GitHub repo.
2. Set the same variables from `.env.example` as encrypted App Platform env
   vars (Settings -> App-Level Environment Variables). Never put real
   credentials in the repo.
3. App Platform auto-deploys on every push to `main`.
4. Make sure the Managed PostgreSQL cluster's trusted sources / firewall
   allows connections from your App Platform app (DigitalOcean lets you add
   an App Platform app directly as a trusted source on the database
   cluster's settings page).

## Known simplifications (call these out to judges, don't hide them)

- Salaries are compared in nominal dollars in the current query code --
  cross-year comparisons should be flagged as such, or adjusted, before
  being presented as a finding.
- `No Response` alumni (~15%) are implicitly excluded wherever we filter
  `first_job_title != 'Not Applicable'`. That's a deliberate choice, and it
  should be stated whenever placement rates are shown.
- The skill-gap comparison (`backend/queries/skill_gap.py`) is a starting
  point, not a proof of anything causal -- same caveat the dataset's own
  `examples/explore_python.py` ends on.
- Model availability on DigitalOcean's serverless inference API can change;
  confirm the current model list (`GET /v1/models`) rather than assuming
  `DO_INFERENCE_MODEL`'s default is still valid.
