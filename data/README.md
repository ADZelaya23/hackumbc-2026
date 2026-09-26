# Local data folder

This folder is where the six dataset CSVs live locally. They're gitignored
(see repo root `.gitignore`) so we don't bloat the repo with ~22 MB of data
that already has a canonical home.

Get them from: https://github.com/jasonpaluck/hackumbc-2026

Expected files:

```
data/
├── students_current.csv
├── alumni.csv
├── transcripts.csv
├── employment_history.csv
├── student_experience.csv
├── course_catalog.csv
└── sample/            # optional 10% referentially-complete cut, same filenames
```

`ingest/load_to_snowflake.py` reads from this folder by default. Point it at
`data/sample/` instead if you want to iterate fast before loading the full set.
