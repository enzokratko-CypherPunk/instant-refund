from fastapi import FastAPI
from fastapi.responses import JSONResponse
import socket

app = FastAPI(
    title="Instant Refund API",
    version="0.1.0"
)

# ------------------------------------------------------
# Root — human / partner friendly
# ------------------------------------------------------
@app.get("/")
def root():
    return {
        "service": "Instant Refund API",
        "status": "running",
        "health_endpoint": "/health"
    }

# ------------------------------------------------------
# Health — readiness / liveness probe
# ------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# ------------------------------------------------------
# Debug — kaspad connectivity (NON-FATAL)
# ------------------------------------------------------
@app.get("/debug/kaspad-connect")
def debug_kaspad_connect():
    kaspad_host = "127.0.0.1"
    kaspad_port = 16110  # typical kaspad RPC port

    try:
        with socket.create_connection((kaspad_host, kaspad_port), timeout=2):
            return {
                "kaspad_reachable": True,
                "host": kaspad_host,
                "port": kaspad_port
            }
    except Exception as e:
        return JSONResponse(
            status_code=200,
            content={
                "kaspad_reachable": False,
                "host": kaspad_host,
                "port": kaspad_port,
                "error": str(e)
            }
        )
