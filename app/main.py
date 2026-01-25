import sys
import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ROBUST IMPORT STRATEGY
# We try to import from the current package (neighbors) first.
try:
    from . import signer
    from . import rpc
    print("--- [SYSTEM] NEIGHBOR MODULES LOADED ---", file=sys.stderr)
    IMPORT_ERROR = None
except ImportError as e:
    # Fallback: maybe we are running as a script, not a package
    try:
        import signer
        import rpc
        print("--- [SYSTEM] STANDARD MODULES LOADED ---", file=sys.stderr)
        IMPORT_ERROR = None
    except Exception as e2:
        IMPORT_ERROR = f"CRITICAL MISSING PARTS: {str(e2)}\n{traceback.format_exc()}"
        print(IMPORT_ERROR, file=sys.stderr)

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
            "message": "Deployment Error: Files Missing", 
            "details": IMPORT_ERROR
        }

    try:
        # THE MONEY SHOT
        print("--- [STEP 1] SIGNING ---", file=sys.stderr, flush=True)
        hex_tx = signer.sign_transaction(request.amount, request.recipient_address)
        
        print("--- [STEP 2] BROADCASTING ---", file=sys.stderr, flush=True)
        result = rpc.submit_transaction(hex_tx)
        
        return {"status": "success", "txid": result, "note": "MAINNET SUCCESS"}

    except Exception as e:
        return {"status": "error", "message": str(e), "trace": traceback.format_exc()}

@app.get("/")
def health_check():
    return {"status": "ok"}
