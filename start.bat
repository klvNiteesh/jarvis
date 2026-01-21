@echo off
echo ============================================
echo   Starting JARVIS AI Assistant
echo ============================================
echo.

echo Starting Backend Server...
start "Jarvis Backend" cmd /k "cd backend && venv\Scripts\activate && python app.py"

timeout /t 3 /nobreak > nul

echo Starting Frontend Server...
start "Jarvis Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ============================================
echo   JARVIS is starting up!
echo ============================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to stop all servers...
pause > nul

echo Stopping servers...
taskkill /FI "WindowTitle eq Jarvis Backend*" /T /F
taskkill /FI "WindowTitle eq Jarvis Frontend*" /T /F
