import sys
import os
import glob
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Instant Refund API")

# --- DEBUG: FILE SYSTEM X-RAY ---
@app.get("/debug/files")
def list_files():
    # This lists all files in the current folder so we can see if signer.py is actually there
    cwd = os.getcwd()
    files = []
    for root, dirs, filenames in os.walk(cwd):
        for f in filenames:
            files.append(os.path.join(root, f))
    return {"cwd": cwd, "files": files}

# --- ATTEMPT IMPORT ---
try:
    # Try neighbor import
    from . import signer
    from . import rpc
    IMPORT_ERROR = None
except ImportError:
    try:
        # Try root import
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        import signer
        import rpc
        IMPORT_ERROR = None
    except Exception as e:
        IMPORT_ERROR = str(e)

class RefundRequest(BaseModel):
    amount: int
    recipient_address: str
    merchant_id: str

@app.post("/v1/refunds/instant")
def process_refund(request: RefundRequest):
    if IMPORT_ERROR:
        # If it fails, we tell you WHY and WHAT FILES EXIST
        return {
            "status": "error",
            "error": "Missing Modules",
            "details": IMPORT_ERROR,
            "help": "Go to /debug/files to see what is missing."
        }
    
    try:
        hex_tx = signer.sign_transaction(request.amount, request.recipient_address)
        result = rpc.submit_transaction(hex_tx)
        return {"status": "success", "txid": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
def health_check():
    return {"status": "ok"}
