"""Load the six dataset CSVs into Snowflake.

    python ingest/load_to_snowflake.py
    python ingest/load_to_snowflake.py --source data/sample   # fast iteration

Runs ingest/schema.sql to (re)create the tables, then PUTs each CSV to an
internal stage and COPY INTOs the matching table. Requires .env to be filled
in (see .env.example).

This is the "local file -> Snowflake" path. If you've uploaded the CSVs to
DigitalOcean Spaces instead (see upload_to_spaces.py), point COPY INTO at an
external stage backed by that bucket instead -- see the commented-out
alternative at the bottom of this file.
"""

import argparse
import os
from pathlib import Path

import snowflake.connector
from dotenv import load_dotenv

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
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        role=os.environ.get("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
        warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        database=os.environ.get("SNOWFLAKE_DATABASE", "CAREER_NAVIGATOR"),
        schema=os.environ.get("SNOWFLAKE_SCHEMA", "PUBLIC"),
    )


def run_schema(cur):
    schema_sql = (HERE / "schema.sql").read_text()
    for statement in schema_sql.split(";"):
        statement = statement.strip()
        if statement:
            cur.execute(statement)


def load_table(cur, table_name, source_dir):
    csv_path = source_dir / f"{table_name}.csv"
    if not csv_path.exists():
        print(f"  skip {table_name}: {csv_path} not found")
        return

    stage = f"@%{table_name}"
    cur.execute(f"PUT file://{csv_path.resolve()} {stage} AUTO_COMPRESS=TRUE OVERWRITE=TRUE")
    cur.execute(f"""
        COPY INTO {table_name}
        FROM {stage}
        FILE_FORMAT = (
            TYPE = CSV
            SKIP_HEADER = 1
            FIELD_OPTIONALLY_ENCLOSED_BY = '"'
            NULL_IF = ('')
            EMPTY_FIELD_AS_NULL = FALSE
        )
        ON_ERROR = 'ABORT_STATEMENT'
    """)
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cur.fetchone()[0]
    print(f"  loaded {table_name}: {count:,} rows")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="data", help="folder containing the CSVs")
    args = parser.parse_args()
    source_dir = Path(args.source)

    conn = get_connection()
    cur = conn.cursor()
    try:
        print("Creating schema...")
        run_schema(cur)

        print(f"Loading tables from {source_dir}/ ...")
        for table in TABLES:
            load_table(cur, table, source_dir)
    finally:
        cur.close()
        conn.close()

    print("Done.")


if __name__ == "__main__":
    main()


# -----------------------------------------------------------------------
# Alternative: load from DigitalOcean Spaces instead of a local file, once
# upload_to_spaces.py has put the CSVs there.
#
#   CREATE OR REPLACE STAGE do_spaces_stage
#     URL = 's3compat://<bucket>'
#     CREDENTIALS = (AWS_KEY_ID = '<DO_SPACES_KEY>' AWS_SECRET_KEY = '<DO_SPACES_SECRET>')
#     -- Snowflake's S3-compatible stage support varies by account/region;
#     -- confirm current syntax in Snowflake's stage docs before relying on
#     -- this path for the full dataset.
#
#   COPY INTO alumni FROM @do_spaces_stage/alumni.csv FILE_FORMAT = (...);
# -----------------------------------------------------------------------
