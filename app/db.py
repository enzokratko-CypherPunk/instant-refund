import os
import time
import psycopg
from psycopg.rows import dict_row

def get_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set")
    return url

def connect():
    return psycopg.connect(get_database_url(), row_factory=dict_row)

def init_schema_if_possible():
    """
    Attempt to initialize schema.
    Safe to call multiple times.
    Does NOT crash the process if DB is unavailable.
    """
    try:
        ddl = """
        CREATE TABLE IF NOT EXISTS refunds (
            refund_id TEXT PRIMARY KEY,
            created_at TIMESTAMPTZ NOT NULL,
            original_transaction_id TEXT NOT NULL,
            amount NUMERIC NOT NULL,
            currency TEXT NOT NULL,
            status TEXT NOT NULL,
            settlement_state TEXT NOT NULL,
            txid TEXT NULL,
            last_error TEXT NULL
        );

        CREATE TABLE IF NOT EXISTS settlement_jobs (
            job_id BIGSERIAL PRIMARY KEY,
            refund_id TEXT NOT NULL REFERENCES refunds(refund_id) ON DELETE CASCADE,
            state TEXT NOT NULL,
            attempts INT NOT NULL DEFAULT 0,
            next_run_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            locked_at TIMESTAMPTZ NULL,
            last_error TEXT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );

        CREATE INDEX IF NOT EXISTS idx_settlement_jobs_run
          ON settlement_jobs (state, next_run_at);

        CREATE INDEX IF NOT EXISTS idx_settlement_jobs_refund
          ON settlement_jobs (refund_id);
        """
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute(ddl)
            conn.commit()
    except Exception:
        # Swallow errors here; API/worker will handle DB availability later
        pass

def utc_now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
