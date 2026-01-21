@echo off
echo ============================================
echo   JARVIS AI Assistant - Setup Script
echo ============================================
echo.

echo [1/4] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo.
echo [2/4] Setting up Python backend...
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo [3/4] Setting up environment variables...
if not exist .env (
    copy .env.example .env
    echo Created .env file. Please edit it to add your Pinecone API key if needed.
)

cd ..

echo.
echo [4/4] Setting up Node.js frontend...
cd frontend

echo Installing Node.js dependencies...
call npm install

cd ..

echo.
echo ============================================
echo   Setup Complete! 
echo ============================================
echo.
echo Next steps:
echo.
echo 1. Install Ollama from https://ollama.ai/
echo 2. Run: ollama pull llama2
echo 3. Start Ollama: ollama serve
echo 4. Run start.bat to launch the application
echo.
pause
