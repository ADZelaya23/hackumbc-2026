"""Load the six dataset CSVs into DigitalOcean Managed PostgreSQL.

    python ingest/load_to_postgres.py
    python ingest/load_to_postgres.py --source data/sample   # fast iteration

Runs ingest/schema.sql to (re)create the tables, then uses Postgres's native
COPY command to bulk-load each CSV. Requires .env to be filled in with
DATABASE_URL (see .env.example) -- that's the full connection string
DigitalOcean gives you in the control panel for your Managed Database
cluster.
"""

import argparse
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

from backend.config import settings

load_dotenv()

TABLES = [
    "students_current",
    "alumni",
    "transcripts",
    "employment_history",
    "student_experience",
    "course_catalog",
]

HERE = Path(__file__).parent


def get_connection():
    return psycopg2.connect(settings.database_url)


def run_schema(cur):
    schema_sql = (HERE / "schema.sql").read_text()
    cur.execute(schema_sql)


def load_table(cur, table_name, source_dir):
    csv_path = source_dir / f"{table_name}.csv"
    if not csv_path.exists():
        print(f"  skip {table_name}: {csv_path} not found")
        return

    cur.execute(f"TRUNCATE TABLE {table_name}")
    with open(csv_path, "r", encoding="utf-8") as f:
        cur.copy_expert(
            f"""
            COPY {table_name} FROM STDIN WITH (
                FORMAT csv,
                HEADER true,
                NULL ''
            )
            """,
            f,
        )
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cur.fetchone()[0]
    print(f"  loaded {table_name}: {count:,} rows")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="data", help="folder containing the CSVs")
    args = parser.parse_args()
    source_dir = Path(args.source)

    conn = get_connection()
    conn.autocommit = False
    cur = conn.cursor()
    try:
        print("Creating schema...")
        run_schema(cur)
        conn.commit()

        print(f"Loading tables from {source_dir}/ ...")
        for table in TABLES:
            load_table(cur, table, source_dir)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

    print("Done.")


if __name__ == "__main__":
    main()
