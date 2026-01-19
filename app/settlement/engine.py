from __future__ import annotations

from ..store import STORE
from ..models import RefundStatus

def process_pending_refunds(limit: int = 50) -> int:
    """
    Task #2 implementation:
    - Uses Postgres as authoritative ledger
    - Moves CREATED -> PENDING_SETTLEMENT to prove persistence and state transitions

    Task #3 will replace this with:
    - Kaspa testnet broadcast
    - txid tracking
    - confirmations -> SETTLED
    - failures -> FAILED (with retry policy + event log)
    """
    updated = 0
    recs = STORE.list_pending_for_settlement(limit=limit)

    for rec in recs:
        # Only transition CREATED -> PENDING_SETTLEMENT here (placeholder).
        if rec.status == RefundStatus.CREATED:
            STORE.mark_pending_settlement(rec.refund_id, settlement_reference=None)
            STORE.add_settlement_event(rec.refund_id, "MARKED_PENDING", {"note": "placeholder until kaspa broadcast"})
            updated += 1

    return updated
