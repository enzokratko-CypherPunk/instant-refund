from __future__ import annotations

import os
import socket
from fastapi import FastAPI

from app.api import router as refund_router


app = FastAPI(title="Instant Refund Closeout", version="0.1.0")

# -------------------------------------------------------------------
# Health endpoints
# -------------------------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/kaspa")
def kaspa_health():
    host = "165.227.115.22"
    port = 16110

    try:
        with socket.create_connection((host, port), timeout=2):
            return {
                "kaspa_node": "reachable",
                "host": host,
                "port": port,
            }
    except Exception as e:
        return {
            "kaspa_node": "unreachable",
            "error": str(e),
        }

# -------------------------------------------------------------------
# API routes
# -------------------------------------------------------------------

app.include_router(refund_router, prefix="/v1")
