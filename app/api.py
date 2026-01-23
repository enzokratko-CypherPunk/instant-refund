from fastapi import FastAPI, HTTPException
import os
import time
import base64
import hmac
import hashlib
import httpx

app = FastAPI(title="Instant Refund API")

SIGNER_SHARED_SECRET = "DEBUG_SHARED_SECRET_DO_NOT_KEEP"
shared_secret = SIGNER_SHARED_SECRET.encode("utf-8")

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

    signer_url = "https://instant-refund-signer-XXXXX.ondigitalocean.app/sign"

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(signer_url, json=body)

    if resp.status_code != 200:
        raise HTTPException(status_code=500, detail=resp.text)

    return resp.json()



