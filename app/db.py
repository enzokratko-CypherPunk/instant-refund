from __future__ import annotations

import os
from urllib.parse import urlparse
from typing import Optional

import psycopg2
import psycopg2.extras


def _database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set (required for Postgres persistence).")
    return url


def get_conn():
    """
    Returns a new psycopg2 connection. Callers should use context managers and close quickly.
    """
    url = _database_url()
    # psycopg2 accepts DATABASE_URL directly (postgres:// or postgresql://)
    return psycopg2.connect(url)


def init_db() -> None:
    """
    Idempotent schema init. Safe to call on startup.
    """
    ddl = [
        # Core refunds ledger. One row = one refund attempt.
        # Idempotency: unique per (merchant_id, idempotency_key) when key is provided.
        \"\"\"
        CREATE TABLE IF NOT EXISTS refunds (
          refund_id TEXT PRIMARY KEY,
          merchant_id TEXT NOT NULL,
          order_id TEXT NOT NULL,
          customer_id TEXT NOT NULL,
          amount TEXT NOT NULL,
          reason TEXT NULL,
          idempotency_key TEXT NULL,
          status TEXT NOT NULL,
          settlement_reference TEXT NULL,
          created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        \"\"\",
        # Supports querying pending refunds quickly for settlement engine.
        \"\"\"
        CREATE INDEX IF NOT EXISTS idx_refunds_status_created_at
          ON refunds (status, created_at);
        \"\"\",
        # Enforce idempotency only when idempotency_key is present.
        \"\"\"
        DO 
        BEGIN
          IF NOT EXISTS (
            SELECT 1
            FROM pg_indexes
            WHERE schemaname = 'public' AND indexname = 'ux_refunds_merchant_idem_notnull'
          ) THEN
            CREATE UNIQUE INDEX ux_refunds_merchant_idem_notnull
              ON refunds (merchant_id, idempotency_key)
              WHERE idempotency_key IS NOT NULL;
          END IF;
        END ;
        \"\"\",
        # Audit trail for settlement attempts (Task #3 will populate real txids + statuses).
        \"\"\"
        CREATE TABLE IF NOT EXISTS settlement_events (
          event_id BIGSERIAL PRIMARY KEY,
          refund_id TEXT NOT NULL REFERENCES refunds(refund_id) ON DELETE CASCADE,
          event_type TEXT NOT NULL,
          detail JSONB NULL,
          created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        \"\"\",
        \"\"\"
        CREATE INDEX IF NOT EXISTS idx_settlement_events_refund_id_created_at
          ON settlement_events (refund_id, created_at);
        \"\"\",
    ]

    conn = get_conn()
    try:
        conn.autocommit = True
        with conn.cursor() as cur:
            for stmt in ddl:
                cur.execute(stmt)
    finally:
        conn.close()
