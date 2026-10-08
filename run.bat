@echo off
echo =======================================================
echo    Intelligent Timetable Optimization - Dev Server
echo =======================================================

:: Add Node.js to PATH in case it's not registered globally
set PATH=%PATH%;C:\Program Files\nodejs

echo.
echo [1/2] Starting Flask Backend (API)...
start "Flask Backend" cmd /k ".\venv\Scripts\activate && python app.py"

echo [2/2] Starting React Frontend (Vite)...
cd frontend
start "React Frontend" cmd /k "npm run dev"

echo.
echo Both servers are starting in new windows!
echo - Backend API: http://127.0.0.1:5000
echo - Frontend UI: http://localhost:5173
echo.
echo Close this window or the new windows to stop the servers.
pause
