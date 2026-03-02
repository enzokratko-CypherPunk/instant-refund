param(
  [string]$RepoRoot = "C:\Users\brian\instant-refund\instant-refund"
)

$ErrorActionPreference = "Stop"
$sidecar = Join-Path $RepoRoot "sidecar-kaspa"
$outDir = Join-Path $RepoRoot "ops\diag"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$outFile = Join-Path $outDir ("sidecar_files_{0}.txt" -f (Get-Date -Format "yyyyMMdd_HHmmss"))

function Add-File($relative) {
  $p = Join-Path $sidecar $relative
  Add-Content -Path $outFile -Value "`n==================== FILE: $relative ====================`n"
  if (Test-Path $p) { Get-Content $p | Add-Content -Path $outFile }
  else { Add-Content -Path $outFile -Value "MISSING: $p" }
}

Add-File "src\main.rs"
Add-File "src\state.rs"
Add-File "src\http_server.rs"
Add-File "src\http.rs"
Add-File "src\settlement_key.rs"
Add-File "src\api\mod.rs"
Add-File "src\api\submit_signed.rs"
Add-File "src\kaspa\grpc_client.rs"

Write-Output $outFile
