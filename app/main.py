import sys
import os
import base64
import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

print("--- [SYSTEM] STARTING IN SALES DEMO MODE ---", file=sys.stderr)

# UNPACK DEMO MODULES
signer_b64 = "aW1wb3J0IHRpbWUKaW1wb3J0IGhhc2hsaWIKaW1wb3J0IHJhbmRvbQoKZGVmIHNpZ25fdHJhbnNhY3Rpb24oYW1vdW50LCB0b19hZGRyZXNzKToKICAgICMgU0lNVUxBVElPTiBNT0RFCiAgICAjIFdlIGdlbmVyYXRlIGEgZmFrZSB0cmFuc2FjdGlvbiBoYXNoIHRoYXQgbG9va3MgZXhhY3RseSBsaWtlIGEgcmVhbCBLYXNwYSBUWElELgogICAgIyBGb3JtYXQ6IDY0IGNoYXJhY3RlcnMgb2YgaGV4CiAgICAKICAgIHByaW50KGYiLS0tIFtERU1PXSBTSU1VTEFUSU5HIFNJR05JTkc6IHthbW91bnR9IC0+IHt0b19hZGRyZXNzfSAtLS0iKQogICAgCiAgICAjIEdlbmVyYXRlIHJhbmRvbSBoYXNoCiAgICByYW5kb21fZGF0YSA9IGYie2Ftb3VudH17dG9fYWRkcmVzc317dGltZS50aW1lKCl9e3JhbmRvbS5yYW5kaW50KDAsOTk5OSl9IgogICAgdHhpZCA9IGhhc2hsaWIuc2hhMjU2KHJhbmRvbV9kYXRhLmVuY29kZSgpKS5oZXhkaWdlc3QoKQogICAgCiAgICByZXR1cm4gdHhpZA=="
rpc_b64 = "ZGVmIHN1Ym1pdF90cmFuc2FjdGlvbihoZXhfdHgpOgogICAgIyBTSU1VTEFUSU9OIE1PREUKICAgICMgSW4gYSByZWFsIGFwcCwgdGhpcyBzZW5kcyB0byB0aGUgbm9kZS4KICAgICMgSW4gZGVtbyBtb2RlLCB3ZSBqdXN0IHJldHVybiB0aGUgVFhJRCAod2hpY2ggaXMgcGFzc2VkIGFzIGhleF90eCBoZXJlIGZvciBzaW1wbGljaXR5KQogICAgcHJpbnQoZiItLS0gW0RFTU9dIEJST0FEQ0FTVElORyBUWDoge2hleF90eH0gLS0tIikKICAgIHJldHVybiBoZXhfdHg="

try:
    with open("signer.py", "wb") as f: f.write(base64.b64decode(signer_b64))
    with open("rpc.py", "wb") as f: f.write(base64.b64decode(rpc_b64))
    
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import signer
    import rpc
    print("--- [SYSTEM] DEMO ENGINE LOADED ---", file=sys.stderr)
    IMPORT_ERROR = None
except Exception as e:
    IMPORT_ERROR = str(e)

app = FastAPI(title="Instant Refund API (DEMO)")

class RefundRequest(BaseModel):
    amount: int
    recipient_address: str
    merchant_id: str

@app.post("/v1/refunds/instant")
def process_refund(request: RefundRequest):
    if IMPORT_ERROR:
        return {"status": "error", "details": IMPORT_ERROR}

    # EXECUTE DEMO TRANSACTION
    try:
        # 1. Sign (returns a TXID in demo mode)
        txid = signer.sign_transaction(request.amount, request.recipient_address)
        
        # 2. Broadcast (returns the same TXID)
        final_txid = rpc.submit_transaction(txid)
        
        return {
            "status": "success", 
            "txid": final_txid, 
            "message": "REFUND_COMPLETE",
            "mode": "SALES_DEMO"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
def health_check():
    return {"status": "ok", "mode": "demo"}
