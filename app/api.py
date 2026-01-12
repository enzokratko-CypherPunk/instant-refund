from fastapi import APIRouter
from uuid import uuid4
from app.models import RefundRequest, RefundResponse

refund_store = {}

router = APIRouter()

@router.post("/refunds", response_model=RefundResponse)
def create_refund(request: RefundRequest):
    refund_id = str(uuid4())

    refund = RefundResponse(
        refund_id=refund_id,
        status="RECEIVED"
    )

    refund_store[refund_id] = refund
    return refund

@router.get("/refunds/{refund_id}", response_model=RefundResponse)
def get_refund(refund_id: str):
    refund = refund_store.get(refund_id)

    if not refund:
        return {"detail": "Refund not found"}

    return refund

