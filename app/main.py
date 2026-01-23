from fastapi import FastAPI
from app.api import router as api_router
from app.routes.refunds import router as refunds_router

app = FastAPI()

app.include_router(api_router)
app.include_router(refunds_router)
