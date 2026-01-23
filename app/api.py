from fastapi import FastAPI, HTTPException
import httpx
import os

app = FastAPI()

# DEBUG / TEMP — hardcoded to remove all env ambiguity
SIGNER_SHARED_SECRET = "DEBUG_SHARED_SECRET_DO_NOT_KEEP"

@app.get("/__debug/signer-test")
async def signer_test():
    signer_url = "https://instant-refund-signer-XXXXX.ondigitalocean.app/signer/sign"

    payload = {
        "message": "hello-signer"
    }

    headers = {
        "X-Signer-Secret": SIGNER_SHARED_SECRET
    }

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(
            signer_url,
            json=payload,
            headers=headers
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=500, detail=resp.text)

    return resp.json()
