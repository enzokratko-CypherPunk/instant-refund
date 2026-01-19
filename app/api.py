from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Literal
import socket
import uuid
from datetime import datetime, timezone

app = FastAPI(
    title="Instant Refund API",
    version="0.1.0"
)

# ------------------------------------------------------
# Models
# ------------------------------------------------------
class InstantRefundRequest(BaseModel):
    original_transaction_id: str = Field(..., min_length=1, max_length=128)
    amount: float = Field(..., gt=0)
    currency: str = Field("USD", min_length=3, max_length=8)
    reason: Optional[str] = Field(None, max_length=256)
    merchant_id: Optional[str] = Field(None, max_length=128)
    customer_id: Optional[str] = Field(None, max_length=128)

class InstantRefundResponse(BaseModel):
    refund_id: str
    status: Literal["initiated"]
    refund_type: Literal["instant"]
    created_at: str
    original_transaction_id: str
    amount: float
    currency: str
    settlement: dict
    merchant_message: str

# ------------------------------------------------------
# Root — human / partner friendly
# ------------------------------------------------------
@app.get("/")
def root():
    return {
        "service": "Instant Refund API",
        "status": "running",
        "health_endpoint": "/health",
        "instant_refund_endpoint": "/refund/instant"
    }

# ------------------------------------------------------
# Health — readiness / liveness probe
# ------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# ------------------------------------------------------
# Debug — kaspad connectivity (NON-FATAL)
# ------------------------------------------------------
@app.get("/debug/kaspad-connect")
def debug_kaspad_connect():
    kaspad_host = "127.0.0.1"
    kaspad_port = 16110  # typical kaspad RPC port

    try:
        with socket.create_connection((kaspad_host, kaspad_port), timeout=2):
            return {
                "kaspad_reachable": True,
                "host": kaspad_host,
                "port": kaspad_port
            }
    except Exception as e:
        return JSONResponse(
            status_code=200,
            content={
                "kaspad_reachable": False,
                "host": kaspad_host,
                "port": kaspad_port,
                "error": str(e)
            }
        )

# ------------------------------------------------------
# Instant Refund — partner demo safe stub
# ------------------------------------------------------
@app.post("/refund/instant", response_model=InstantRefundResponse)
def refund_instant(req: InstantRefundRequest):
    refund_id = "irf_" + uuid.uuid4().hex[:12]
    created_at = datetime.now(timezone.utc).isoformat()

    # Demo-safe: we acknowledge instantly and mark settlement as pending.
    # No external calls. No database. No side effects.
    resp = {
        "refund_id": refund_id,
        "status": "initiated",
        "refund_type": "instant",
        "created_at": created_at,
        "original_transaction_id": req.original_transaction_id,
        "amount": float(req.amount),
        "currency": req.currency.upper(),
        "settlement": {
            "rail": "kaspa",
            "state": "pending",
            "note": "stubbed - settlement execution not yet wired"
        },
        "merchant_message": "Refund issued instantly. Settlement in progress."
    }

    return resp
