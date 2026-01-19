from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Literal
import socket
import uuid
import os

from app.db import connect, init_schema_if_possible, utc_now_iso

app = FastAPI(
    title="Instant Refund API",
    version="0.1.0"
)

# Attempt schema init on boot, but never crash
init_schema_if_possible()

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
# Root
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
# Health (never depends on DB)
# ------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# ------------------------------------------------------
# Debug — kaspad connectivity (NON-FATAL)
# ------------------------------------------------------
@app.get("/debug/kaspad-connect")
def debug_kaspad_connect():
    kaspad_host = os.getenv("KASPAD_HOST", "kaspa-sidecar")
    kaspad_port = int(os.getenv("KASPAD_PORT", "16110"))

    try:
        with socket.create_connection((kaspad_host, kaspad_port), timeout=2):
            return {"kaspad_reachable": True, "host": kaspad_host, "port": kaspad_port}
    except Exception as e:
        return JSONResponse(status_code=200, content={
            "kaspad_reachable": False,
            "host": kaspad_host,
            "port": kaspad_port,
            "error": str(e)
        })

# ------------------------------------------------------
# Instant Refund — enqueue settlement job
# ------------------------------------------------------
@app.post("/refund/instant", response_model=InstantRefundResponse)
def refund_instant(req: InstantRefundRequest):
    try:
        # Ensure schema exists when DB is actually used
        init_schema_if_possible()

        refund_id = "irf_" + uuid.uuid4().hex[:12]
        created_at = utc_now_iso()
        currency = req.currency.upper()

        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO refunds (refund_id, created_at, original_transaction_id, amount, currency, status, settlement_state)
                    VALUES (%s, NOW(), %s, %s, %s, %s, %s);
                    """,
                    (refund_id, req.original_transaction_id, req.amount, currency, "initiated", "queued")
                )
                cur.execute(
                    """
                    INSERT INTO settlement_jobs (refund_id, state)
                    VALUES (%s, 'queued');
                    """,
                    (refund_id,)
                )
            conn.commit()

        return {
            "refund_id": refund_id,
            "status": "initiated",
            "refund_type": "instant",
            "created_at": created_at,
            "original_transaction_id": req.original_transaction_id,
            "amount": float(req.amount),
            "currency": currency,
            "settlement": {
                "rail": "kaspa",
                "state": "queued",
                "note": "worker will sign+broadcast via kaspad"
            },
            "merchant_message": "Refund issued instantly. Settlement in progress."
        }

    except RuntimeError as e:
        # DATABASE_URL missing or DB unavailable
        raise HTTPException(status_code=503, detail=str(e))
