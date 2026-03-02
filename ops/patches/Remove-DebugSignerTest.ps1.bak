# ENV: LOCAL Windows PowerShell 5.x
# Purpose: Remove /__debug/signer-test endpoint
# Method: Full-file rewrites only, .bak backups
# Safety: Streaming, no exit, no freezes

$ErrorActionPreference = "Stop"

$root = "C:\Users\brian\instant-refund\instant-refund"

if (-not (Test-Path $root)) {
  throw "Repo root not found: $root"
}

Write-Host "Repo root: $root"

$filesWithHits = @{}

Get-ChildItem -Path $root -Recurse -File | ForEach-Object {
  if (Select-String -Path $_.FullName -Pattern "/__debug/signer-test" -Quiet) {
    $filesWithHits[$_.FullName] = $true
    Write-Host "Found reference in: $($_.FullName)"
  }
}

if ($filesWithHits.Count -eq 0) {
  Write-Host "No files contain '/__debug/signer-test'. Nothing to remove."
  return
}

foreach ($file in $filesWithHits.Keys) {
  $orig = Get-Content -LiteralPath $file -Raw

  Copy-Item -LiteralPath $file -Destination ($file + ".bak") -Force

  $pattern = '(?ms)^[ \t]*@(?:app|router)\.(?:get|post|api_route)\(\s*["'']\/__debug\/signer-test["''][^\)]*\)\s*\r?\n' +
             '^[ \t]*def[ \t]+[A-Za-z_][A-Za-z0-9_]*\s*\(.*?\)\s*:\s*\r?\n' +
             '(?:^[ \t]+.*\r?\n)*'

  $updated = [regex]::Replace($orig, $pattern, "")

  if ($updated -eq $orig) {
    Write-Host "No removable handler block matched in: $file"
    continue
  }

  Set-Content -LiteralPath $file -Value $updated -NoNewline
  Write-Host "Rewrote: $file"
}

Write-Host "Debug endpoint removal complete."
