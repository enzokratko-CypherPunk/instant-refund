$ProjectRoot = Split-Path -Parent $PSScriptRoot
Write-Host "`n[FIX-09] Fixing silent exception in BIN loader..." -ForegroundColor Cyan
$binPath = Join-Path $ProjectRoot "app\tools\bin_lookup.py"
if (-not (Test-Path $binPath)) { Write-Error "Not found: $binPath"; exit 1 }
$c = Get-Content $binPath -Raw
if ($c -notmatch 'import logging') { $c = "import logging`n`nlogger = logging.getLogger(__name__)`n" + $c }
$c = $c -replace '(?m)(\s*)except:\s*\r?\n\s*pass', '$1except Exception:$1    logger.exception("BIN loader failed")'
$c = $c -replace '(?m)except\s+Exception\s*:\s*pass', "except Exception:`n        logger.exception(`"BIN loader failed`")"
Set-Content $binPath $c -NoNewline
Write-Host "  [OK] Silent exception fixed in bin_lookup.py" -ForegroundColor Green
Write-Host "[FIX-09] Done.`n" -ForegroundColor Green
