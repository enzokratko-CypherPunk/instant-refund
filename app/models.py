from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal

class RefundRequest(BaseModel):
    merchant_id: str
    transaction_id: str
    amount: Decimal
    currency: str = "USD"
    reason: str

class RefundResponse(BaseModel):
    refund_id: UUID
    status: str
