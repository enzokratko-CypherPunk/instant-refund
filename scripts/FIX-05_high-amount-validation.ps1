$ProjectRoot = Split-Path -Parent $PSScriptRoot
Write-Host "`n[FIX-05] Adding amount validation..." -ForegroundColor Cyan
$modelsPath = Join-Path $ProjectRoot "app\models.py"
if (-not (Test-Path $modelsPath)) { Write-Error "Not found: $modelsPath"; exit 1 }
$c = Get-Content $modelsPath -Raw
if ($c -notmatch 'from decimal import') { $c = "from decimal import Decimal, InvalidOperation`n" + $c; Write-Host "  [OK] Added Decimal import" -ForegroundColor Green }
if ($c -notmatch '\bvalidator\b') { $c = $c -replace '(from pydantic import[^\n]*)', '$1, validator'; Write-Host "  [OK] Added validator import" -ForegroundColor Green }
$c = $c -replace '(amount\s*:\s*)(str|float)(\s*=?\s*Field)', '$1Decimal$3'
$c = $c -replace '(amount\s*:\s*)(str|float)(\s*\n)', '$1Decimal$3'
Write-Host "  [OK] Changed amount type to Decimal" -ForegroundColor Green
if ($c -notmatch 'validate_amount') {
    $v = "`n    @validator('amount', pre=True)`n    def validate_amount(cls, v):`n        try:`n            amount = Decimal(str(v))`n        except Exception:`n            raise ValueError('amount must be a valid number')`n        if amount <= 0:`n            raise ValueError('amount must be greater than zero')`n        if amount > Decimal('1000000'):`n            raise ValueError('amount exceeds maximum allowed value')`n        return amount`n"
    $c = $c -replace '(class RefundRequest[^:]*:)', "`$1$v"
    Write-Host "  [OK] Injected validate_amount()" -ForegroundColor Green
}
Set-Content $modelsPath $c -NoNewline
Write-Host "[FIX-05] Done.`n" -ForegroundColor Green
