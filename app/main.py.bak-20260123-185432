\""\""
DigitalOcean entrypoint.

IMPORTANT RULE:
- FastAPI() is created ONLY here.
- app/api.py contains only routers.
\""\""

from fastapi import FastAPI

# Import routers
from app.api import router as api_router

# Existing refunds router (keep as-is if present)
try:
    from app.routes.refunds import router as refunds_router
except Exception:
    refunds_router = None

app = FastAPI()

# Mount routers
app.include_router(api_router)

if refunds_router is not None:
    app.include_router(refunds_router)