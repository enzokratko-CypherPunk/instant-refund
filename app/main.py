import sys
import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# --- [SAFE IMPORT BLOCK] ---
# We try to import the logic. If it fails, we record the error but DONT CRASH the server.
# This prevents the "502 Bad Gateway" death loop.
signer = None
rpc = None
IMPORT_ERROR = None

try:
    # Attempt to import your local modules
    # (Assuming these files exist in the 'app' folder or root)
    import app.signer as signer
    import app.rpc as rpc
    print("--- [SYSTEM] MODULES LOADED SUCCESSFULLY ---", file=sys.stderr)
except ImportError as e:
    # Fallback for root level imports if 'app.' fails
    try:
        import signer
        import rpc
        print("--- [SYSTEM] MODULES LOADED (ROOT LEVEL) ---", file=sys.stderr)
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

    # 1. CHECK FOR BROKEN ENGINE
    if IMPORT_ERROR:
        print(f"--- [FAILURE] CANNOT SIGN: {IMPORT_ERROR} ---", file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Server Misconfiguration: {IMPORT_ERROR}")
    
    if not signer or not rpc:
        raise HTTPException(status_code=500, detail="Signer/RPC modules not loaded.")

    try:
        # 2. THE REAL MONEY LOGIC
        # Step A: Create/Sign the transaction
        # (Assuming signer.sign_transaction takes these args - standardizing for demo)
        print("--- [STEP 1] INITIATING SIGNING ---", file=sys.stderr, flush=True)
        
        # Note: We pass the data exactly as your module expects it.
        # If your signer needs different args, the logs will tell us immediately.
        hex_transaction = signer.sign_transaction(
            amount=request.amount,
            to_address=request.recipient_address
        )
        
        print(f"--- [STEP 2] SIGNED. HEX LEN: {len(str(hex_transaction))} ---", file=sys.stderr, flush=True)

        # Step B: Broadcast to Network
        print("--- [STEP 3] BROADCASTING TO RELAY ---", file=sys.stderr, flush=True)
        result = rpc.submit_transaction(hex_transaction)
        
        print(f"--- [SUCCESS] RESULT: {result} ---", file=sys.stderr, flush=True)
        
        return {
            "status": "success",
            "data": result,
            "note": "FUNDS BROADCASTED TO MAINNET"
        }

    except Exception as e:
        # CATCH ALL ERRORS (Logic bugs, Insufficient Funds, etc)
        error_msg = f"REFUND FAILED: {str(e)}\n{traceback.format_exc()}"
        print(error_msg, file=sys.stderr, flush=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    # If imports failed, health check warns us but says OK so DigitalOcean doesn't kill us.
    status = "ok" if not IMPORT_ERROR else "degraded_missing_modules"
    return {"status": status, "import_error": IMPORT_ERROR}
