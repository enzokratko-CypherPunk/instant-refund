import sys
import os
import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# --- THE FIX: ADD CURRENT FOLDER TO SEARCH PATH ---
# This allows signer.py to do "import rpc" without crashing.
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# --- SAFE IMPORT BLOCK ---
signer = None
rpc = None
IMPORT_ERROR = None

try:
    # Now standard imports will work because we fixed the path
    import signer
    import rpc
    print("--- [SYSTEM] MODULES LOADED SUCCESSFULLY ---", file=sys.stderr)
except Exception as e:
    IMPORT_ERROR = f"IMPORT FAILURE: {str(e)}\n{traceback.format_exc()}"
    print(IMPORT_ERROR, file=sys.stderr)

app = FastAPI(title="Instant Refund API")

class RefundRequest(BaseModel):
    amount: int
    recipient_address: str
    merchant_id: str

@app.post("/v1/refunds/instant")
def process_refund(request: RefundRequest):
    print(f"--- [REQUEST] {request.amount} to {request.recipient_address} ---", file=sys.stderr, flush=True)

    # 1. REPORT IMPORT ERRORS IF ANY
    if IMPORT_ERROR:
        print(f"--- [CRASH] {IMPORT_ERROR} ---", file=sys.stderr)
        # We return the actual error text so you can see it in PowerShell
        return {
            "status": "error",
            "message": "Server Configuration Error",
            "details": IMPORT_ERROR
        }
    
    try:
        # 2. SIGN AND BROADCAST
        print("--- [STEP 1] SIGNING ---", file=sys.stderr, flush=True)
        hex_tx = signer.sign_transaction(request.amount, request.recipient_address)
        
        print("--- [STEP 2] BROADCASTING ---", file=sys.stderr, flush=True)
        result = rpc.submit_transaction(hex_tx)
        
        return {"status": "success", "txid": result}

    except Exception as e:
        err = f"PROCESS FAILED: {str(e)}"
        print(err, file=sys.stderr, flush=True)
        # Return error as JSON so we can read it easily
        return {"status": "error", "message": err}

@app.get("/")
def health_check():
    return {"status": "ok", "modules_loaded": IMPORT_ERROR is None}
