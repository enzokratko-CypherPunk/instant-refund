from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter()

SIGNER_SHARED_SECRET = "DEBUG_SHARED_SECRET_DO_NOT_KEEP"
shared_secret = SIGNER_SHARED_SECRET.encode("utf-8")

@router.get("/__debug/signer-test")
async def signer_test():
    payload = "hello-signer"
    body = {"payload": payload}

    signer_url = "http://instant-refund-signer:8080/sign"

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(signer_url, json=body)

    if resp.status_code != 200:
        raise HTTPException(status_code=500, detail=resp.text)

    return resp.json()



