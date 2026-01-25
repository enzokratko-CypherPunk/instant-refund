param(
    [Parameter(Mandatory=$true)]
    [string]$SignerUrl
)

$apiPath = "C:\Users\brian\instant-refund-full\app\api.py"

$content = Get-Content $apiPath -Raw

$pattern = 'signer_url\s*=\s*".*"'
$replacement = "signer_url = `"$SignerUrl/sign`""

if ($content -notmatch $pattern) {
    Write-Host "ERROR: signer_url line not found in api.py" -ForegroundColor Red
    exit 1
}

$content = [regex]::Replace($content, $pattern, $replacement)
Set-Content -Path $apiPath -Value $content -Encoding UTF8

Write-Host "OK: api.py updated to use signer URL:" -ForegroundColor Green
Write-Host $SignerUrl -ForegroundColor Cyan
