"""Skill-gap teaser: what a job family asks for vs. what the curriculum
teaches. skill_tags (course_catalog) and role_skill_tags (employment_history)
share one vocabulary by design -- see the dataset README -- so this is a
plain set comparison, no mapping table needed.

Note: pipe-delimited list columns are easiest to explode in pandas; Snowflake
SQL can do it too (SPLIT_TO_TABLE / FLATTEN) but for a hackathon timeline,
pulling the two relevant columns and exploding in pandas is simpler and the
tables involved are tiny (72 courses, thousands of job rows).
"""

from backend.snowflake_client import query_df


def top_skills_for_job_family(job_family: str, seniority: str | None = None, top_n: int = 10) -> list[str]:
    filters = ["job_family = %(job_family)s"]
    params = {"job_family": job_family}
    if seniority:
        filters.append("seniority_level = %(seniority)s")
        params["seniority"] = seniority

    df = query_df(
        f"SELECT role_skill_tags FROM employment_history WHERE {' AND '.join(filters)}",
        params,
    )
    if df.empty:
        return []

    exploded = df["ROLE_SKILL_TAGS"].str.split("|").explode()
    return exploded.value_counts().head(top_n).index.tolist()


def courses_teaching(skills: list[str]) -> list[dict]:
    """Which catalog courses teach at least one of the given skills, with
    prerequisites included so the caller can filter to what's actually
    takeable next.
    """
    df = query_df("SELECT course_id, course_title, skill_tags, prerequisite_ids FROM course_catalog")
    if df.empty:
        return []

    skill_set = set(skills)
    df["matched_skills"] = df["SKILL_TAGS"].str.split("|").apply(
        lambda tags: sorted(skill_set.intersection(tags))
    )
    matches = df[df["matched_skills"].str.len() > 0]
    return matches[["COURSE_ID", "COURSE_TITLE", "matched_skills", "PREREQUISITE_IDS"]].to_dict("records")
