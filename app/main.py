"""
Instant Refund API entrypoint (DigitalOcean App Platform).

This module is the authoritative router wiring point.
"""

import os
import socket
import time
import base64
import hmac
import hashlib
import httpx

from app.api import app
from app.routes.refunds import router as refunds_router


# ---- Core router wiring (DETERMINISTIC) ----
app.include_router(refunds_router)


# ---- Debug endpoints ----

@app.get("/debug/kaspad-connect")
def debug_kaspad_connect():
    host = os.getenv("KASPA_RPC_HOST", "10.17.0.5")
    port = int(os.getenv("KASPA_RPC_PORT", "16110"))
    timeout = float(os.getenv("KASPA_RPC_TIMEOUT", "3"))

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        s.close()
        return {"status": "ok", "message": f"Connected to kaspad at {host}:{port}"}
    except Exception as e:
        return {"status": "error", "error": str(e), "target": f"{host}:{port}"}


@app.get("/__debug/signer-test")
async def debug_signer_test():
    secret_b64 = os.getenv("SIGNER_SHARED_SECRET")
    if not secret_b64:
        return {"error": "SIGNER_SHARED_SECRET not set"}

    shared_secret = base64.b64decode(secret_b64)

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
        return {"error": resp.text}

    return resp.json()