# Frontend

Not scaffolded yet -- pick one and build it here:

- **React** (more polished, more setup) -- talks to the FastAPI backend at
  `/api/dashboard` and `/api/chat`.
- **Streamlit** (fastest, Python-only) -- can live in this repo as
  `frontend/app.py` and skip a separate JS build entirely; still calls the
  same backend endpoints, or import `backend/queries/*` directly if you'd
  rather skip the HTTP hop for the dashboard step.

Whichever is chosen, DigitalOcean App Platform just needs a build/run
command for this folder (or the Streamlit entrypoint) -- see
`docs/architecture.md` for the deploy notes.
