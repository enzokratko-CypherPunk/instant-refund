# FIX-Internal-SignerURL.ps1
# ENV: LOCAL WINDOWS POWERSHELL

$root = "C:\Users\brian\instant-refund-full"
$apiPath = Join-Path $root "app\api.py"

if (-not (Test-Path $apiPath)) {
    Write-Host "ERROR: api.py not found at $apiPath" -ForegroundColor Red
    exit 1
}

$content = Get-Content $apiPath -Raw

$pattern = 'signer_url\s*=\s*".*?"'
$replacement = 'signer_url = "http://instant-refund-signer:8080/signer/sign"'

if ($content -notmatch $pattern) {
    Write-Host "ERROR: signer_url assignment not found in api.py" -ForegroundColor Red
    exit 1
}

$content = [regex]::Replace($content, $pattern, $replacement)
Set-Content -Path $apiPath -Value $content -Encoding UTF8

Write-Host "OK: signer_url set to internal DO service" -ForegroundColor Green
Write-Host "http://instant-refund-signer:8080/signer/sign" -ForegroundColor Cyan
