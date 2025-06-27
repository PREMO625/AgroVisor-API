@echo off
echo ========================================
echo Agricultural AI System Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo Starting Agricultural AI System...
echo.

REM Run the system launcher
python run_system.py

pause