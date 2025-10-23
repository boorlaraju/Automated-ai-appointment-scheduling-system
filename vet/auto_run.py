#!/usr/bin/env python3
"""
Team_Vet - Auto Run Script
Comprehensive launcher for the veterinary management system
"""

import os
import sys
import subprocess
import time
import webbrowser
import threading
from pathlib import Path

# Set UTF-8 encoding for Windows compatibility
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

class TeamVetAutoRunner:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.web_interface_path = self.project_root / "web_interface"
        self.scheduling_path = self.project_root / "scheduling"
        
    def print_banner(self):
        """Print project banner"""
        print("=" * 80)
        print("🏥 TEAM_VET - AI-POWERED VETERINARY MANAGEMENT SYSTEM 🏥")
        print("=" * 80)
        print("Developed by:")
        print("1. Ramsingh B200003")
        print("2. Mahesh B200737") 
        print("3. Raju B200276")
        print("4. Nagaraju B201136")
        print("5. Santhosh B20")
        print("=" * 80)
        print()
        
    def check_python_version(self):
        """Check if Python version is compatible"""
        if sys.version_info < (3, 8):
            print("❌ Error: Python 3.8 or higher is required")
            print(f"Current version: {sys.version}")
            return False
        print(f"✅ Python version: {sys.version.split()[0]}")
        return True
        
    def install_dependencies(self):
        """Install required dependencies"""
        print("📦 Installing dependencies...")
        
        dependencies = [
            "pandas>=1.5.0",
            "numpy>=1.21.0", 
            "scikit-learn>=1.1.0",
            "joblib>=1.2.0",
            "python-dateutil>=2.8.0",
            "flask>=2.0.0",
            "flask-cors>=3.0.0"
        ]
        
        try:
            for dep in dependencies:
                print(f"Installing {dep}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep], 
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("✅ All dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing dependencies: {e}")
            return False
            
    def setup_directories(self):
        """Create necessary directories"""
        print("📁 Setting up directories...")
        
        directories = [
            "scheduling/data",
            "scheduling/data/models", 
            "inventory/data",
            "web_interface/templates"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created directory: {directory}")
            
    def train_ml_models(self):
        """Train the ML models"""
        print("🤖 Training ML models...")
        
        try:
            # Change to scheduling directory
            os.chdir(self.scheduling_path)
            
            # Run training script
            result = subprocess.run([sys.executable, "train_model.py"], 
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("✅ ML models trained successfully")
                return True
            else:
                print(f"❌ Model training failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Model training timed out")
            return False
        except Exception as e:
            print(f"❌ Error training models: {e}")
            return False
        finally:
            # Return to project root
            os.chdir(self.project_root)
            
    def start_web_server(self):
        """Start the Flask web server"""
        print("🌐 Starting web server...")
        
        try:
            # Change to web interface directory
            os.chdir(self.web_interface_path)
            
            # Start Flask app in background
            process = subprocess.Popen([sys.executable, "run_web.py"], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE)
            
            # Wait a moment for server to start
            time.sleep(3)
            
            # Check if server is running
            if process.poll() is None:
                print("✅ Web server started successfully")
                print("🌐 Opening browser...")
                
                # Open browser after delay
                def open_browser():
                    time.sleep(2)
                    webbrowser.open("http://127.0.0.1:5000")
                    
                browser_thread = threading.Thread(target=open_browser)
                browser_thread.daemon = True
                browser_thread.start()
                
                return process
            else:
                print("❌ Failed to start web server")
                return None
                
        except Exception as e:
            print(f"❌ Error starting web server: {e}")
            return None
        finally:
            # Return to project root
            os.chdir(self.project_root)
            
    def run_simple_test(self):
        """Run a simple test to verify system works"""
        print("🧪 Running system test...")
        
        try:
            os.chdir(self.scheduling_path)
            result = subprocess.run([sys.executable, "simple_test.py"], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("✅ System test passed")
                return True
            else:
                print(f"❌ System test failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error running test: {e}")
            return False
        finally:
            os.chdir(self.project_root)
            
    def show_system_info(self):
        """Show system information and status"""
        print("\n" + "=" * 80)
        print("📊 SYSTEM INFORMATION")
        print("=" * 80)
        
        # Check if models exist
        models_path = self.scheduling_path / "data" / "models"
        if models_path.exists():
            model_files = list(models_path.glob("*.pkl"))
            print(f"🤖 ML Models: {len(model_files)} files found")
        else:
            print("🤖 ML Models: Not found")
            
        # Check data files
        data_path = self.scheduling_path / "data"
        if data_path.exists():
            data_files = list(data_path.glob("*.json")) + list(data_path.glob("*.csv"))
            print(f"📊 Data Files: {len(data_files)} files found")
        else:
            print("📊 Data Files: Not found")
            
        print("\n🌐 Web Interface: http://127.0.0.1:5000")
        print("📱 Features Available:")
        print("   • AI-Powered Appointment Scheduling")
        print("   • Real-time Availability Management") 
        print("   • Inventory Management")
        print("   • Customer Service Chatbot")
        print("   • Analytics Dashboard")
        print("=" * 80)
        
    def run(self):
        """Main run method"""
        self.print_banner()
        
        # Check Python version
        if not self.check_python_version():
            return False
            
        # Install dependencies
        if not self.install_dependencies():
            return False
            
        # Setup directories
        self.setup_directories()
        
        # Run simple test first
        if not self.run_simple_test():
            print("⚠️  Simple test failed, but continuing...")
            
        # Train ML models
        if not self.train_ml_models():
            print("⚠️  ML model training failed, but continuing...")
            
        # Start web server
        server_process = self.start_web_server()
        if not server_process:
            print("❌ Failed to start web server")
            return False
            
        # Show system info
        self.show_system_info()
        
        print("\n🎉 Team_Vet system is now running!")
        print("Press Ctrl+C to stop the server")
        
        try:
            # Keep the script running
            server_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            server_process.terminate()
            print("✅ Server stopped")
            
        return True

def main():
    """Main entry point"""
    runner = TeamVetAutoRunner()
    success = runner.run()
    
    if not success:
        print("\n❌ Auto-run failed. Please check the errors above.")
        sys.exit(1)
    else:
        print("\n✅ Auto-run completed successfully!")

if __name__ == "__main__":
    main()