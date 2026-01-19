from __future__ import annotations

import os
import psycopg2


def get_conn():
    """
    Return a new DB connection.
    DATABASE_URL must be set in DigitalOcean App Platform.
    """
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL not set")

    return psycopg2.connect(dsn)


def ensure_schema():
    """
    Create required tables if they do not already exist.
    Safe to call multiple times.
    """
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS refunds (
            refund_id TEXT PRIMARY KEY,
            merchant_id TEXT NOT NULL,
            order_id TEXT NOT NULL,
            customer_id TEXT NOT NULL,
            amount TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP,
            idempotency_key TEXT,
            settlement_reference TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS settlement_events (
            id SERIAL PRIMARY KEY,
            refund_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            payload JSONB NOT NULL,
            created_at TIMESTAMP NOT NULL
        )
        """
    )

    conn.commit()
