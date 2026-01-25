\""\""
Routers only (NO FastAPI instance here).
Single-source-of-truth app object lives in app/main.py.

This prevents route drift where DO runs app.main:app but routes
were accidentally defined on a different FastAPI() instance.
\""\""

from fastapi import APIRouter, HTTPException
import os
import httpx

router = APIRouter()

# --- Optional configuration ---
# If SIGNER_SHARED_SECRET is set, /__debug/signer-test will attempt to call the signer.
# If it is not set, the endpoint still exists and returns a deterministic status.
SIGNER_SHARED_SECRET = os.getenv("SIGNER_SHARED_SECRET")

# NOTE: This should be the INTERNAL URL if DO provides one. If not available, leave unset.
# You can override via environment variable without code changes.
SIGNER_URL = os.getenv("SIGNER_URL")  # e.g. http://instant-refund-signer:8080/signer/sign (if internal DNS exists)

@router.get("/__debug/signer-test")
async def signer_test():
    # Endpoint ALWAYS exists. It will not disappear due to app wiring drift.
    if not SIGNER_URL:
        return {"status": "ok", "signer_call": "skipped", "reason": "SIGNER_URL not set"}

    headers = {}
    if SIGNER_SHARED_SECRET:
        headers["X-Signer-Secret"] = SIGNER_SHARED_SECRET

    body = {"message": "hello-signer"}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(SIGNER_URL, json=body, headers=headers)
        return {
            "status": "ok",
            "signer_url": SIGNER_URL,
            "http_status": resp.status_code,
            "body": resp.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signer call failed: {e}")