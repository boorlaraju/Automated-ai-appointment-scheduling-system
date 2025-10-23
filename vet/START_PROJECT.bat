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
echo Starting Flask web server on port 5000...
start /B python simple_app.py

echo Waiting for server to start...
timeout /t 3 /nobreak >nul

echo Starting HTML interface on port 8000...
start /B python -m http.server 8000

echo Waiting for HTML server to start...
timeout /t 2 /nobreak >nul

echo Opening browsers...
start http://127.0.0.1:5000
start http://127.0.0.1:8000/simple_interface.html

echo.
echo ============================================================
echo Team_Vet is now running!
echo ============================================================
echo.
echo Two interfaces available:
echo 1. Flask App: http://127.0.0.1:5000
echo 2. HTML Interface: http://127.0.0.1:8000/simple_interface.html
echo.
echo Features:
echo - AI-Powered Appointment Scheduling
echo - Doctor Management
echo - Real-time Dashboard
echo - Analytics and Reports
echo - Customer Service Chatbot
echo.
echo Press any key to stop all servers...
pause >nul

echo Stopping servers...
taskkill /f /im python.exe >nul 2>&1
echo All servers stopped.
