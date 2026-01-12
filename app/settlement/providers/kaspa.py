from __future__ import annotations

import os
import time
import uuid
from typing import Dict, Any

from .base import SettlementProvider


class KaspaSettlementProvider(SettlementProvider):
    """
    Kaspa provider skeleton.
    Today: deterministic stub (no node calls).
    Next: replace internals with RPC / wallet / node integration.
    """

    def __init__(self) -> None:
        # future: KASPAD RPC / wallet config
        self.network = os.getenv("KASPA_NETWORK", "mainnet")
        self.confirmations_required = int(os.getenv("KASPA_CONFIRMATIONS_REQUIRED", "1"))

    def quote(self, amount: int, currency: str) -> Dict[str, Any]:
        # future: real fee estimation
        return {
            "rail": "kaspa",
            "network": self.network,
            "estimated_fee": 1,  # placeholder (units depend on how you represent amount)
            "currency": currency,
        }

    def settle(self, refund_id: str, amount: int, currency: str) -> Dict[str, Any]:
        # stub: create a deterministic-ish tx reference + deposit address placeholder
        # future: generate address, send transaction, return txid
        settlement_ref = f"kaspa_{uuid.uuid4().hex}"
        deposit_address = f"kaspa:{uuid.uuid4().hex[:32]}"  # placeholder
        return {
            "rail": "kaspa",
            "network": self.network,
            "settlement_ref": settlement_ref,
            "deposit_address": deposit_address,
            "submitted_at": int(time.time()),
            "status": "submitted",
        }

    def status(self, settlement_ref: str) -> Dict[str, Any]:
        # future: query tx status from node
        return {
            "settlement_ref": settlement_ref,
            "status": "confirmed",
            "confirmations_required": self.confirmations_required,
        }
