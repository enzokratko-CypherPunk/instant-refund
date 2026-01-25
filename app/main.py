from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from app.core.config import settings
from app.services.rpc import submit_transaction

app = FastAPI(title="Instant Refund Engine")

class RefundRequest(BaseModel):
    amount: int
    recipient_address: str
    merchant_id: str

@app.get("/")
def read_root():
    return {"status": "System Online", "mode": "MAINNET"}

@app.get("/__debug/signer-test")
def debug_signer():
    try:
        # Test connection to Signer
        r = requests.get(f"{settings.SIGNER_URL.replace('/sign', '')}/healthz", timeout=3)
        return {"signer_status": r.status_code, "url": settings.SIGNER_URL}
    except Exception as e:
        return {"error": str(e)}

@app.post("/v1/refunds/instant")
def process_refund(request: RefundRequest):
    # 1. PREPARE
    payload = {
        "amount": request.amount,
        "to_address": request.recipient_address,
        "merchant_id": request.merchant_id
    }

    # 2. SIGN (Securely)
    try:
        signer_resp = requests.post(settings.SIGNER_URL, json=payload, timeout=10)
        signer_resp.raise_for_status()
        signed_data = signer_resp.json()
        tx_hex = signed_data.get("signed_hex")
        if not tx_hex:
            raise HTTPException(status_code=500, detail="Signer returned no hex")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Signer Failed: {str(e)}")

    # 3. BROADCAST (To Mainnet)
    rpc_response = submit_transaction(tx_hex)
    
    if "error" in rpc_response:
         raise HTTPException(status_code=502, detail=f"Node Broadcast Failed: {rpc_response['error']}")

    return {
        "status": "success",
        "txid": rpc_response.get("result", {}).get("transactionId"),
        "details": rpc_response
    }
