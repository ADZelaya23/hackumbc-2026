-- Schema for the six HackUMBC 2026 dataset files.
-- Run once (load_to_snowflake.py executes this automatically).
--
-- Note: several "numeric" columns are declared VARCHAR because the source
-- data mixes real numbers with the literal string "Not Applicable" in the
-- same column (e.g. first_job_annual_salary_usd). Cast in queries after
-- filtering out the sentinel -- see backend/queries/ for examples.

CREATE DATABASE IF NOT EXISTS CAREER_NAVIGATOR;
USE DATABASE CAREER_NAVIGATOR;
CREATE SCHEMA IF NOT EXISTS PUBLIC;
USE SCHEMA PUBLIC;

CREATE OR REPLACE TABLE students_current (
    campus_id                     VARCHAR,
    entry_term                    VARCHAR,
    entry_type                    VARCHAR,
    major                         VARCHAR,
    track                         VARCHAR,
    second_major                  VARCHAR,
    minor                         VARCHAR,
    class_level                   VARCHAR,
    residency                     VARCHAR,
    enrollment_intensity          VARCHAR,
    is_first_generation           BOOLEAN,
    work_hours_per_week           INTEGER,
    credits_earned                INTEGER,
    credits_required              INTEGER,
    cumulative_gpa                VARCHAR,  -- 'Not Applicable' for first-termers
    major_gpa                     VARCHAR,
    academic_standing             VARCHAR,
    expected_graduation_term      VARCHAR,
    internship_count              INTEGER,
    credential_count              INTEGER,
    engagement_activity_count     INTEGER,
    tuition_paid_to_date_usd      INTEGER
);

CREATE OR REPLACE TABLE alumni (
    campus_id                          VARCHAR,
    major                               VARCHAR,
    degree_level                        VARCHAR,
    track                               VARCHAR,
    graduation_term                     VARCHAR,
    graduation_year                     INTEGER,
    entry_type                          VARCHAR,
    time_to_degree_years                FLOAT,
    total_credits_earned                INTEGER,
    final_gpa                           FLOAT,
    major_gpa                           FLOAT,
    residency                           VARCHAR,
    holds_prior_umbc_bachelors          BOOLEAN,
    work_hours_per_week_while_enrolled  INTEGER,
    internship_count                    INTEGER,
    credential_count                    INTEGER,
    engagement_activity_count           INTEGER,
    net_cost_usd                        INTEGER,
    total_loans_usd                     INTEGER,
    first_destination                   VARCHAR,
    months_to_first_job                 VARCHAR,  -- 'Not Applicable' sentinel
    first_job_title                     VARCHAR,
    first_job_family                    VARCHAR,
    first_employer                      VARCHAR,
    first_employer_industry             VARCHAR,
    first_job_region                    VARCHAR,
    first_job_annual_salary_usd         VARCHAR,  -- 'Not Applicable' sentinel
    first_job_is_remote                 VARCHAR,  -- TRUE/FALSE/'Not Applicable'
    first_job_found_via                 VARCHAR
);

CREATE OR REPLACE TABLE transcripts (
    campus_id             VARCHAR,
    term                  VARCHAR,
    course_id             VARCHAR,
    course_title          VARCHAR,
    subject               VARCHAR,
    credits_attempted     INTEGER,
    credits_earned        INTEGER,
    grade                 VARCHAR,
    grade_points          VARCHAR,  -- 'Not Applicable' for W/IP
    is_repeat             BOOLEAN,
    requirement_category  VARCHAR
);

CREATE OR REPLACE TABLE employment_history (
    job_id               VARCHAR,
    campus_id            VARCHAR,
    employer             VARCHAR,
    employer_industry    VARCHAR,
    employer_size        VARCHAR,
    job_title            VARCHAR,
    job_family           VARCHAR,
    seniority_level      VARCHAR,
    region               VARCHAR,
    cost_of_living_index INTEGER,
    is_remote            BOOLEAN,
    start_date           DATE,
    end_date             DATE,      -- NULL iff is_current
    is_current           BOOLEAN,
    tenure_months        INTEGER,
    annual_salary_usd    INTEGER,
    change_type          VARCHAR,
    requires_clearance   BOOLEAN,
    role_skill_tags      VARCHAR    -- pipe-delimited
);

CREATE OR REPLACE TABLE student_experience (
    record_id         VARCHAR,
    campus_id         VARCHAR,
    experience_type   VARCHAR,
    experience_name   VARCHAR,
    organization      VARCHAR,
    industry          VARCHAR,
    term              VARCHAR,
    duration_terms    INTEGER,
    hours_per_week    VARCHAR,  -- 'Not Applicable' for certifications
    is_paid           VARCHAR,  -- TRUE/FALSE/'Not Applicable'
    role_level        VARCHAR,
    outcome           VARCHAR
);

CREATE OR REPLACE TABLE course_catalog (
    course_id              VARCHAR,
    subject                VARCHAR,
    catalog_number         INTEGER,
    course_title           VARCHAR,
    credits                INTEGER,
    course_level           VARCHAR,
    course_type            VARCHAR,
    required_for_majors    VARCHAR,  -- pipe-delimited
    prerequisite_ids       VARCHAR,  -- pipe-delimited, may contain " or "
    skill_tags             VARCHAR,  -- pipe-delimited
    difficulty_index       FLOAT,
    typical_terms_offered  VARCHAR   -- pipe-delimited
);
