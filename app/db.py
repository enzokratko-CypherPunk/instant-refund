from __future__ import annotations

import os
import psycopg2
import psycopg2.extras


def _database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set")
    return url


def get_conn():
    """
    Returns a new psycopg2 connection.
    Callers should open briefly and close promptly.
    """
    return psycopg2.connect(_database_url())


def init_db() -> None:
    """
    Idempotent schema initialization.
    Safe to call on startup.
    """
    ddl = [
        """
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
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_refunds_status_created_at
          ON refunds (status, created_at);
        """,
        """
        DO )
        BEGIN
          IF NOT EXISTS (
            SELECT 1
            FROM pg_indexes
            WHERE schemaname = 'public'
              AND indexname = 'ux_refunds_merchant_idem_notnull'
          ) THEN
            CREATE UNIQUE INDEX ux_refunds_merchant_idem_notnull
              ON refunds (merchant_id, idempotency_key)
              WHERE idempotency_key IS NOT NULL;
          END IF;
        END );
        """,
        """
        CREATE TABLE IF NOT EXISTS settlement_events (
          event_id BIGSERIAL PRIMARY KEY,
          refund_id TEXT NOT NULL REFERENCES refunds(refund_id) ON DELETE CASCADE,
          event_type TEXT NOT NULL,
          detail JSONB NULL,
          created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_settlement_events_refund_id_created_at
          ON settlement_events (refund_id, created_at);
        """,
    ]

    conn = get_conn()
    try:
        conn.autocommit = True
        with conn.cursor() as cur:
            for stmt in ddl:
                cur.execute(stmt)
    finally:
        conn.close()