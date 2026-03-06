$ProjectRoot = Split-Path -Parent $PSScriptRoot
Write-Host "`n[FIX-02] Removing hardcoded Kaspa node IP..." -ForegroundColor Cyan
$configPath = Join-Path $ProjectRoot "app\core\config.py"
if (-not (Test-Path $configPath)) { Write-Error "Not found: $configPath"; exit 1 }
$c = Get-Content $configPath -Raw
if ($c -match 'os\.environ\.get\(["\x27]KASPA_RPC_HOST["\x27],\s*["\x27][^"\x27]*["\x27]\)') {
    $c = $c -replace 'os\.environ\.get\(["\x27]KASPA_RPC_HOST["\x27],\s*["\x27][^"\x27]*["\x27]\)', '_require_env("KASPA_RPC_HOST")'
    Set-Content $configPath $c -NoNewline
    Write-Host "  [OK] Replaced hardcoded KASPA_RPC_HOST" -ForegroundColor Green
} else { Write-Host "  [SKIP] Not found (may already be fixed)" -ForegroundColor Yellow }
if ((Get-Content $configPath -Raw) -match '159\.203\.168\.9') { Write-Warning "  [WARN] Hardcoded IP still present - manual review needed" }
else { Write-Host "  [OK] Verified: no hardcoded IP remains" -ForegroundColor Green }
Write-Host "[FIX-02] Done.`n" -ForegroundColor Green
