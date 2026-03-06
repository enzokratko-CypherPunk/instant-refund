$ProjectRoot = Split-Path -Parent $PSScriptRoot
Write-Host "`n[FIX-04] Adding rate limiting..." -ForegroundColor Cyan
$reqPath = Join-Path $ProjectRoot "requirements.txt"
if (Test-Path $reqPath) {
    $r = Get-Content $reqPath -Raw
    if ($r -notmatch 'slowapi') { Add-Content $reqPath "`nslowapi>=0.1.9"; Write-Host "  [OK] Added slowapi to requirements.txt" -ForegroundColor Green }
    else { Write-Host "  [SKIP] slowapi already present" -ForegroundColor Yellow }
}
$mainPath = Join-Path $ProjectRoot "app\main.py"
if (-not (Test-Path $mainPath)) { Write-Error "Not found: $mainPath"; exit 1 }
$c = Get-Content $mainPath -Raw
if ($c -notmatch 'from slowapi') {
    $imports = "from slowapi import Limiter, _rate_limit_exceeded_handler`nfrom slowapi.errors import RateLimitExceeded`nfrom slowapi.util import get_remote_address`nimport os`n"
    $c = $imports + $c
    Write-Host "  [OK] Added slowapi imports" -ForegroundColor Green
}
if ($c -notmatch 'Limiter\(') {
    $limiter = "`n_RATE_LIMIT = os.environ.get('RATE_LIMIT', '60/minute')`nlimiter = Limiter(key_func=get_remote_address, default_limits=[_RATE_LIMIT])`n"
    $c = $c -replace '(app\s*=\s*FastAPI)', "$limiter`$1"
    Write-Host "  [OK] Added Limiter instance" -ForegroundColor Green
}
if ($c -notmatch 'app\.state\.limiter') {
    $attach = "`napp.state.limiter = limiter`napp.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)`n"
    $c = $c -replace '(app\s*=\s*FastAPI\([^)]*\))', "`$1$attach"
    Write-Host "  [OK] Attached limiter to app" -ForegroundColor Green
}
Set-Content $mainPath $c -NoNewline
Write-Host "[FIX-04] Done.`n" -ForegroundColor Green
