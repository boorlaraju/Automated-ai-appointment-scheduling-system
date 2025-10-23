@echo off
echo ============================================================
echo TEAM_VET - VETERINARY MANAGEMENT SYSTEM
echo ============================================================
echo Developed by:
echo 1. Ramsingh B200003
echo 2. Mahesh B200737
echo 3. Raju B200276
echo 4. Nagaraju B201136
echo 5. Santhosh B20
echo ============================================================
echo.
echo Starting Team_Vet system...
echo.

cd web_interface
echo Starting Flask web server...
start /B python simple_app.py

echo Waiting for server to start...
timeout /t 5 /nobreak >nul

echo Opening browser...
start http://127.0.0.1:5000

echo.
echo ============================================================
echo Team_Vet is now running!
echo Web Interface: http://127.0.0.1:5000
echo ============================================================
echo.
echo Features available:
echo - AI-Powered Appointment Scheduling
echo - Doctor Management
echo - Real-time Dashboard
echo - Analytics and Reports
echo - Customer Service Chatbot
echo.
echo Press any key to stop the server...
pause >nul

echo Stopping server...
taskkill /f /im python.exe >nul 2>&1
echo Server stopped.
