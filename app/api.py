from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models import RefundRequest, RefundResponse
from app.settlement import create_refund, get_refund

router = APIRouter()


@router.post("/refunds", response_model=RefundResponse)
def create_refund_endpoint(req: RefundRequest):
    return create_refund(req)


@router.get("/refunds/{refund_id}", response_model=RefundResponse)
def get_refund_endpoint(refund_id: str):
    try:
        return get_refund(refund_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Refund not found")
