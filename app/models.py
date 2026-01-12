from __future__ import annotations

from typing import Optional, Literal
from pydantic import BaseModel, Field


Rail = Literal["kaspa", "mock_bank"]
RefundStatus = Literal["created", "submitted", "confirmed", "failed"]


class RefundRequest(BaseModel):
    amount: int = Field(..., ge=1, description="Amount in smallest unit (e.g. cents)")
    currency: str = Field("USD", min_length=3, max_length=10)
    original_tx_id: Optional[str] = Field(None, description="Original transaction reference")
    merchant_id: Optional[str] = Field(None, description="Tenant/merchant id (future: API key maps to this)")
    rail: Rail = Field("mock_bank", description="Settlement rail to use (kaspa | mock_bank)")


class RefundResponse(BaseModel):
    refund_id: str
    status: RefundStatus
    amount: int
    currency: str
    original_tx_id: Optional[str] = None
    merchant_id: Optional[str] = None
    rail: Rail = "mock_bank"

    # settlement fields
    settlement_ref: Optional[str] = None
    deposit_address: Optional[str] = None
    network: Optional[str] = None
