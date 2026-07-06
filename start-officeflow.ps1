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
$FrontendLog = Join-Path $Outputs "frontend.log"

$BackendCommand = "Set-Location `"$Root`"; & `"$Python`" -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 *> `"$BackendLog`""
$FrontendCommand = "Set-Location `"$Frontend`"; npm run dev *> `"$FrontendLog`""

Start-Process powershell -WindowStyle Hidden -ArgumentList "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", $BackendCommand
Start-Sleep -Seconds 2
Start-Process powershell -WindowStyle Hidden -ArgumentList "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", $FrontendCommand
Start-Sleep -Seconds 3

Start-Process "http://localhost:5173"

Write-Host "OfficeFlow is starting."
Write-Host "Frontend: http://localhost:5173"
Write-Host "Backend:  http://localhost:8000/api/health"
Write-Host "Logs:     outputs\backend.log and outputs\frontend.log"
