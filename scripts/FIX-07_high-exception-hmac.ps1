$ProjectRoot = Split-Path -Parent $PSScriptRoot
Write-Host "`n[FIX-07] Sanitizing exceptions and HMAC fallback..." -ForegroundColor Cyan
$apiPath = Join-Path $ProjectRoot "app\api.py"
if (Test-Path $apiPath) {
    $c = Get-Content $apiPath -Raw
    if ($c -match 'detail\s*=\s*str\(e\)') {
        if ($c -notmatch 'import uuid') { $c = "import uuid`nimport logging`n`nlogger = logging.getLogger(__name__)`n" + $c }
        $c = $c -replace 'detail\s*=\s*str\(e\)', 'detail="An internal error occurred"'
        Set-Content $apiPath $c -NoNewline
        Write-Host "  [OK] Replaced detail=str(e) in api.py" -ForegroundColor Green
    } else { Write-Host "  [SKIP] str(e) pattern not found in api.py" -ForegroundColor Yellow }
}
$workerPath = Join-Path $ProjectRoot "app\worker.py"
if (Test-Path $workerPath) {
    $c = Get-Content $workerPath -Raw
    if ($c -match "os\.environ\.get\([`"']SIGNER_SHARED_SECRET[`"'],\s*[`"'][`"']\)") {
        $c = $c -replace "os\.environ\.get\([`"']SIGNER_SHARED_SECRET[`"'],\s*[`"'][`"']\)", "os.environ.get('SIGNER_SHARED_SECRET')"
        if ($c -notmatch 'from app\.core\.config import.*SIGNER_SHARED_SECRET') {
            $c = "from app.core.config import SIGNER_SHARED_SECRET`n" + $c
        }
        Set-Content $workerPath $c -NoNewline
        Write-Host "  [OK] Removed empty HMAC fallback in worker.py" -ForegroundColor Green
    } else { Write-Host "  [SKIP] Empty HMAC fallback not found in worker.py" -ForegroundColor Yellow }
}
Write-Host "[FIX-07] Done.`n" -ForegroundColor Green
