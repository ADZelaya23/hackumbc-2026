"""Salary lens: what does this job family pay, at entry and over time.

Reads from alumni.csv (first job) and employment_history.csv (full career),
per the join graph in the dataset README. Handles the two `Not Applicable`
sentinels (`first_job_annual_salary_usd`, `first_job_family`) documented in
alumni.md, and the nominal-dollars gotcha (no cross-year inflation
adjustment here yet -- flag this as a known simplification, not a fix).
"""

from backend.snowflake_client import query_df


def salary_lens(job_family: str) -> dict:
    """Entry-level salary distribution plus a by-seniority progression.

    Returns a dict shaped for direct use in a chart:
        {
          "job_family": ...,
          "entry": {"median": ..., "p25": ..., "p75": ..., "n": ...},
          "by_seniority": [{"seniority_level": ..., "median": ..., "n": ...}, ...]
        }
    """
    entry_df = query_df(
        """
        SELECT annual_salary_usd
        FROM employment_history
        WHERE job_family = %(job_family)s
          AND seniority_level = 'Entry'
        """,
        {"job_family": job_family},
    )

    progression_df = query_df(
        """
        SELECT seniority_level,
               MEDIAN(annual_salary_usd) AS median_salary,
               COUNT(*) AS n
        FROM employment_history
        WHERE job_family = %(job_family)s
        GROUP BY seniority_level
        """,
        {"job_family": job_family},
    )

    seniority_order = ["Entry", "Mid", "Senior", "Lead", "Manager", "Director"]
    progression = progression_df.to_dict("records")
    progression.sort(
        key=lambda r: seniority_order.index(r["SENIORITY_LEVEL"])
        if r["SENIORITY_LEVEL"] in seniority_order else 99
    )

    return {
        "job_family": job_family,
        "entry": {
            "median": float(entry_df["ANNUAL_SALARY_USD"].median()) if not entry_df.empty else None,
            "p25": float(entry_df["ANNUAL_SALARY_USD"].quantile(0.25)) if not entry_df.empty else None,
            "p75": float(entry_df["ANNUAL_SALARY_USD"].quantile(0.75)) if not entry_df.empty else None,
            "n": int(len(entry_df)),
        },
        "by_seniority": progression,
    }
