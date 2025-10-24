@echo off
title HireOps Quick Start

echo 🚀 HireOps Quick Start...

:: Quick check and start
if exist "venv\Scripts\python.exe" (
    echo ✅ Starting HireOps...
    start /min "" .\venv\Scripts\python.exe main.py
    timeout /t 5 /nobreak > nul
    echo 🌐 Opening in browser...
    start "" http://127.0.0.1:8000
    echo.
    echo ✅ HireOps is running at http://127.0.0.1:8000
    echo Press any key to exit this launcher...
    pause >nul
) else (
    echo ❌ Setup required. Please run "🚀_Launch_HireOps.bat" first.
    pause
)