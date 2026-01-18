"""
Instant Refund API entrypoint (DigitalOcean App Platform).

This module intentionally:
- Imports the existing FastAPI app from app.api
- Adds a deterministic connectivity probe endpoint to kaspad

Endpoint:
  GET /debug/kaspad-connect
Environment variables (optional):
  KASPA_RPC_HOST (default: 10.17.0.5)
  KASPA_RPC_PORT (default: 16110)
"""

import os
import socket
from app.api import app  # keep existing routes/app wiring intact


@app.get("/debug/kaspad-connect")
def debug_kaspad_connect():
    host = os.getenv("KASPA_RPC_HOST", "10.17.0.5")
    port = int(os.getenv("KASPA_RPC_PORT", "16110"))
    timeout = float(os.getenv("KASPA_RPC_TIMEOUT", "3"))

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        s.close()
        return {"status": "ok", "message": f"Connected to kaspad at {host}:{port}"}
    except Exception as e:
        return {"status": "error", "error": str(e), "target": f"{host}:{port}"}
