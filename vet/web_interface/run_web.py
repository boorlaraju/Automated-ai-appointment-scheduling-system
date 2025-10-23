"""
Web Interface Launcher for Veterinary Scheduling System
Automatically opens in Chrome browser
"""

import os
import sys
import webbrowser
import time
import threading
from flask import Flask

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def open_browser_delayed():
    """Open browser after a short delay"""
    time.sleep(2)
    webbrowser.open('http://127.0.0.1:5000')

def main():
    """Main function to run the web interface"""
    print("=" * 60)
    print("VETERINARY SCHEDULING WEB INTERFACE")
    print("=" * 60)
    print("Starting web server...")
    print("The interface will open automatically in your browser.")
    print("If it doesn't open, go to: http://127.0.0.1:5000")
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Open browser in a separate thread
    browser_thread = threading.Thread(target=open_browser_delayed)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Import and run the Flask app
    try:
        from app import app
        app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
    except ImportError as e:
        print(f"Error importing Flask app: {e}")
        print("Make sure Flask is installed: pip install flask")
    except Exception as e:
        print(f"Error running web server: {e}")

if __name__ == "__main__":
    main()
