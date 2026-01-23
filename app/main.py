from fastapi import FastAPI
from app.api import router as api_router

try:
    from app.routes.refunds import router as refunds_router
except Exception:
    refunds_router = None

app = FastAPI()

app.include_router(api_router)

if refunds_router is not None:
    app.include_router(refunds_router)