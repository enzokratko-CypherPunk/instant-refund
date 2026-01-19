from __future__ import annotations

import uuid
import json
from datetime import datetime
from typing import Optional, List

from .db import get_conn
from .models import RefundStatus


class Store:
    """
    Authoritative Postgres-backed ledger for refunds.
    """

    def create_refund(
        self,
        merchant_id: str,
        order_id: str,
        customer_id: str,
        amount: str,
        reason: Optional[str],
        idempotency_key: Optional[str],
    ):
        """
        Create refund record. If idempotency hits, return existing row.
        """
        conn = get_conn()
        cur = conn.cursor()

        if idempotency_key:
            cur.execute(
                """
                SELECT * FROM refunds
                WHERE merchant_id = %s AND idempotency_key = %s
                """,
                (merchant_id, idempotency_key),
            )
            row = cur.fetchone()
            if row:
                return row

        refund_id = str(uuid.uuid4())
        now = datetime.utcnow()

        cur.execute(
            """
            INSERT INTO refunds (
                refund_id,
                merchant_id,
                order_id,
                customer_id,
                amount,
                status,
                created_at,
                idempotency_key
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING *
            """,
            (
                refund_id,
                merchant_id,
                order_id,
                customer_id,
                amount,
                RefundStatus.CREATED.value,
                now,
                idempotency_key,
            ),
        )

        row = cur.fetchone()
        conn.commit()
        return row

    def get_refund(self, refund_id: str):
        """
        Fetch refund by ID.
        """
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM refunds WHERE refund_id = %s", (refund_id,))
        return cur.fetchone()

    def list_pending_for_settlement(self, limit: int = 50):
        """
        List refunds awaiting settlement.
        """
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM refunds
            WHERE status = %s
            ORDER BY created_at ASC
            LIMIT %s
            """,
            (RefundStatus.CREATED.value, limit),
        )
        return cur.fetchall()

    def mark_pending_settlement(self, refund_id: str, settlement_reference: Optional[str]):
        """
        Transition refund to pending settlement.
        """
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE refunds
            SET status = %s,
                settlement_reference = %s,
                updated_at = %s
            WHERE refund_id = %s
            """,
            (
                RefundStatus.PENDING_SETTLEMENT.value,
                settlement_reference,
                datetime.utcnow(),
                refund_id,
            ),
        )
        conn.commit()

    def add_settlement_event(self, refund_id: str, event_type: str, payload: dict):
        """
        Append immutable settlement event.
        """
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO settlement_events (
                refund_id,
                event_type,
                payload,
                created_at
            )
            VALUES (%s,%s,%s,%s)
            """,
            (
                refund_id,
                event_type,
                json.dumps(payload),
                datetime.utcnow(),
            ),
        )
        conn.commit()


STORE = Store()
