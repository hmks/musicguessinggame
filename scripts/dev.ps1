$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path "$PSScriptRoot/.."
Set-Location $repoRoot

if (Get-Command docker -ErrorAction SilentlyContinue) {
  docker compose up -d mongo
} else {
  Write-Host "Docker not found; skipping MongoDB startup."
}

if (Test-Path "api") {
  Write-Host "Starting API (FastAPI) on http://localhost:8001"
  Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd api; python -m venv .venv | Out-Null; .\\.venv\\Scripts\\Activate.ps1; pip install -r requirements.txt; uvicorn app.main:app --host 0.0.0.0 --port 8001"
}

if (Test-Path "mobile") {
  Write-Host "Starting Expo"
  Set-Location mobile
  npm install
  npx expo start
  Set-Location $repoRoot
}
