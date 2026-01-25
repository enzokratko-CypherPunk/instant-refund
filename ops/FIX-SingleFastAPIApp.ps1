param(
  [string]$RepoRoot = "C:\Users\brian\instant-refund-full"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-FileUtf8NoBom([string]$Path, [string]$Content) {
  $dir = Split-Path -Parent $Path
  if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }

  # Backup existing file if present
  if (Test-Path $Path) {
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    Copy-Item -Force $Path "$Path.bak-$stamp" | Out-Null
  }

  # Write UTF-8 (no BOM)
  $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($Path, $Content, $utf8NoBom)
  Write-Host "Rewrote: $Path" -ForegroundColor Green
}

$apiPath  = Join-Path $RepoRoot "app\api.py"
$mainPath = Join-Path $RepoRoot "app\main.py"

# ----------------------------
# app\api.py  (ROUTERS ONLY)
# ----------------------------
$apiContent = @"
\""\""
Routers only (NO FastAPI instance here).
Single-source-of-truth app object lives in app/main.py.

This prevents route drift where DO runs app.main:app but routes
were accidentally defined on a different FastAPI() instance.
\""\""

from fastapi import APIRouter, HTTPException
import os
import httpx

router = APIRouter()

# --- Optional configuration ---
# If SIGNER_SHARED_SECRET is set, /__debug/signer-test will attempt to call the signer.
# If it is not set, the endpoint still exists and returns a deterministic status.
SIGNER_SHARED_SECRET = os.getenv("SIGNER_SHARED_SECRET")

# NOTE: This should be the INTERNAL URL if DO provides one. If not available, leave unset.
# You can override via environment variable without code changes.
SIGNER_URL = os.getenv("SIGNER_URL")  # e.g. http://instant-refund-signer:8080/signer/sign (if internal DNS exists)

@router.get("/__debug/signer-test")
async def signer_test():
    # Endpoint ALWAYS exists. It will not disappear due to app wiring drift.
    if not SIGNER_URL:
        return {"status": "ok", "signer_call": "skipped", "reason": "SIGNER_URL not set"}

    headers = {}
    if SIGNER_SHARED_SECRET:
        headers["X-Signer-Secret"] = SIGNER_SHARED_SECRET

    body = {"message": "hello-signer"}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(SIGNER_URL, json=body, headers=headers)
        return {
            "status": "ok",
            "signer_url": SIGNER_URL,
            "http_status": resp.status_code,
            "body": resp.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signer call failed: {e}")
"@

# ----------------------------
# app\main.py  (THE ONLY FastAPI())
# ----------------------------
$mainContent = @"
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
"@

Write-FileUtf8NoBom -Path $apiPath -Content $apiContent
Write-FileUtf8NoBom -Path $mainPath -Content $mainContent

Write-Host ""
Write-Host "OK: Single FastAPI() enforced (app/main.py). Routers live in app/api.py." -ForegroundColor Cyan
Write-Host "Next: git add/commit/push to trigger DO deploy." -ForegroundColor Cyan
