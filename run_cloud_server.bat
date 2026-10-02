@echo off
title BioMechAI AI Server + ngrok Cloud Launcher
color 0B
echo ======================================================================
echo           BIOMECHAI AI SERVER + NGROK CLOUD LAUNCHER
echo ======================================================================
echo.
echo [1/2] Starting FastAPI & PoseC3D v5 AI Backend Server on Port 8000...
start "BioMechAI Backend Server" cmd /k "cd /d "%~dp0" && if exist venv\Scripts\activate.bat (call venv\Scripts\activate.bat) && python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Permanent ngrok Cloud Tunnel...
echo       Public URL: https://persevere-kindred-tasty.ngrok-free.dev
start "BioMechAI ngrok Tunnel" cmd /k "ngrok http --url=persevere-kindred-tasty.ngrok-free.dev 8000"

echo.
echo ======================================================================
echo   SUCCESS: Both services are now running!
echo   ------------------------------------------------------------------
echo   Permanent Cloud URL : https://persevere-kindred-tasty.ngrok-free.dev
echo   Local Web Interface : http://localhost:8000
echo.
echo   Keep the two opened windows running in the background.
echo   To stop everything, simply close the two opened terminal windows.
echo ======================================================================
echo.
pause
