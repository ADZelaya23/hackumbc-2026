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
   recomputes the same aggregates the dashboard used and hands them to
   Cortex as `computed_context`; the model's job is explanation, not
   retrieval.

Same backend query functions power both phases -- the dashboard just calls
them directly, and the chat endpoint calls them to build context before
asking Cortex.

## Data flow

```
data/*.csv (from the hackumbc-2026 dataset repo)
      │
      ├── ingest/upload_to_spaces.py  ──▶  DigitalOcean Spaces (raw data lake, optional)
      │
      └── ingest/load_to_snowflake.py ──▶  Snowflake tables (ingest/schema.sql)
                                                  │
                                     backend/queries/*.py (SQL via
                                     snowflake-connector-python -> pandas)
                                                  │
                        ┌─────────────────────────┴─────────────────────────┐
                        ▼                                                   ▼
              POST /api/dashboard                                 POST /api/chat
              (deterministic aggregates)                (same aggregates -> Cortex COMPLETE
                                                           -> natural-language answer)
                        │                                                   │
                        └───────────────────────┬───────────────────────────┘
                                                 ▼
                                          frontend/ (GUI)
```

## Deploying

1. Create a DigitalOcean App Platform app pointed at this GitHub repo.
2. Set the same variables from `.env.example` as encrypted App Platform env
   vars (Settings -> App-Level Environment Variables). Never put real
   credentials in the repo.
3. App Platform auto-deploys on every push to `main`.
4. The backend needs a persistent Snowflake connection at request time --
   no separate always-on server is required beyond the one App Platform
   component running FastAPI (+ frontend, if served from the same process).

## Known simplifications (call these out to judges, don't hide them)

- Salaries are compared in nominal dollars in the current query code --
  cross-year comparisons should be flagged as such, or adjusted, before
  being presented as a finding.
- `No Response` alumni (~15%) are implicitly excluded wherever we filter
  `first_job_title != 'Not Applicable'`. That's a deliberate choice, and it
  should be stated whenever placement rates are shown.
- The skill-gap comparison (`backend/queries/skill_gap.py`) is a starting
  point, not a proof of anything causal -- same caveat the dataset's own
  `explore_python.py` example ends on.
