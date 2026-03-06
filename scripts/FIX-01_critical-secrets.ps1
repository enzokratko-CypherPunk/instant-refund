$ProjectRoot = Split-Path -Parent $PSScriptRoot
Write-Host "`n[FIX-01] Removing hardcoded secrets..." -ForegroundColor Cyan

$signerPath = Join-Path $ProjectRoot "app\signer_service.py"
if (-not (Test-Path $signerPath)) { Write-Warning "Not found: $signerPath" } else {
    $c = Get-Content $signerPath -Raw
    $p = '(?m)^.*SIGNER_SHARED_SECRET\s*=\s*["\x27][^"\x27]*["\x27].*$\r?\n?'
    if ($c -match $p) {
        $c = $c -replace $p, ''
        if ($c -notmatch 'from app\.core\.config import') { $c = "from app.core.config import SIGNER_SHARED_SECRET, SIGNER_URL`n" + $c }
        elseif ($c -notmatch 'SIGNER_SHARED_SECRET') { $c = $c -replace '(from app\.core\.config import[^\n]*)', '$1, SIGNER_SHARED_SECRET' }
        Set-Content $signerPath $c -NoNewline
        Write-Host "  [OK] Removed hardcoded SIGNER_SHARED_SECRET" -ForegroundColor Green
    } else { Write-Host "  [SKIP] Not found (may already be fixed)" -ForegroundColor Yellow }
}

$configPath = Join-Path $ProjectRoot "app\core\config.py"
if (-not (Test-Path $configPath)) { Write-Warning "Not found: $configPath" } else {
    $c = Get-Content $configPath -Raw
    if ($c -match 'os\.environ\.get\(["\x27]SECRET_KEY["\x27],\s*["\x27][^"\x27]*["\x27]\)') {
        $c = $c -replace 'os\.environ\.get\(["\x27]SECRET_KEY["\x27],\s*["\x27][^"\x27]*["\x27]\)', '_require_env("SECRET_KEY", secret=True)'
        Write-Host "  [OK] Replaced weak SECRET_KEY default" -ForegroundColor Green
    }
    if ($c -match 'os\.environ\.get\(["\x27]SIGNER_SHARED_SECRET["\x27],\s*["\x27][^"\x27]*["\x27]\)') {
        $c = $c -replace 'os\.environ\.get\(["\x27]SIGNER_SHARED_SECRET["\x27],\s*["\x27][^"\x27]*["\x27]\)', '_require_env("SIGNER_SHARED_SECRET", secret=True)'
        Write-Host "  [OK] Replaced weak SIGNER_SHARED_SECRET default" -ForegroundColor Green
    }
    if ($c -notmatch '_require_env') {
        $helper = "`nimport sys`n`n_FORBIDDEN_SECRETS = {`"dev_secret_key_change_me`", `"DEBUG_SHARED_SECRET_DO_NOT_KEEP`", `"secret`", `"changeme`", `"password`", `"`"}`n`ndef _require_env(name: str, *, secret: bool = False) -> str:`n    value = os.environ.get(name, `"`").strip()`n    if not value:`n        print(f`"STARTUP FAILED: Required env var '{name}' is not set.`", file=sys.stderr)`n        sys.exit(1)`n    if secret and value.lower() in _FORBIDDEN_SECRETS:`n        print(f`"STARTUP FAILED: '{name}' contains a known-weak placeholder.`", file=sys.stderr)`n        sys.exit(1)`n    return value`n"
        $c = $c -replace '(import os\r?\n)', "`$1$helper"
        Write-Host "  [OK] Injected _require_env() helper" -ForegroundColor Green
    }
    Set-Content $configPath $c -NoNewline
}
Write-Host "[FIX-01] Done.`n" -ForegroundColor Green
