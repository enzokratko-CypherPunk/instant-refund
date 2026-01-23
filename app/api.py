from fastapi import APIRouter, HTTPException
import os
import httpx

router = APIRouter()

SIGNER_SHARED_SECRET = os.getenv("SIGNER_SHARED_SECRET")
SIGNER_URL = os.getenv("SIGNER_URL")

@router.get("/__debug/signer-test")
async def signer_test():
    if not SIGNER_URL:
        return {
            "status": "ok",
            "signer_call": "skipped",
            "reason": "SIGNER_URL not set"
        }

    headers = {}
    if SIGNER_SHARED_SECRET:
        headers["X-Signer-Secret"] = SIGNER_SHARED_SECRET

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                SIGNER_URL,
                json={"message": "hello-signer"},
                headers=headers
            )
        return {
            "status": "ok",
            "http_status": resp.status_code,
            "body": resp.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))