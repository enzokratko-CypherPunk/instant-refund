from __future__ import annotations

import os
import time
import uuid
from typing import Dict, Any, Optional

import requests

from .db import (
    init_db,
    get_refund as db_get_refund,
    insert_refund,
    update_refund,
    list_pending_refunds,
    get_refund_id_for_key,
    set_idempotency_key,
)
from .providers.kaspa import KaspaSettlementProvider
from .providers.base import SettlementProvider


# ----- init DB on import -----
init_db()


class SettlementEngine:
    def __init__(self) -> None:
        self.providers: Dict[str, SettlementProvider] = {
            "kaspa": KaspaSettlementProvider(),
        }

    def quote(self, rail: str, amount: int, currency: str) -> Dict[str, Any]:
        return self.providers[rail].quote(amount=amount, currency=currency)

    def settle(self, rail: str, refund_id: str, amount: int, currency: str) -> Dict[str, Any]:
        return self.providers[rail].settle(refund_id=refund_id, amount=amount, currency=currency)

    def status(self, rail: str, settlement_ref: str) -> Dict[str, Any]:
        return self.providers[rail].status(settlement_ref=settlement_ref)


_engine = SettlementEngine()


def _now() -> int:
    return int(time.time())


def _emit_webhook(event: str, data: dict) -> None:
    url = os.getenv("WEBHOOK_URL")
    if not url:
        return
    try:
        requests.post(url, json={"event": event, "data": data}, timeout=2)
    except Exception as e:
        print(f"[webhook error] {e}")


def create_refund(
    amount: int,
    currency: str = "USD",
    rail: str = "kaspa",
    idempotency_key: Optional[str] = None,
) -> Dict[str, Any]:

    # A2: idempotency across restarts
    if idempotency_key:
        existing_id = get_refund_id_for_key(idempotency_key)
        if existing_id:
            existing = db_get_refund(existing_id)
            if existing:
                return existing

    refund_id = uuid.uuid4().hex

    record: Dict[str, Any] = {
        "refund_id": refund_id,
        "amount": amount,
        "currency": currency,
        "rail": rail,
        "status": "created",
        "idempotency_key": idempotency_key,
        "quote": None,
        "settlement": None,
        "settlement_ref": None,
        "settlement_status": None,
        "created_at": _now(),
        "updated_at": _now(),
    }

    insert_refund(record)

    if idempotency_key:
        set_idempotency_key(idempotency_key, refund_id)

    quote = _engine.quote(rail, amount, currency)
    settlement = _engine.settle(rail, refund_id, amount, currency)

    settlement_ref = (
        settlement.get("settlement_ref")
        or settlement.get("reference")
        or settlement.get("txid")
        or settlement.get("transaction_id")
        or settlement.get("id")
    )

    update_refund(
        refund_id,
        quote=quote,
        settlement=settlement,
        settlement_ref=settlement_ref,
        status="pending",
        updated_at=_now(),
    )

    saved = db_get_refund(refund_id)
    return saved if saved else record


def get_refund(refund_id: str) -> Optional[Dict[str, Any]]:
    return db_get_refund(refund_id)


def refresh_pending_refunds() -> int:
    updated_count = 0

    pending = list_pending_refunds()
    for refund in pending:
        if not refund:
            continue

        st = _engine.status(refund["rail"], refund["settlement_ref"])

        # provider returns: { "status": "...", ... } (your kaspa provider does)
        # accept either "state" or "status" so we're robust
        state = st.get("state") or st.get("status")

        if state == "confirmed":
            update_refund(
                refund["refund_id"],
                status="settled",
                settlement_status=st,
                updated_at=_now(),
            )
            updated_count += 1

            _emit_webhook(
                "refund.settled",
                {
                    "refund_id": refund["refund_id"],
                    "rail": refund["rail"],
                    "amount": refund["amount"],
                    "currency": refund["currency"],
                    "settled_at": _now(),
                },
            )

    return updated_count
