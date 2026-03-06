$ProjectRoot = Split-Path -Parent $PSScriptRoot
Write-Host "`n[FIX-03] Adding API key authentication..." -ForegroundColor Cyan
$refundsPath = Join-Path $ProjectRoot "app\routes\refunds.py"
if (-not (Test-Path $refundsPath)) { Write-Error "Not found: $refundsPath"; exit 1 }
$c = Get-Content $refundsPath -Raw
if ($c -notmatch 'require_api_key') {
    $authDep = "`nimport secrets`nfrom typing import Optional`nfrom fastapi import Header, HTTPException, status`n`nasync def require_api_key(x_api_key: Optional[str] = Header(None)) -> str:`n    valid_keys = [k.strip() for k in os.environ.get('API_KEYS','').split(',') if k.strip()]`n    if not x_api_key:`n        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Missing X-API-Key header')`n    for vk in valid_keys:`n        if secrets.compare_digest(x_api_key.strip(), vk):`n            return x_api_key.strip()`n    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid API key')`n"
    $c = $authDep + $c
    if ($c -notmatch 'import os') { $c = "import os`n" + $c }
    Set-Content $refundsPath $c -NoNewline
    Write-Host "  [OK] Injected require_api_key() into $refundsPath" -ForegroundColor Green
    Write-Host "  ACTION: Add Depends(require_api_key) to each route function manually" -ForegroundColor Yellow
} else { Write-Host "  [SKIP] require_api_key already present" -ForegroundColor Yellow }
Write-Host "[FIX-03] Done.`n" -ForegroundColor Green
