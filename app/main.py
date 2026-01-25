import sys
import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# FORCE IMPORTS FROM SAME FOLDER
try:
    from . import signer
    from . import rpc
    print("--- [SYSTEM] NEIGHBOR MODULES LOADED ---", file=sys.stderr)
    IMPORT_ERROR = None
except ImportError as e:
    # If that fails, try absolute
    try:
        import app.signer as signer
        import app.rpc as rpc
        print("--- [SYSTEM] APP MODULES LOADED ---", file=sys.stderr)
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
    print(f"--- [MAINNET REQUEST] {request.amount} sompi to {request.recipient_address} ---", file=sys.stderr, flush=True)

    if IMPORT_ERROR:
        print(f"--- [FAILURE] CANNOT SIGN: {IMPORT_ERROR} ---", file=sys.stderr)
        # We return 500, but we INCLUDE the error text in the body so you can see it in PowerShell
        raise HTTPException(status_code=500, detail=f"Server Misconfiguration: {IMPORT_ERROR}")
    
    try:
        # THE MONEY LOGIC
        print("--- [STEP 1] INITIATING SIGNING ---", file=sys.stderr, flush=True)
        
        hex_transaction = signer.sign_transaction(
            amount=request.amount,
            to_address=request.recipient_address
        )
        
        print(f"--- [STEP 2] SIGNED. HEX LEN: {len(str(hex_transaction))} ---", file=sys.stderr, flush=True)

        print("--- [STEP 3] BROADCASTING TO RELAY ---", file=sys.stderr, flush=True)
        result = rpc.submit_transaction(hex_transaction)
        
        print(f"--- [SUCCESS] RESULT: {result} ---", file=sys.stderr, flush=True)
        
        return {
            "status": "success",
            "data": result,
            "note": "FUNDS BROADCASTED TO MAINNET"
        }

    except Exception as e:
        error_msg = f"REFUND FAILED: {str(e)}"
        print(error_msg, file=sys.stderr, flush=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "ok"}
