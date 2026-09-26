"""Which student_experience activities correlate with landing in a given
job family -- joins alumni.csv to student_experience.csv on campus_id.
"""

from backend.db_client import query_df


def correlated_activities(job_family: str, limit: int = 8) -> list[dict]:
    df = query_df(
        """
        SELECT se.experience_type, COUNT(*) AS n
        FROM student_experience se
        JOIN alumni a ON a.campus_id = se.campus_id
        WHERE a.first_job_family = %(job_family)s
        GROUP BY se.experience_type
        ORDER BY n DESC
        LIMIT %(limit)s
        """,
        {"job_family": job_family, "limit": limit},
    )
    return df.to_dict("records")
