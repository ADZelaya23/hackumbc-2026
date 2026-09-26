"""Upload the raw CSVs to a DigitalOcean Spaces bucket.

    python ingest/upload_to_spaces.py

This is optional -- it's here for the "data hosted on DigitalOcean" piece of
the architecture. Spaces is S3-compatible, so this just uses boto3 pointed
at the Spaces endpoint. Once uploaded, Snowflake can read from the bucket
via an external stage (see the commented block at the bottom of
load_to_snowflake.py) instead of loading straight from a local file.

Requires DO_SPACES_KEY / DO_SPACES_SECRET / DO_SPACES_REGION /
DO_SPACES_BUCKET / DO_SPACES_ENDPOINT in .env.
"""

import os
from pathlib import Path

import boto3
from dotenv import load_dotenv

load_dotenv()

FILES = [
    "students_current.csv",
    "alumni.csv",
    "transcripts.csv",
    "employment_history.csv",
    "student_experience.csv",
    "course_catalog.csv",
]

DATA_DIR = Path(__file__).parent.parent / "data"


def get_client():
    return boto3.client(
        "s3",
        region_name=os.environ["DO_SPACES_REGION"],
        endpoint_url=os.environ["DO_SPACES_ENDPOINT"],
        aws_access_key_id=os.environ["DO_SPACES_KEY"],
        aws_secret_access_key=os.environ["DO_SPACES_SECRET"],
    )


def main():
    client = get_client()
    bucket = os.environ["DO_SPACES_BUCKET"]

    for filename in FILES:
        local_path = DATA_DIR / filename
        if not local_path.exists():
            print(f"  skip {filename}: not found in data/")
            continue
        client.upload_file(str(local_path), bucket, f"raw/{filename}")
        print(f"  uploaded {filename} -> s3://{bucket}/raw/{filename}")

    print("Done. Set the bucket's access as needed (private by default).")


if __name__ == "__main__":
    main()
