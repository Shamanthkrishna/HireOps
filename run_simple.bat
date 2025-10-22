@echo off
echo 🚀 Starting HireOps Simple Version...
echo.

cd /d "D:\SKB\Courses\Adarsh Project\HireOps\app"

echo 📦 Checking dependencies...
python -c "import fastapi; print('✅ FastAPI available')" 2>nul || (
    echo ❌ FastAPI not found, installing...
    pip install fastapi uvicorn[standard]
)

echo 🌐 Starting application...
echo.
echo 🔗 Once started, visit: http://localhost:8001
echo 🔗 Or try: http://localhost:8002
echo.
echo ⏹️  Press Ctrl+C to stop the server
echo.

python main_simple.py

pause
