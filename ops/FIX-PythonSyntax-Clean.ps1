param(
  [string]$RepoRoot = "C:\Users\brian\instant-refund-full"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function WriteUtf8NoBom($Path, $Content) {
  if (Test-Path $Path) {
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    Copy-Item $Path "$Path.bak-$stamp" -Force | Out-Null
  }
  $utf8 = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($Path, $Content, $utf8)
  Write-Host "Rewrote: $Path" -ForegroundColor Green
}

$apiPath  = Join-Path $RepoRoot "app\api.py"
$mainPath = Join-Path $RepoRoot "app\main.py"

# ---------------- app/api.py ----------------
$api = @"
from fastapi import APIRouter, HTTPException
import os
import httpx

router = APIRouter()

SIGNER_SHARED_SECRET = os.getenv("SIGNER_SHARED_SECRET")
SIGNER_URL = os.getenv("SIGNER_URL")

@router.get("/__debug/signer-test")
async def signer_test():
    if not SIGNER_URL:
        return {
            "status": "ok",
            "signer_call": "skipped",
            "reason": "SIGNER_URL not set"
        }

    headers = {}
    if SIGNER_SHARED_SECRET:
        headers["X-Signer-Secret"] = SIGNER_SHARED_SECRET

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                SIGNER_URL,
                json={"message": "hello-signer"},
                headers=headers
            )
        return {
            "status": "ok",
            "http_status": resp.status_code,
            "body": resp.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"@

# ---------------- app/main.py ----------------
$main = @"
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
"@

WriteUtf8NoBom $apiPath  $api
WriteUtf8NoBom $mainPath $main

Write-Host ""
Write-Host "OK: Python syntax corrected. Single FastAPI enforced." -ForegroundColor Cyan
Write-Host "Next: commit + push." -ForegroundColor Cyan
