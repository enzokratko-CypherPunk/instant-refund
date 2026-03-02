# ENV: LOCAL Windows PowerShell
# Purpose: Wire /v1/refunds/instant to persist refund + signed intent (no broadcast)
# Method: Full-file rewrite of app/api.py
# Safety: No signer, no kaspad, no side effects

$ErrorActionPreference = "Stop"

$root = "C:\Users\brian\instant-refund\instant-refund"
$target = Join-Path $root "app\api.py"

if (-not (Test-Path $target)) {
  throw "Target file not found: $target"
}

Copy-Item $target "$target.bak" -Force
Write-Host "Backup created: api.py.bak"

@'
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime

from app.store import STORE

app = FastAPI()

class InstantRefundRequest(BaseModel):
    merchant_id: str
    original_payment_id: str
    amount_cents: int
    currency: str = "USD"

class InstantRefundResponse(BaseModel):
    refund_id: str
    signed_intent_id: str
    status: str

@app.post("/v1/refunds/instant", response_model=InstantRefundResponse)
def instant_refund(req: InstantRefundRequest):
    refund_id = str(uuid4())
    signed_intent_id = str(uuid4())
    now = datetime.utcnow()

    try:
        with STORE.transaction():
            STORE.execute(
                """
                INSERT INTO refunds (
                    refund_id,
                    merchant_id,
                    original_payment_id,
                    amount_cents,
                    currency,
                    status,
                    created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (refund_id) DO NOTHING
                """,
                (
                    refund_id,
                    req.merchant_id,
                    req.original_payment_id,
                    req.amount_cents,
                    req.currency,
                    "PENDING",
                    now,
                ),
            )

            STORE.execute(
                """
                INSERT INTO signed_intents (
                    signed_intent_id,
                    refund_id,
                    status,
                    created_at
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    signed_intent_id,
                    refund_id,
                    "PENDING",
                    now,
                ),
            )

        return InstantRefundResponse(
            refund_id=refund_id,
            signed_intent_id=signed_intent_id,
            status="PENDING",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
'@ | Set-Content -Path $target -NoNewline

Write-Host "Rewrote: app/api.py"
Write-Host "/v1/refunds/instant is now stateful (no broadcast)."
