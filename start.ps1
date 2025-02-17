
# Activate the Python virtual environment
& "SkillsReadyTalentFutureAdamKhooAcademy\venv\Scripts\Activate.ps1"

# Check if the environment is activated
if ($?) {
    Write-Host "Virtual environment activated successfully." -ForegroundColor Green

    # Start the first server in a new PowerShell process
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& 'python' -m uvicorn SkillsReadyTalentFutureAdamKhooAcademy.apiGateway.main:app --host 0.0.0.0 --port 80"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& 'python' -m SkillsReadyTalentFutureAdamKhooAcademy.accountService.main"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& 'python' -m SkillsReadyTalentFutureAdamKhooAcademy.courseService.main"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& 'python' -m SkillsReadyTalentFutureAdamKhooAcademy.assessmentService.main"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& 'python' -m SkillsReadyTalentFutureAdamKhooAcademy.jobService.main"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& 'python' -m SkillsReadyTalentFutureAdamKhooAcademy.certificateService.main"
} else {
    Write-Host "Failed to activate the virtual environment." -ForegroundColor Red
}

Pause
