from __future__ import annotations

from typing import Dict, Any

from .providers.kaspa import KaspaSettlementProvider
from .providers.base import SettlementProvider


class SettlementEngine:
    """
    Chooses a provider based on requested rail.
    This is the layer that makes "partner integrations" inevitable later.
    """

    def __init__(self) -> None:
        self.providers: Dict[str, SettlementProvider] = {
            "kaspa": KaspaSettlementProvider(),
            # future: "stripe": StripeSettlementProvider(),
            # future: "paypal": PayPalSettlementProvider(),
            # future: "zelle": ZelleSettlementProvider(),
        }

    def quote(self, rail: str, amount: int, currency: str) -> Dict[str, Any]:
        provider = self._get_provider(rail)
        return provider.quote(amount=amount, currency=currency)

    def settle(self, rail: str, refund_id: str, amount: int, currency: str) -> Dict[str, Any]:
        provider = self._get_provider(rail)
        return provider.settle(refund_id=refund_id, amount=amount, currency=currency)

    def status(self, rail: str, settlement_ref: str) -> Dict[str, Any]:
        provider = self._get_provider(rail)
        return provider.status(settlement_ref=settlement_ref)

    def _get_provider(self, rail: str) -> SettlementProvider:
        rail_key = (rail or "").strip().lower()
        if rail_key not in self.providers:
            raise ValueError(f"Unsupported rail: {rail}")
        return self.providers[rail_key]
