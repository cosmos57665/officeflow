$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Outputs = Join-Path $Root "outputs"
$Frontend = Join-Path $Root "frontend"
$Python = Join-Path $Root "venv\Scripts\python.exe"

if (!(Test-Path $Outputs)) {
    New-Item -ItemType Directory -Path $Outputs | Out-Null
}

if (!(Test-Path $Python)) {
    $Python = "python"
}

$BackendLog = Join-Path $Outputs "backend.log"
$BackendErr = Join-Path $Outputs "backend.err.log"
$FrontendLog = Join-Path $Outputs "frontend.log"
$FrontendErr = Join-Path $Outputs "frontend.err.log"

Start-Process -FilePath $Python `
    -ArgumentList @("-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000") `
    -WorkingDirectory $Root `
    -RedirectStandardOutput $BackendLog `
    -RedirectStandardError $BackendErr `
    -WindowStyle Hidden
Start-Sleep -Seconds 2
$Npm = "npm.cmd"
Start-Process -FilePath $Npm `
    -ArgumentList @("run", "dev") `
    -WorkingDirectory $Frontend `
    -RedirectStandardOutput $FrontendLog `
    -RedirectStandardError $FrontendErr `
    -WindowStyle Hidden
Start-Sleep -Seconds 3

Start-Process "http://localhost:5173"

Write-Host "OfficeFlow is starting."
Write-Host "Frontend: http://localhost:5173"
Write-Host "Backend:  http://localhost:8000/api/health"
Write-Host "Logs:     outputs\backend.log and outputs\frontend.log"
