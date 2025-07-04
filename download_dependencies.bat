@echo off
echo === Cropperview Dependency Downloader ===
echo This script will download the required executables for Cropperview.
echo.

REM Check if PowerShell is available
powershell -Command "Get-Host" >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: PowerShell is required to download dependencies.
    echo Please install PowerShell or download dependencies manually.
    pause
    exit /b 1
)

REM Run the PowerShell script
echo Running dependency downloader...
powershell -ExecutionPolicy Bypass -File "download_dependencies.ps1"

echo.
echo Setup complete! Check the output above for status.
pause 