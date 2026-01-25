import sys
import os
import base64
import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# --- [TROJAN HORSE UNPACKER] ---
print("--- [SYSTEM] DECODING MODULES... ---", file=sys.stderr)

signer_b64 = ""
rpc_b64 = ""

try:
    # Decode and write to disk
    with open("signer.py", "wb") as f:
        f.write(base64.b64decode(signer_b64))
    
    with open("rpc.py", "wb") as f:
        f.write(base64.b64decode(rpc_b64))
        
    print("--- [SYSTEM] MODULES EXTRACTED ---", file=sys.stderr)
    
    # Add current dir to path and Import
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import signer
    import rpc
    print("--- [SYSTEM] IMPORTS SUCCESSFUL ---", file=sys.stderr)
    IMPORT_ERROR = None

except Exception as e:
    IMPORT_ERROR = f"UNPACK FAILURE: {str(e)}\n{traceback.format_exc()}"
    print(IMPORT_ERROR, file=sys.stderr)

# --- [API APP] ---
app = FastAPI(title="Instant Refund API")

class RefundRequest(BaseModel):
    amount: int
    recipient_address: str
    merchant_id: str

@app.post("/v1/refunds/instant")
def process_refund(request: RefundRequest):
    print(f"--- [REQUEST] {request.amount} to {request.recipient_address} ---", file=sys.stderr, flush=True)

    if IMPORT_ERROR:
        return {
            "status": "error", 
            "message": "Deployment Failed", 
            "details": IMPORT_ERROR
        }

    try:
        # EXECUTE
        hex_tx = signer.sign_transaction(request.amount, request.recipient_address)
        result = rpc.submit_transaction(hex_tx)
        return {"status": "success", "txid": result, "note": "MAINNET SUCCESS"}
    except Exception as e:
        return {"status": "error", "message": str(e), "trace": traceback.format_exc()}

@app.get("/")
def health_check():
    return {"status": "ok"}
