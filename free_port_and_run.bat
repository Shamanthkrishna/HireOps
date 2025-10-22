@echo off
echo 🔍 Checking what's using port 8000...
netstat -ano | findstr :8000

echo.
echo 🛑 Attempting to free port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Found process ID: %%a
    taskkill /F /PID %%a 2>nul
)

echo.
echo ✅ Port should now be free. Starting HireOps...
cd /d "D:\SKB\Courses\Adarsh Project\HireOps\app"
python main_simple.py

pause
