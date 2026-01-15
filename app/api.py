from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

from app.settlement import create_refund, get_refund
from app.settlement.engine import refresh_pending_refunds


router = APIRouter()


class RefundRequest(BaseModel):
    amount: int = Field(..., ge=1, description="Refund amount in smallest unit for MVP (int).")
    currency: str = Field(default="USD", min_length=3, max_length=8)
    rail: str = Field(default="kaspa", min_length=2, max_length=32)


class RefundResponse(BaseModel):
    refund_id: str
    amount: int
    currency: str
    rail: str
    status: str
    idempotency_key: Optional[str] = None
    quote: Optional[Dict[str, Any]] = None
    settlement: Optional[Dict[str, Any]] = None
    settlement_ref: Optional[str] = None
    settlement_status: Optional[Dict[str, Any]] = None
    created_at: int
    updated_at: int


def _err(code: str, message: str, http_status: int = 400) -> None:
    raise HTTPException(
        status_code=http_status,
        detail={
            "error": {
                "code": code,
                "message": message,
            }
        },
    )


@router.post("/refunds", response_model=RefundResponse)
def create_refund_endpoint(
    req: RefundRequest,
    idempotency_key: Optional[str] = Header(default=None, alias="Idempotency-Key"),
):
    try:
        record = create_refund(
            amount=req.amount,
            currency=req.currency,
            rail=req.rail,
            idempotency_key=idempotency_key,
        )
        return record
    except ValueError as e:
        msg = str(e)
        if msg.startswith("unsupported_rail:"):
            _err("unsupported_rail", msg.replace("unsupported_rail:", "Unsupported rail: "), 400)
        _err("invalid_request", "Invalid request", 400)
    except Exception:
        _err("internal_error", "Unexpected error creating refund", 500)


@router.get("/refunds/{refund_id}", response_model=RefundResponse)
def get_refund_endpoint(refund_id: str):
    record = get_refund(refund_id)
    if not record:
        _err("refund_not_found", "Refund does not exist", 404)
    return record


@router.post("/refunds/refresh")
def refresh_refunds():
    updated = refresh_pending_refunds()
    return {"updated": updated}
