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
echo Starting web server on port 8000...
start /B python -m http.server 8000

echo Waiting for server to start...
timeout /t 3 /nobreak >nul

echo Opening browser...
start http://127.0.0.1:8000/simple_interface.html

echo.
echo ============================================================
echo Team_Vet is now running!
echo Web Interface: http://127.0.0.1:8000/simple_interface.html
echo ============================================================
echo.
echo Press any key to stop the server...
pause >nul

echo Stopping server...
taskkill /f /im python.exe >nul 2>&1
echo Server stopped.
