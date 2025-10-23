#!/usr/bin/env python3
"""
Team_Vet - Simple Auto Run Script
Quick launcher for the veterinary management system
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def main():
    print("=" * 60)
    print("🏥 TEAM_VET - VETERINARY MANAGEMENT SYSTEM 🏥")
    print("=" * 60)
    print("Developed by:")
    print("1. Ramsingh B200003")
    print("2. Mahesh B200737") 
    print("3. Raju B200276")
    print("4. Nagaraju B201136")
    print("5. Santhosh B20")
    print("=" * 60)
    print()
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    
    # Install basic dependencies
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "pandas", "numpy", "scikit-learn"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Dependencies installed")
    except:
        print("⚠️  Some dependencies may not have installed properly")
    
    # Setup directories
    print("📁 Setting up directories...")
    directories = ["scheduling/data", "scheduling/data/models", "inventory/data"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}")
    
    # Try to start web server
    print("🌐 Starting web server...")
    try:
        os.chdir("web_interface")
        process = subprocess.Popen([sys.executable, "run_web.py"])
        
        print("✅ Web server started!")
        print("🌐 Opening browser in 3 seconds...")
        time.sleep(3)
        webbrowser.open("http://127.0.0.1:5000")
        
        print("\n🎉 Team_Vet is now running!")
        print("📱 Access the system at: http://127.0.0.1:5000")
        print("Press Ctrl+C to stop the server")
        
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            process.terminate()
            print("✅ Server stopped")
            
    except Exception as e:
        print(f"❌ Error starting web server: {e}")
        print("💡 Try running manually: cd web_interface && python run_web.py")
        return False
    
    return True

if __name__ == "__main__":
    main()
