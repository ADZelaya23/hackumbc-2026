-- Schema for the six HackUMBC 2026 dataset files, targeting DigitalOcean
-- Managed PostgreSQL.
--
-- Note: several "numeric" columns are declared VARCHAR/TEXT because the
-- source data mixes real numbers with the literal string "Not Applicable"
-- in the same column (e.g. first_job_annual_salary_usd). Cast in queries
-- after filtering out the sentinel -- see backend/queries/ for examples.

CREATE TABLE IF NOT EXISTS students_current (
    campus_id                     TEXT,
    entry_term                    TEXT,
    entry_type                    TEXT,
    major                         TEXT,
    track                         TEXT,
    second_major                  TEXT,
    minor                         TEXT,
    class_level                   TEXT,
    residency                     TEXT,
    enrollment_intensity          TEXT,
    is_first_generation           BOOLEAN,
    work_hours_per_week           INTEGER,
    credits_earned                INTEGER,
    credits_required              INTEGER,
    cumulative_gpa                TEXT,  -- 'Not Applicable' for first-termers
    major_gpa                     TEXT,
    academic_standing             TEXT,
    expected_graduation_term      TEXT,
    internship_count              INTEGER,
    credential_count              INTEGER,
    engagement_activity_count     INTEGER,
    tuition_paid_to_date_usd      INTEGER
);

CREATE TABLE IF NOT EXISTS alumni (
    campus_id                          TEXT,
    major                               TEXT,
    degree_level                        TEXT,
    track                                TEXT,
    graduation_term                     TEXT,
    graduation_year                     INTEGER,
    entry_type                          TEXT,
    time_to_degree_years                REAL,
    total_credits_earned                INTEGER,
    final_gpa                           REAL,
    major_gpa                           REAL,
    residency                           TEXT,
    holds_prior_umbc_bachelors          BOOLEAN,
    work_hours_per_week_while_enrolled  INTEGER,
    internship_count                    INTEGER,
    credential_count                    INTEGER,
    engagement_activity_count           INTEGER,
    net_cost_usd                        INTEGER,
    total_loans_usd                     INTEGER,
    first_destination                   TEXT,
    months_to_first_job                 TEXT,  -- 'Not Applicable' sentinel
    first_job_title                     TEXT,
    first_job_family                    TEXT,
    first_employer                      TEXT,
    first_employer_industry             TEXT,
    first_job_region                    TEXT,
    first_job_annual_salary_usd         TEXT,  -- 'Not Applicable' sentinel
    first_job_is_remote                 TEXT,  -- TRUE/FALSE/'Not Applicable'
    first_job_found_via                 TEXT
);

CREATE TABLE IF NOT EXISTS transcripts (
    campus_id             TEXT,
    term                  TEXT,
    course_id             TEXT,
    course_title          TEXT,
    subject               TEXT,
    credits_attempted     INTEGER,
    credits_earned        INTEGER,
    grade                 TEXT,
    grade_points          TEXT,  -- 'Not Applicable' for W/IP
    is_repeat             BOOLEAN,
    requirement_category  TEXT
);

CREATE TABLE IF NOT EXISTS employment_history (
    job_id               TEXT,
    campus_id            TEXT,
    employer             TEXT,
    employer_industry    TEXT,
    employer_size        TEXT,
    job_title            TEXT,
    job_family           TEXT,
    seniority_level      TEXT,
    region               TEXT,
    cost_of_living_index INTEGER,
    is_remote            BOOLEAN,
    start_date           DATE,
    end_date             DATE,      -- NULL iff is_current
    is_current           BOOLEAN,
    tenure_months        INTEGER,
    annual_salary_usd    INTEGER,
    change_type          TEXT,
    requires_clearance   BOOLEAN,
    role_skill_tags      TEXT    -- pipe-delimited
);

CREATE TABLE IF NOT EXISTS student_experience (
    record_id         TEXT,
    campus_id         TEXT,
    experience_type   TEXT,
    experience_name   TEXT,
    organization      TEXT,
    industry          TEXT,
    term              TEXT,
    duration_terms    INTEGER,
    hours_per_week    TEXT,  -- 'Not Applicable' for certifications
    is_paid           TEXT,  -- TRUE/FALSE/'Not Applicable'
    role_level        TEXT,
    outcome           TEXT
);

CREATE TABLE IF NOT EXISTS course_catalog (
    course_id              TEXT,
    subject                TEXT,
    catalog_number         INTEGER,
    course_title           TEXT,
    credits                INTEGER,
    course_level           TEXT,
    course_type            TEXT,
    required_for_majors    TEXT,  -- pipe-delimited
    prerequisite_ids       TEXT,  -- pipe-delimited, may contain " or "
    skill_tags             TEXT,  -- pipe-delimited
    difficulty_index       REAL,
    typical_terms_offered  TEXT   -- pipe-delimited
);
