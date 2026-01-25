$ErrorActionPreference = "Stop"

$root = "C:\Users\brian\instant-refund-full"
Set-Location $root

$apiPath    = Join-Path $root "app\api.py"
$signerPath = Join-Path $root "app\signer_service.py"

if (!(Test-Path $apiPath))    { throw "Missing file: $apiPath" }
if (!(Test-Path $signerPath)) { throw "Missing file: $signerPath" }

$debugSecret = "DEBUG_SHARED_SECRET_DO_NOT_KEEP"

function Rewrite-FileWithReplacements {
  param(
    [Parameter(Mandatory=$true)][string]$Path,
    [Parameter(Mandatory=$true)][hashtable]$Replacements,
    [Parameter(Mandatory=$true)][string]$Label
  )

  $orig = Get-Content -Raw -Encoding UTF8 $Path
  $new  = $orig

  foreach ($k in $Replacements.Keys) {
    $pattern = $k
    $replacement = $Replacements[$k]

    $before = $new
    $new = [regex]::Replace(
      $new,
      $pattern,
      $replacement,
      [System.Text.RegularExpressions.RegexOptions]::Singleline
    )

    if ($before -eq $new) {
      Write-Host "----" -ForegroundColor Yellow
      Write-Host ("FAILED to match pattern in {0}: {1}" -f $Label, $pattern) -ForegroundColor Yellow
      Write-Host "Showing SIGNER-related lines from file:" -ForegroundColor Yellow
      Select-String -Path $Path -Pattern "SIGNER|signer|x-signer|secret" |
        ForEach-Object { $_.Line } |
        Select-Object -First 50
      throw "Replacement did not apply for $Label"
    }
  }

  Set-Content -Path $Path -Value $new -Encoding UTF8
  Write-Host "Rewrote: $Path" -ForegroundColor Green
}

# ---- API replacement
$apiReplacements = @{
  'SIGNER_SHARED_SECRET\s*=\s*os\.getenv\(\s*["'']SIGNER_SHARED_SECRET["'']\s*\)\s*\r?\n\s*if\s+not\s+SIGNER_SHARED_SECRET\s*:\s*\r?\n\s*raise\s+RuntimeError\(\s*["'']SIGNER_SHARED_SECRET not set["'']\s*\)\s*' =
  "SIGNER_SHARED_SECRET = `"$debugSecret`"`n"
}

Rewrite-FileWithReplacements -Path $apiPath -Replacements $apiReplacements -Label "API (app\\api.py)"

# ---- SIGNER replacement
$signerReplacements = @{
  'SIGNER_SHARED_SECRET\s*=\s*os\.getenv\(\s*["'']SIGNER_SHARED_SECRET["'']\s*\)\s*' =
  "SIGNER_SHARED_SECRET = `"$debugSecret`"`n"
}

Rewrite-FileWithReplacements -Path $signerPath -Replacements $signerReplacements -Label "SIGNER (app\\signer_service.py)"

Write-Host "`nOK: hardcoded debug secret into BOTH API + SIGNER." -ForegroundColor Cyan
Write-Host "Next: commit + push." -ForegroundColor Cyan
