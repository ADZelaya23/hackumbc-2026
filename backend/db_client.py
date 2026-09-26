"""Shared DigitalOcean Managed PostgreSQL connection helper.

Usage:
    from backend.db_client import query_df, run_sql

    df = query_df("SELECT * FROM alumni LIMIT 5")
    rows = run_sql("SELECT COUNT(*) FROM alumni")
"""

from contextlib import contextmanager

import pandas as pd
import psycopg2

from backend.config import settings


@contextmanager
def get_connection():
    conn = psycopg2.connect(settings.database_url)
    try:
        yield conn
    finally:
        conn.close()


def query_df(sql: str, params: dict | None = None) -> pd.DataFrame:
    """Run a query and get a pandas DataFrame back. Use for dashboard analytics."""
    with get_connection() as conn:
        return pd.read_sql(sql, conn, params=params)


def run_sql(sql: str, params: dict | None = None):
    """Run a query and get raw rows back. Use for scalar results."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, params or {})
        return cur.fetchall()
