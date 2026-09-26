# Career Navigator — HackUMBC 2026

An application that turns UMBC's synthetic career/alumni dataset into two things
a student can actually use:

1. **A dashboard** — answer a few simple questions (major, track, interests) and
   get back a salary lens graph, a typical first job, what alumni like you did,
   and activities correlated with your interest area.
2. **A grounded chat** — ask follow-up questions and get answers backed by the
   real rows behind them, not invented numbers.

## Architecture

```
GitHub  ──push──▶  DigitalOcean App Platform (hosts this app)
                          │
                          ▼
                     backend/ (FastAPI)
                          │
              ┌───────────┴────────────┐
              ▼                        ▼
        pandas analytics        Snowflake Cortex
        (dashboard queries)     (SNOWFLAKE.CORTEX.COMPLETE,
              │                  grounded chat answers)
              ▼                        │
        Snowflake tables ◀─────────────┘
              ▲
              │ COPY INTO
        DigitalOcean Spaces (raw CSV data lake, optional)
```

See [`docs/architecture.md`](docs/architecture.md) for the full write-up.

## Repo layout

```
career-navigator/
├── data/                  # CSVs go here locally (gitignored — see data/README.md)
├── ingest/                # one-time scripts: load CSVs -> Spaces -> Snowflake
├── backend/               # FastAPI app: dashboard queries + Cortex chat
├── frontend/              # the GUI (React or Streamlit — TBD by the team)
├── docs/                  # architecture notes, diagrams
└── .github/workflows/     # CI
```

## Setup

1. **Get the data.** Download the six CSVs from the
   [hackumbc-2026 dataset repo](https://github.com/jasonpaluck/hackumbc-2026)
   into `data/`.

2. **Copy the env template.**
   ```bash
   cp .env.example .env
   # fill in your Snowflake and DigitalOcean Spaces credentials
   ```

3. **Install dependencies.**
   ```bash
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Load the data into Snowflake.**
   ```bash
   python ingest/load_to_snowflake.py
   ```
   (Optionally, run `python ingest/upload_to_spaces.py` first if you want the
   raw CSVs backed by DigitalOcean Spaces as the source of truth instead of
   loading straight from your laptop — see that script's docstring.)

5. **Run the backend locally.**
   ```bash
   uvicorn backend.main:app --reload
   ```

6. **Run the frontend** — see `frontend/README.md` once the team picks a stack.

## Deployment

Push to `main` on GitHub; DigitalOcean App Platform is configured to
auto-deploy from this repo (App Platform → Create Resource from Source →
point at this repo). Secrets (Snowflake creds, etc.) are set in App
Platform's environment variable panel, **not** committed to the repo.

## Environment variables

See `.env.example` for the full list. Never commit a real `.env` file —
it's already in `.gitignore`.
