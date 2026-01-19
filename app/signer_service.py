import os
import time
import hmac
import hashlib
from typing import Optional, Literal, Dict, Any

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field

app = FastAPI(
    title="Instant Refund Signer",
    version="0.1.0"
)

# -----------------------------
# Config (env)
# -----------------------------
SIGNER_NETWORK = os.getenv("KASPA_NETWORK", "testnet")  # testnet|mainnet later
SIGNER_FROM_ADDRESS = os.getenv("KASPA_REFUND_FROM_ADDRESS", "")
SIGNER_PRIVATE_KEY = os.getenv("KASPA_SIGNER_PRIVATE_KEY", "")  # testnet key first
SIGNER_SHARED_SECRET = os.getenv("SIGNER_SHARED_SECRET", "")    # HMAC auth between worker and signer

MAX_REFUND_ATOMIC = int(os.getenv("MAX_REFUND_ATOMIC", "0"))    # 0 means "not set" => deny
MAX_PER_MINUTE = int(os.getenv("MAX_SIGNS_PER_MINUTE", "30"))

# simple in-memory rate limiter (v1). For multi-replica, move to DB/Redis later.
_bucket_minute = int(time.time() // 60)
_bucket_count = 0


def _rate_limit_ok() -> bool:
    global _bucket_minute, _bucket_count
    now_min = int(time.time() // 60)
    if now_min != _bucket_minute:
        _bucket_minute = now_min
        _bucket_count = 0
    _bucket_count += 1
    return _bucket_count <= MAX_PER_MINUTE


def _require_config():
    if not SIGNER_SHARED_SECRET:
        raise HTTPException(status_code=503, detail="SIGNER_SHARED_SECRET not set")
    if not SIGNER_FROM_ADDRESS:
        raise HTTPException(status_code=503, detail="KASPA_REFUND_FROM_ADDRESS not set")
    if not SIGNER_PRIVATE_KEY:
        raise HTTPException(status_code=503, detail="KASPA_SIGNER_PRIVATE_KEY not set")
    if MAX_REFUND_ATOMIC <= 0:
        raise HTTPException(status_code=503, detail="MAX_REFUND_ATOMIC not set (must be > 0)")


def _hmac_hex(payload_bytes: bytes) -> str:
    return hmac.new(SIGNER_SHARED_SECRET.encode("utf-8"), payload_bytes, hashlib.sha256).hexdigest()


def _auth_ok(given: str, payload_bytes: bytes) -> bool:
    expected = _hmac_hex(payload_bytes)
    # timing-safe compare
    return hmac.compare_digest(given or "", expected)


# -----------------------------
# Models
# -----------------------------
class TxIntent(BaseModel):
    refund_id: str = Field(..., min_length=1, max_length=64)
    network: Literal["testnet", "mainnet"]
    from_address: str = Field(..., min_length=10, max_length=128)
    to_address: str = Field(..., min_length=10, max_length=128)
    amount_atomic: int = Field(..., gt=0)
    expires_at_unix: int = Field(..., gt=0)
    idempotency_key: str = Field(..., min_length=1, max_length=128)

class SignRequest(BaseModel):
    job_id: int
    tx_intent: TxIntent
    unsigned_tx_bytes_b64: str = Field(..., min_length=1)

class SignResponse(BaseModel):
    signed_tx_bytes_b64: str
    audit: Dict[str, Any]


@app.get("/health")
def health():
    return {"status": "ok", "service": "signer"}


@app.post("/internal/sign", response_model=SignResponse)
def sign(req: SignRequest, x_signer_auth: Optional[str] = Header(default=None)):
    # hard requirements
    _require_config()

    # auth
    # We auth the canonical bytes of (job_id + tx_intent + unsigned_tx_bytes_b64) using HMAC
    canonical = (str(req.job_id) + "|" + req.tx_intent.model_dump_json() + "|" + req.unsigned_tx_bytes_b64).encode("utf-8")
    if not _auth_ok(x_signer_auth, canonical):
        raise HTTPException(status_code=401, detail="invalid signer auth")

    # rate limit
    if not _rate_limit_ok():
        raise HTTPException(status_code=429, detail="rate limit exceeded")

    # policy checks
    now = int(time.time())
    if req.tx_intent.expires_at_unix < now:
        raise HTTPException(status_code=403, detail="tx intent expired")

    if req.tx_intent.network != SIGNER_NETWORK:
        raise HTTPException(status_code=403, detail=f"network not allowed: {req.tx_intent.network}")

    if req.tx_intent.from_address != SIGNER_FROM_ADDRESS:
        raise HTTPException(status_code=403, detail="from_address not allowed")

    if req.tx_intent.amount_atomic > MAX_REFUND_ATOMIC:
        raise HTTPException(status_code=403, detail="amount exceeds policy limit")

    # v1 signing placeholder:
    # We DO NOT implement cryptography here yet.
    # We return the unsigned bytes as "signed" to validate the full delegated flow end-to-end.
    #
    # Next step (immediately after this is deployed and stable):
    # Replace this with real Kaspa signing using the Kaspa SDK or kaspad signing RPC.
    signed_stub = req.unsigned_tx_bytes_b64

    return {
        "signed_tx_bytes_b64": signed_stub,
        "audit": {
            "job_id": req.job_id,
            "refund_id": req.tx_intent.refund_id,
            "network": req.tx_intent.network,
            "amount_atomic": req.tx_intent.amount_atomic,
            "policy_version": "v1",
            "signed_at_unix": int(time.time())
        }
    }
