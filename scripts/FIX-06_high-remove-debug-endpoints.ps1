$ProjectRoot = Split-Path -Parent $PSScriptRoot
Write-Host "`n[FIX-06] Removing debug endpoints..." -ForegroundColor Cyan
$mainPath = Join-Path $ProjectRoot "app\main.py"
if (-not (Test-Path $mainPath)) { Write-Error "Not found: $mainPath"; exit 1 }
$c = Get-Content $mainPath -Raw
$before = $c.Length
$c = [regex]::Replace($c, '(?ms)@app\.[a-z]+\(["\x27](?:/__?debug|/debug)[^"]*["\x27][^)]*\).*?(?=@app\.|\Z)', '')
$c = $c -replace '(?m)^.*include_router.*debug.*$\r?\n?', ''
if ($c.Length -lt $before) {
    Set-Content $mainPath $c -NoNewline
    Write-Host "  [OK] Debug endpoint blocks removed" -ForegroundColor Green
} else { Write-Host "  [SKIP] No debug endpoints found (may already be removed)" -ForegroundColor Yellow }
if ((Get-Content $mainPath -Raw) -match '["\x27]/__?debug|["\x27]/debug/') { Write-Warning "  [WARN] Possible debug route still present - manual review needed" }
else { Write-Host "  [OK] Verified: no debug routes remain" -ForegroundColor Green }
Write-Host "[FIX-06] Done.`n" -ForegroundColor Green
