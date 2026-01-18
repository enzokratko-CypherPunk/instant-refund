from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


class RefundState(str, Enum):
    REQUESTED = "requested"
    SETTLING = "settling"
    SETTLED = "settled"
    FAILED = "failed"


@dataclass
class Refund:
    refund_id: str
    merchant_id: str
    original_tx_id: str
    amount: float
    currency: str

    state: RefundState
    created_at: datetime
    updated_at: datetime

    settlement_tx_id: Optional[str] = None
    failure_reason: Optional[str] = None
