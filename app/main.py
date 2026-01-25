from fastapi import APIRouter, Depends, HTTPException
from typing import Any
import sys

router = APIRouter()

@router.post("/instant")
def process_refund(
    refund_request: dict,
) -> Any:
    # DEBUG: ECHO TEST
    print("--- [ECHO TEST] ALIVE AND KICKING ---", file=sys.stderr, flush=True)
    return {
        "status": "success", 
        "message": "I AM ALIVE. PIPES ARE WORKING.",
        "received": refund_request
    }
