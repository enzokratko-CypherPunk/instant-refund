from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os
import base64
import time
import hmac
import hashlib
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

app = FastAPI(title="Instant Refund Signer")

# ---- Load secrets ----

PRIVATE_KEY_B64 = os.getenv("KASPA_SIGNER_PRIVATE_KEY")
SHARED_SECRET_B64 = os.getenv("SIGNER_SHARED_SECRET")

if not PRIVATE_KEY_B64 or not SHARED_SECRET_B64:
    raise RuntimeError("Signer secrets not configured")

private_key = ed25519.Ed25519PrivateKey.from_private_bytes(
    base64.b64decode(PRIVATE_KEY_B64)
)

shared_secret = base64.b64decode(SHARED_SECRET_B64)

# ---- Models ----

class SignRequest(BaseModel):
    payload: str
    timestamp: int
    signature: str

# ---- Helpers ----

def verify_hmac(payload: str, timestamp: int, signature: str):
    msg = f"{payload}:{timestamp}".encode()
    expected = hmac.new(shared_secret, msg, hashlib.sha256).digest()
    provided = base64.b64decode(signature)

    if not hmac.compare_digest(expected, provided):
        raise HTTPException(status_code=403, detail="Invalid HMAC")

    if abs(time.time() - timestamp) > 60:
        raise HTTPException(status_code=403, detail="Stale request")

# ---- Routes ----

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/sign")
def sign(req: SignRequest):
    verify_hmac(req.payload, req.timestamp, req.signature)

    sig = private_key.sign(req.payload.encode())

    return {
        "signature": base64.b64encode(sig).decode()
    }
