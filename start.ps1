
# Activate the Python virtual environment
& "SRTFAKA\venv\Scripts\Activate.ps1"

# Check if the environment is activated
if ($?) {
    Write-Host "Virtual environment activated successfully." -ForegroundColor Green

    # Start the first server in a new PowerShell process
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& 'python' -m uvicorn SRTFAKA.apiGateway.main:app --host 0.0.0.0 --port 80"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& 'python' -m SRTFAKA.accountService.main"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& 'python' -m SRTFAKA.courseService.main"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& 'python' -m SRTFAKA.assessmentService.main"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& 'python' -m SRTFAKA.jobService.main"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& 'python' -m SRTFAKA.certificateService.main"
} else {
    Write-Host "Failed to activate the virtual environment." -ForegroundColor Red
}

Pause
