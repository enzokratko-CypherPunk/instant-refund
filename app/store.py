from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from typing import Optional, List

from .db import get_conn
from .models import RefundStatus


@dataclass(frozen=True)
class RefundRecord:
    refund_id: str
    merchant_id: str
    order_id: str
    customer_id: str
    amount: str
    reason: Optional[str]
    idempotency_key: Optional[str]
    status: RefundStatus
    settlement_reference: Optional[str]
    created_at: str
    updated_at: str


class PostgresStore:
    """
    Authoritative ledger store backed by Postgres.
    """

    def create_refund(
        self,
        merchant_id: str,
        order_id: str,
        customer_id: str,
        amount: str,
        reason: Optional[str],
        idempotency_key: Optional[str],
    ) -> RefundRecord:
        refund_id = str(uuid.uuid4())
        status = RefundStatus.CREATED

        conn = get_conn()
        try:
            with conn:
                with conn.cursor() as cur:
                    if idempotency_key:
                        cur.execute(
                            """
                            INSERT INTO refunds (
                              refund_id, merchant_id, order_id, customer_id,
                              amount, reason, idempotency_key, status
                            )
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                            ON CONFLICT ON CONSTRAINT ux_refunds_merchant_idem_notnull DO NOTHING
                            RETURNING refund_id;
                            """,
                            (
                                refund_id,
                                merchant_id,
                                order_id,
                                customer_id,
                                amount,
                                reason,
                                idempotency_key,
                                status.value,
                            ),
                        )
                        inserted = cur.fetchone()
                        if inserted is None:
                            cur.execute(
                                """
                                SELECT refund_id, merchant_id, order_id, customer_id,
                                       amount, reason, idempotency_key, status,
                                       settlement_reference, created_at, updated_at
                                  FROM refunds
                                 WHERE merchant_id = %s AND idempotency_key = %s
                                 LIMIT 1;
                                """,
                                (merchant_id, idempotency_key),
                            )
                            row = cur.fetchone()
                            if not row:
                                raise RuntimeError("Idempotency conflict but refund not found")
                            return self._row_to_record(row)
                    else:
                        cur.execute(
                            """
                            INSERT INTO refunds (
                              refund_id, merchant_id, order_id, customer_id,
                              amount, reason, idempotency_key, status
                            )
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                            RETURNING refund_id, merchant_id, order_id, customer_id,
                                      amount, reason, idempotency_key, status,
                                      settlement_reference, created_at, updated_at;
                            """,
                            (
                                refund_id,
                                merchant_id,
                                order_id,
                                customer_id,
                                amount,
                                reason,
                                None,
                                status.value,
                            ),
                        )
                        row = cur.fetchone()
                        return self._row_to_record(row)

                    cur.execute(
                        """
                        SELECT refund_id, merchant_id, order_id, customer_id,
                               amount, reason, idempotency_key, status,
                               settlement_reference, created_at, updated_at
                          FROM refunds
                         WHERE refund_id = %s
                         LIMIT 1;
                        """,
                        (refund_id,),
                    )
                    row = cur.fetchone()
                    if not row:
                        raise RuntimeError("Inserted refund not found")
                    return self._row_to_record(row)
        finally:
            conn.close()

    def get_refund(self, refund_id: str) -> Optional[RefundRecord]:
        conn = get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT refund_id, merchant_id, order_id, customer_id,
                           amount, reason, idempotency_key, status,
                           settlement_reference, created_at, updated_at
                      FROM refunds
                     WHERE refund_id = %s
                     LIMIT 1;
                    """,
                    (refund_id,),
                )
                row = cur.fetchone()
                if not row:
                    return None
                return self._row_to_record(row)
        finally:
            conn.close()

    def list_pending_for_settlement(self, limit: int = 50) -> List[RefundRecord]:
        conn = get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT refund_id, merchant_id, order_id, customer_id,
                           amount, reason, idempotency_key, status,
                           settlement_reference, created_at, updated_at
                      FROM refunds
                     WHERE status IN (%s, %s)
                     ORDER BY created_at ASC
                     LIMIT %s;
                    """,
                    (
                        RefundStatus.CREATED.value,
                        RefundStatus.PENDING_SETTLEMENT.value,
                        limit,
                    ),
                )
                rows = cur.fetchall() or []
                return [self._row_to_record(r) for r in rows]
        finally:
            conn.close()

    def mark_pending_settlement(
        self, refund_id: str, settlement_reference: Optional[str] = None
    ) -> None:
        conn = get_conn()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        UPDATE refunds
                           SET status = %s,
                               settlement_reference = COALESCE(%s, settlement_reference),
                               updated_at = NOW()
                         WHERE refund_id = %s;
                        """,
                        (
                            RefundStatus.PENDING_SETTLEMENT.value,
                            settlement_reference,
                            refund_id,
                        ),
                    )
        finally:
            conn.close()

    def add_settlement_event(
        self, refund_id: str, event_type: str, detail: Optional[dict] = None
    ) -> None:
        conn = get_conn()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO settlement_events (refund_id, event_type, detail)
                        VALUES (%s, %s, %s);
                        """,
                        (refund_id, event_type, json.dumps(detail) if detail else None),
                    )
        finally:
            conn.close()

    def _row_to_record(self, row) -> RefundRecord:
        status = RefundStatus(row[7])
        return RefundRecord(
            refund_id=row[0],
            merchant_id=row[1],
            order_id=row[2],
            customer_id=row[3],
            amount=row[4],
            reason=row[5],
            idempotency_key=row[6],
            status=status,
            settlement_reference=row[8],
            created_at=str(row[9]),
            updated_at=str(row[10]),
        )


STORE = PostgresStore()