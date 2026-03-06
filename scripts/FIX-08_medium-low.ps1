$ProjectRoot = Split-Path -Parent $PSScriptRoot
Write-Host "`n[FIX-08] Applying Medium/Low fixes..." -ForegroundColor Cyan

# CORS
$mainPath = Join-Path $ProjectRoot "app\main.py"
if (Test-Path $mainPath) {
    $c = Get-Content $mainPath -Raw
    if ($c -notmatch 'CORSMiddleware') {
        $c = "from fastapi.middleware.cors import CORSMiddleware`n" + $c
        $cors = "`n_cors = [o.strip() for o in os.environ.get('CORS_ORIGINS','').split(',') if o.strip()]`napp.add_middleware(CORSMiddleware, allow_origins=_cors, allow_credentials=True, allow_methods=['GET','POST'], allow_headers=['Authorization','Content-Type','X-API-Key'])`n"
        $c = $c -replace '(app\s*=\s*FastAPI\([^)]*\))', "`$1$cors"
        Set-Content $mainPath $c -NoNewline
        Write-Host "  [OK] CORSMiddleware added" -ForegroundColor Green
    } else { Write-Host "  [SKIP] CORSMiddleware already present" -ForegroundColor Yellow }
}

# Logging: replace print() in worker
@("app\worker.py","app\settlement\engine.py","app\services\rpc.py") | ForEach-Object {
    $p = Join-Path $ProjectRoot $_
    if (Test-Path $p) {
        $c = Get-Content $p -Raw
        if ($c -match '\bprint\(') {
            if ($c -notmatch 'import logging') { $c = "import logging`n`nlogger = logging.getLogger(__name__)`n" + $c }
            $c = $c -replace '\bprint\(', 'logger.info('
            Set-Content $p $c -NoNewline
            Write-Host "  [OK] Replaced print() in $_" -ForegroundColor Green
        }
    }
}

# raise_for_status on external calls
@("app\tools\currency_converter.py","app\tools\token_price.py","app\tools\defi_health.py","app\tools\ein_validator.py") | ForEach-Object {
    $p = Join-Path $ProjectRoot $_
    if (Test-Path $p) {
        $c = Get-Content $p -Raw
        if ($c -match '\.json\(\)' -and $c -notmatch 'raise_for_status') {
            $c = $c -replace '(\s*)(response\.json\(\))', '$1response.raise_for_status()$1$2'
            $c = $c -replace '(\s*)(r\.json\(\))', '$1r.raise_for_status()$1$2'
            Set-Content $p $c -NoNewline
            Write-Host "  [OK] Added raise_for_status() in $_" -ForegroundColor Green
        }
    }
}

# DB password redaction
$dbPath = Join-Path $ProjectRoot "app\db.py"
if (Test-Path $dbPath) {
    $c = Get-Content $dbPath -Raw
    if ($c -notmatch '_redact_url') {
        $helper = "`nimport re as _re`n`ndef _redact_url(url: str) -> str:`n    return _re.sub(r'(:)[^:@]+(@)', r'\1***\2', url)`n"
        $c = $helper + $c
        Set-Content $dbPath $c -NoNewline
        Write-Host "  [OK] Added _redact_url() to db.py" -ForegroundColor Green
    }
}

Write-Host "[FIX-08] Done.`n" -ForegroundColor Green
