# Career Navigator — HackUMBC 2026

An application that turns UMBC's synthetic career/alumni dataset into two things
a student can actually use:

1. **A dashboard** — answer a few simple questions (major, track, interests) and
   get back a salary lens graph, a typical first job, what alumni like you did,
   and activities correlated with your interest area.
2. **A grounded chat** — ask follow-up questions and get answers backed by the
   real rows behind them, not invented numbers.

Built entirely on DigitalOcean (provided via MLH for this hackathon): Managed
PostgreSQL as the data warehouse, Gradient AI Platform serverless inference as
the LLM, Spaces as an optional raw-data backup, and App Platform for hosting.

## Architecture

```
GitHub  ──push──▶  DigitalOcean App Platform (hosts this app)
                          │
                          ▼
                     backend/ (FastAPI)
                          │
              ┌───────────┴────────────┐
              ▼                        ▼
        pandas analytics       DigitalOcean Gradient AI
        (dashboard queries)    Platform (serverless inference,
              │                 OpenAI-compatible API,
              ▼                 grounded chat answers)
     DigitalOcean Managed              │
     PostgreSQL  ◀────────────────────-┘
              ▲
              │ COPY (bulk load)
     local CSVs (data/), optionally
     backed up to DigitalOcean Spaces
```

See [`docs/architecture.md`](docs/architecture.md) for the full write-up.

## Repo layout

```
career-navigator/
├── data/                  # CSVs go here locally (gitignored — see data/README.md)
├── ingest/                # one-time scripts: load CSVs -> Postgres, optionally -> Spaces
├── backend/               # FastAPI app: dashboard queries + Gradient AI chat
├── frontend/               # the GUI (React or Streamlit — TBD by the team)
├── docs/                   # architecture notes, diagrams
└── .github/workflows/      # CI
```

## Setup

1. **Get the data.** Download the six CSVs from the
   [hackumbc-2026 dataset repo](https://github.com/jasonpaluck/hackumbc-2026)
   into `data/` (and `data/sample/` for the 10% cut, useful for fast iteration).

2. **Create a DigitalOcean Managed PostgreSQL cluster** (Control Panel ->
   Databases -> Create Database Cluster -> PostgreSQL). Copy the connection
   string from its "Connection Details" panel.

3. **Create a DigitalOcean Gradient AI Platform Model Access Key**
   (Control Panel -> AI Platform -> Serverless Inference -> Model Access
   Keys), and confirm which model names are available to your account:
   ```bash
   curl https://inference.do-ai.run/v1/models \
     -H "Authorization: Bearer <your model access key>"
   ```

4. **Copy the env template.**
   ```bash
   cp .env.example .env
   # fill in DATABASE_URL, DO_MODEL_ACCESS_KEY, DO_INFERENCE_MODEL, etc.
   ```

5. **Install dependencies.**
   ```bash
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Load the data into Postgres.**
   ```bash
   python ingest/load_to_postgres.py --source data/sample   # quick test load
   python ingest/load_to_postgres.py                        # full load
   ```
   (Optionally, run `python ingest/upload_to_spaces.py` too, to keep a raw
   copy of the CSVs in a DigitalOcean Spaces bucket — this is a backup/data
   lake step, separate from what the app actually queries.)

7. **Run the backend locally.**
   ```bash
   uvicorn backend.main:app --reload
   ```

8. **Run the frontend** — see `frontend/README.md` once the team picks a stack.

## Deployment

Push to `main` on GitHub; DigitalOcean App Platform is configured to
auto-deploy from this repo (App Platform → Create Resource from Source →
point at this repo). Secrets (database URL, model access key, etc.) are set
in App Platform's environment variable panel, **not** committed to the repo.

## Environment variables

See `.env.example` for the full list. Never commit a real `.env` file —
it's already in `.gitignore`.
