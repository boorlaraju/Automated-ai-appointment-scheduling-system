@echo off
echo ============================================================
echo VETERINARY SCHEDULING WEB INTERFACE
echo ============================================================
echo Starting web server...
echo The interface will open automatically in your browser.
echo If it doesn't open, go to: http://127.0.0.1:5000
echo ============================================================
echo Press Ctrl+C to stop the server
echo ============================================================

cd /d "%~dp0web_interface"
python run_web.py

pause
