from fastapi import FastAPI
from app.api import router as refund_router

app = FastAPI(title="Instant Refund Closeout", version="0.1.0")

@app.get("/")
def health():
    return {"status": "ok"}

app.include_router(refund_router, prefix="/v1")
