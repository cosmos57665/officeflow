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

function Stop-ExistingOfficeFlow {
    Get-CimInstance Win32_Process |
        Where-Object {
            $_.ProcessId -ne $PID -and
            $_.CommandLine -and
            (
                ($_.CommandLine -like "*backend.main:app*" -and $_.CommandLine -like "*$Root*") -or
                ($_.CommandLine -like "*vite*" -and $_.CommandLine -like "*$Frontend*") -or
                ($_.CommandLine -like "*node*" -and $_.CommandLine -like "*$Frontend*")
            )
        } |
        ForEach-Object {
            Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
        }
}

Stop-ExistingOfficeFlow
Start-Sleep -Seconds 1

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

function Wait-ForUrl($Url, $Name) {
    for ($i = 0; $i -lt 20; $i++) {
        try {
            Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2 | Out-Null
            return
        }
        catch {
            Start-Sleep -Seconds 1
        }
    }
    Write-Host "$Name did not start. Check the log files in outputs/."
    exit 1
}

Wait-ForUrl "http://127.0.0.1:8000/api/health" "Backend"
Wait-ForUrl "http://127.0.0.1:5173" "Frontend"

Start-Process "http://localhost:5173"

Write-Host "OfficeFlow is starting."
Write-Host "Frontend: http://localhost:5173"
Write-Host "Backend:  http://localhost:8000/api/health"
Write-Host "Logs:     outputs\backend.log and outputs\frontend.log"
