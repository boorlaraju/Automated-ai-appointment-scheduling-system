"""
Simple HTTP Server for Veterinary Scheduling System
Opens directly in Chrome browser
"""

import http.server
import socketserver
import webbrowser
import threading
import time
import os

def open_browser():
    """Open browser after server starts"""
    time.sleep(1)
    webbrowser.open('http://127.0.0.1:8000')

def main():
    """Start the web server"""
    print("=" * 60)
    print("VETERINARY SCHEDULING WEB INTERFACE")
    print("=" * 60)
    print("Starting web server on http://127.0.0.1:8000")
    print("The interface will open automatically in your browser.")
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Change to the directory containing the HTML file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Open browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start the HTTP server
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Server running at http://127.0.0.1:{PORT}/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            httpd.shutdown()

if __name__ == "__main__":
    main()
