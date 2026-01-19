from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional, List

from .db import get_conn
from .models import RefundRecord, RefundStatus


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


class RefundStore:
    def create_refund(
        self,
        merchant_id: str,
        order_id: str,
        customer_id: str,
        amount: str,
        reason: Optional[str],
        idempotency_key: Optional[str],
    ) -> RefundRecord:
        """"Create refund record. If idempotency hits, return existing row.""""
        conn = get_conn()
        try:
            with conn:
                with conn.cursor() as cur:
                    # If idempotency key exists, try fetch first (fast path)
                    if idempotency_key:
                        cur.execute(
                            \"""
                            SELECT refund_id, status, merchant_id, order_id, customer_id, amount, reason,
                                   idempotency_key, settlement_reference, created_at, updated_at
                            FROM refunds
                            WHERE merchant_id = %s AND idempotency_key = %s
                            \"""
                            ,
                            (merchant_id, idempotency_key),
                        )
                        row = cur.fetchone()
                        if row:
                            return self._row_to_record(row)

                    refund_id = str(uuid.uuid4())
                    cur.execute(
                        \"""
                        INSERT INTO refunds (
                            refund_id, merchant_id, order_id, customer_id, amount, reason, status, idempotency_key
                        )
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                        RETURNING refund_id, status, merchant_id, order_id, customer_id, amount, reason,
                                  idempotency_key, settlement_reference, created_at, updated_at
                        \"""
                        ,
                        (
                            refund_id,
                            merchant_id,
                            order_id,
                            customer_id,
                            amount,
                            reason,
                            RefundStatus.CREATED.value,
                            idempotency_key,
                        ),
                    )
                    row = cur.fetchone()

                    # Event log
                    self.add_settlement_event(
                        refund_id,
                        "CREATED",
                        {
                            "merchant_id": merchant_id,
                            "order_id": order_id,
                            "customer_id": customer_id,
                            "amount": amount,
                            "idempotency_key": idempotency_key,
                        },
                        _conn=conn,
                    )

                    return self._row_to_record(row)
        finally:
            conn.close()

    def get_refund(self, refund_id: str) -> Optional[RefundRecord]:
        conn = get_conn()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        \"""
                        SELECT refund_id, status, merchant_id, order_id, customer_id, amount, reason,
                               idempotency_key, settlement_reference, created_at, updated_at
                        FROM refunds
                        WHERE refund_id = %s
                        \"""
                        ,
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
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        \"""
                        SELECT refund_id, status, merchant_id, order_id, customer_id, amount, reason,
                               idempotency_key, settlement_reference, created_at, updated_at
                        FROM refunds
                        WHERE status IN (%s, %s)
                        ORDER BY created_at ASC
                        LIMIT %s
                        \"""
                        ,
                        (RefundStatus.CREATED.value, RefundStatus.PENDING_SETTLEMENT.value, limit),
                    )
                    rows = cur.fetchall() or []
                    return [self._row_to_record(r) for r in rows]
        finally:
            conn.close()

    def mark_pending_settlement(self, refund_id: str, settlement_reference: Optional[str]) -> None:
        conn = get_conn()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        \"""
                        UPDATE refunds
                        SET status = %s,
                            settlement_reference = COALESCE(%s, settlement_reference),
                            updated_at = NOW()
                        WHERE refund_id = %s
                        \"""
                        ,
                        (RefundStatus.PENDING_SETTLEMENT.value, settlement_reference, refund_id),
                    )
        finally:
            conn.close()

    def mark_settled(self, refund_id: str, settlement_reference: Optional[str]) -> None:
        conn = get_conn()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        \"""
                        UPDATE refunds
                        SET status = %s,
                            settlement_reference = COALESCE(%s, settlement_reference),
                            updated_at = NOW()
                        WHERE refund_id = %s
                        \"""
                        ,
                        (RefundStatus.SETTLED.value, settlement_reference, refund_id),
                    )
        finally:
            conn.close()

    def mark_failed(self, refund_id: str, settlement_reference: Optional[str], reason: str) -> None:
        conn = get_conn()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        \"""
                        UPDATE refunds
                        SET status = %s,
                            settlement_reference = COALESCE(%s, settlement_reference),
                            updated_at = NOW()
                        WHERE refund_id = %s
                        \"""
                        ,
                        (RefundStatus.FAILED.value, settlement_reference, refund_id),
                    )
                    self.add_settlement_event(
                        refund_id,
                        "FAILED",
                        {"reason": reason},
                        _conn=conn,
                    )
        finally:
            conn.close()

    def add_settlement_event(self, refund_id: str, event_type: str, event_json: Optional[Dict[str, Any]], _conn=None) -> None:
        """"Append-only event log for auditability (use existing conn inside tx if provided).""""
        if _conn is None:
            conn = get_conn()
            close = True
        else:
            conn = _conn
            close = False

        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        \"""
                        INSERT INTO refund_events (refund_id, event_type, event_json)
                        VALUES (%s,%s,%s)
                        \"""
                        ,
                        (refund_id, event_type, json.dumps(event_json) if event_json is not None else None),
                    )
        finally:
            if close:
                conn.close()

    def _row_to_record(self, row) -> RefundRecord:
        refund_id, status, merchant_id, order_id, customer_id, amount, reason, idem, settlement_ref, created_at, updated_at = row

        # created_at/updated_at can be datetime or string depending on driver settings
        if hasattr(created_at, "isoformat"):
            created = created_at.isoformat()
        else:
            created = str(created_at)

        if hasattr(updated_at, "isoformat"):
            updated = updated_at.isoformat()
        else:
            updated = str(updated_at)

        return RefundRecord(
            refund_id=str(refund_id),
            status=RefundStatus(status),
            merchant_id=str(merchant_id),
            order_id=str(order_id),
            customer_id=str(customer_id),
            amount=str(amount),
            reason=reason if reason is None else str(reason),
            idempotency_key=idem if idem is None else str(idem),
            settlement_reference=settlement_ref if settlement_ref is None else str(settlement_ref),
            created_at=created,
            updated_at=updated,
        )


STORE = RefundStore()
