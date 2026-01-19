from __future__ import annotations

from enum import Enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RefundStatus(str, Enum):
    CREATED = "created"
    PENDING_SETTLEMENT = "pending_settlement"
    SETTLED = "settled"
    FAILED = "failed"


class InstantRefundRequest(BaseModel):
    """
    API request from merchant/POS to initiate an instant refund.
    """
    merchant_id: str = Field(..., description="Merchant identifier")
    order_id: str = Field(..., description="Merchant order identifier")
    customer_id: str = Field(..., description="Customer identifier")
    amount: float = Field(..., gt=0, description="Refund amount (positive)")
    reason: Optional[str] = Field(None, description="Optional refund reason")
    idempotency_key: Optional[str] = Field(
        None,
        description="Client-provided idempotency key to prevent duplicate refunds"
    )


class RefundReceipt(BaseModel):
    """
    API response returned immediately after refund creation or lookup.
    """
    refund_id: str
    status: RefundStatus
    merchant_id: str
    order_id: str
    customer_id: str
    amount: str
    created_at: datetime
    receipt_message: str
    settlement_reference: Optional[str] = None


class RefreshResponse(BaseModel):
    """
    Response from POST /v1/refunds/refresh indicating how many refunds advanced state.
    """
    updated: int
