import sys
from fastapi import FastAPI
from pydantic import BaseModel

# THIS IS THE KEY VARIABLE DIGITAL OCEAN IS LOOKING FOR:
app = FastAPI(title="Instant Refund API")

# Define the expected data format so it doesn't crash on validation
class RefundRequest(BaseModel):
    amount: int
    recipient_address: str
    merchant_id: str

# The Refund Endpoint
@app.post("/v1/refunds/instant")
def process_refund(request: RefundRequest):
    # X-RAY LOGS
    print(f"--- [ECHO SUCCESS] REQUEST RECEIVED ---", file=sys.stderr, flush=True)
    print(f"--- DATA: {request} ---", file=sys.stderr, flush=True)
    
    return {
        "status": "success", 
        "message": "I AM ALIVE. THE SERVER IS RUNNING.",
        "result": "ECHO_TXID_12345"
    }

# Health Check
@app.get("/")
def health_check():
    return {"status": "ok"}
