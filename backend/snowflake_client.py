"""Shared Snowflake connection helper.

Usage:
    from backend.snowflake_client import query_df, run_sql

    df = query_df("SELECT * FROM alumni LIMIT 5")
    rows = run_sql("SELECT COUNT(*) FROM alumni")
"""

from contextlib import contextmanager

import pandas as pd
import snowflake.connector

from backend.config import settings


@contextmanager
def get_connection():
    conn = snowflake.connector.connect(
        account=settings.snowflake_account,
        user=settings.snowflake_user,
        password=settings.snowflake_password,
        role=settings.snowflake_role,
        warehouse=settings.snowflake_warehouse,
        database=settings.snowflake_database,
        schema=settings.snowflake_schema,
    )
    try:
        yield conn
    finally:
        conn.close()


def query_df(sql: str, params: dict | None = None) -> pd.DataFrame:
    """Run a query and get a pandas DataFrame back. Use for dashboard analytics."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, params or {})
        columns = [c[0] for c in cur.description]
        return pd.DataFrame(cur.fetchall(), columns=columns)


def run_sql(sql: str, params: dict | None = None):
    """Run a query and get raw rows back. Use for scalar results (e.g. Cortex calls)."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, params or {})
        return cur.fetchall()
