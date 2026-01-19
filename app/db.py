from __future__ import annotations

import os
import psycopg2
import psycopg2.extras


def get_conn():
    """"Return a new DB connection. DATABASE_URL must be set in DigitalOcean App Platform.""""
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL is not set")

    # DO typically provides sslmode=require already; we keep it safe if not present.
    if "sslmode=" not in dsn:
        if "?" in dsn:
            dsn = dsn + "&sslmode=require"
        else:
            dsn = dsn + "?sslmode=require"

    return psycopg2.connect(dsn)


def init_db() -> None:
    """"Create tables if they do not exist. Safe to call multiple times.""""
    conn = get_conn()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    \"""
                    CREATE TABLE IF NOT EXISTS refunds (
                        refund_id TEXT PRIMARY KEY,
                        merchant_id TEXT NOT NULL,
                        order_id TEXT NOT NULL,
                        customer_id TEXT NOT NULL,
                        amount TEXT NOT NULL,
                        reason TEXT NULL,
                        status TEXT NOT NULL,
                        idempotency_key TEXT NULL,
                        settlement_reference TEXT NULL,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    );
                    \"""
                )

                # Hard idempotency at merchant boundary
                cur.execute(
                    \"""
                    CREATE UNIQUE INDEX IF NOT EXISTS ux_refunds_merchant_idem
                    ON refunds (merchant_id, idempotency_key)
                    WHERE idempotency_key IS NOT NULL;
                    \"""
                )

                cur.execute(
                    \"""
                    CREATE TABLE IF NOT EXISTS refund_events (
                        event_id BIGSERIAL PRIMARY KEY,
                        refund_id TEXT NOT NULL REFERENCES refunds(refund_id) ON DELETE CASCADE,
                        event_type TEXT NOT NULL,
                        event_json JSONB NULL,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    );
                    \"""
                )

                cur.execute(
                    \"""
                    CREATE INDEX IF NOT EXISTS ix_refund_events_refund_id
                    ON refund_events(refund_id);
                    \"""
                )
    finally:
        conn.close()
