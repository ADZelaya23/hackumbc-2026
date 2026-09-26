"""Typical first job, and what alumni with a similar profile did next.

The "next role" logic mirrors examples/explore_python.py and
examples/explore_sql.sql from the dataset repo: sort each person's job
spells by start_date, pair each with the following one.
"""

from backend.db_client import query_df


def typical_first_jobs(major: str, track: str | None = None, limit: int = 5) -> list[dict]:
    """Most common first_job_title for alumni matching this major/track."""
    filters = ["major = %(major)s", "first_job_title != 'Not Applicable'"]
    params = {"major": major, "limit": limit}
    if track:
        filters.append("track = %(track)s")
        params["track"] = track

    df = query_df(
        f"""
        SELECT first_job_title, first_job_family, COUNT(*) AS n
        FROM alumni
        WHERE {' AND '.join(filters)}
        GROUP BY first_job_title, first_job_family
        ORDER BY n DESC
        LIMIT %(limit)s
        """,
        params,
    )
    return df.to_dict("records")


def alumni_pathways(job_family: str, limit: int = 10) -> list[dict]:
    """Common role -> next-role transitions for alumni who started in this
    job family, computed with LEAD() the same way explore_sql.sql does it.
    """
    df = query_df(
        """
        WITH steps AS (
            SELECT campus_id, job_title, job_family, start_date,
                   LEAD(job_title) OVER (
                       PARTITION BY campus_id ORDER BY start_date
                   ) AS next_role
            FROM employment_history
        )
        SELECT job_title, next_role, COUNT(*) AS weight
        FROM steps
        WHERE job_family = %(job_family)s
          AND next_role IS NOT NULL
        GROUP BY job_title, next_role
        ORDER BY weight DESC
        LIMIT %(limit)s
        """,
        {"job_family": job_family, "limit": limit},
    )
    return df.to_dict("records")
