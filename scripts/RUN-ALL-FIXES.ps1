param(
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot),
    [switch]$SkipBackup
)
$ErrorActionPreference = "Stop"
$ScriptsDir = $PSScriptRoot

Write-Host "`nINSTANT REFUND - Security Audit Remediation" -ForegroundColor Cyan
Write-Host "Fixes: 3 Critical + 7 High + 5 Medium + 4 Low`n" -ForegroundColor Cyan

$required = @("app\main.py","app\core\config.py","app\signer_service.py","app\routes\refunds.py","app\models.py","requirements.txt")
$missing = $required | Where-Object { -not (Test-Path (Join-Path $ProjectRoot $_)) }
if ($missing) {
    Write-Warning "Missing files (will be skipped):"
    $missing | ForEach-Object { Write-Warning "  $_" }
    $ok = Read-Host "Continue anyway? (y/N)"
    if ($ok -ne 'y') { exit 0 }
}

if (-not $SkipBackup) {
    $ts = Get-Date -Format "yyyyMMdd_HHmmss"
    $bk = Join-Path $ProjectRoot "security-backup_$ts"
    New-Item -ItemType Directory -Path $bk -Force | Out-Null
    $required | ForEach-Object {
        $src = Join-Path $ProjectRoot $_
        if (Test-Path $src) {
            $dst = Join-Path $bk $_
            New-Item -ItemType Directory -Path (Split-Path $dst -Parent) -Force | Out-Null
            Copy-Item $src $dst
        }
    }
    Write-Host "Backup saved: $bk" -ForegroundColor Green
}

$fixes = New-Object System.Collections.ArrayList
[void]$fixes.Add(@{F="FIX-01_critical-secrets.ps1";          L="CRITICAL 1+2 - Hardcoded secrets"})
[void]$fixes.Add(@{F="FIX-02_critical-hardcoded-ip.ps1";      L="CRITICAL 3   - Hardcoded Kaspa IP"})
[void]$fixes.Add(@{F="FIX-03_high-auth.ps1";                  L="HIGH 4       - API key auth"})
[void]$fixes.Add(@{F="FIX-04_high-rate-limiting.ps1";         L="HIGH 5       - Rate limiting"})
[void]$fixes.Add(@{F="FIX-05_high-amount-validation.ps1";     L="HIGH 6+10    - Amount validation"})
[void]$fixes.Add(@{F="FIX-06_high-remove-debug-endpoints.ps1";L="HIGH 7       - Remove debug endpoints"})
[void]$fixes.Add(@{F="FIX-07_high-exception-hmac.ps1";        L="HIGH 8+9     - Exception sanitization"})
[void]$fixes.Add(@{F="FIX-08_medium-low.ps1";                 L="MEDIUM+LOW   - CORS, logging, caches"})
[void]$fixes.Add(@{F="FIX-09_low-bin-silent-exception.ps1";   L="LOW 19       - BIN loader exception"})

$results = @()
foreach ($fix in $fixes) {
    $sp = Join-Path $ScriptsDir $fix.F
    Write-Host "`n--- $($fix.L) ---" -ForegroundColor Magenta
    if (-not (Test-Path $sp)) {
        Write-Warning "Script not found: $sp"
        $results += [PSCustomObject]@{Fix=$fix.L; Status="MISSING"}
        continue
    }
    try {
        & $sp
        $results += [PSCustomObject]@{Fix=$fix.L; Status="OK"}
    } catch {
        Write-Error "FAILED: $_"
        $results += [PSCustomObject]@{Fix=$fix.L; Status="FAILED"}
    }
}

Write-Host "`n=== SUMMARY ===" -ForegroundColor Cyan
$results | Format-Table -AutoSize

Write-Host "`nNext: run SET-DO-ENV-VARS.ps1 to set secrets in DigitalOcean" -ForegroundColor Yellow
