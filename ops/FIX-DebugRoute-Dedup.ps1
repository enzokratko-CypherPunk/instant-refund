$path = "app\main.py"
$content = Get-Content $path -Raw

# Remove any __debug route definitions from main.py
$content = [regex]::Replace(
    $content,
    '@app\.get\("/__debug/signer-test"\)[\s\S]*?\n\n',
    '',
    'Singleline'
)

Set-Content -Path $path -Value $content -Encoding UTF8
Write-Host "OK: Removed __debug route from main.py" -ForegroundColor Green
