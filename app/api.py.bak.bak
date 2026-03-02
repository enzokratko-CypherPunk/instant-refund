from fastapi import FastAPI, HTTPException
import os
import time
import base64
import hmac
import hashlib
import httpx

app = FastAPI(title="Instant Refund API")

SIGNER_SHARED_SECRET = os.getenv("SIGNER_SHARED_SECRET")

if not SIGNER_SHARED_SECRET:
    raise RuntimeError("SIGNER_SHARED_SECRET not set")

shared_secret = base64.b64decode(SIGNER_SHARED_SECRET)

@app.get("/__debug/signer-test")
async def signer_test():
    payload = "hello-signer"
    timestamp = int(time.time())

    msg = f"{payload}:{timestamp}".encode()
    sig = hmac.new(shared_secret, msg, hashlib.sha256).digest()
    sig_b64 = base64.b64encode(sig).decode()

    body = {
        "payload": payload,
        "timestamp": timestamp,
        "signature": sig_b64
    }

    signer_url = "https://instant-refund-api-l99qr.ondigitalocean.app/signer/sign"

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(signer_url, json=body)

    if resp.status_code != 200:
        raise HTTPException(status_code=500, detail=resp.text)

    return resp.json()
