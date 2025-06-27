#!/usr/bin/env python3
"""
Agricultural AI System Launcher
This script helps you start the API server and frontend application
"""

import subprocess
import sys
import time
import os
import threading
import webbrowser
from pathlib import Path

def check_requirements():
    """Check if required files exist"""
    required_files = [
        "unified_api.py",
        "unified_frontend.py", 
        "Models/plant_disease_classifier_cnn.keras",
        "Models/paddy_diseases_classifier_cnn.keras",
        "Models/pest_classifier_effnetB3.keras",
        "annotations/plant_disease_classifier.csv",
        "annotations/paddy_disease_classifier.csv",
        "annotations/pest_classifier.csv"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found!")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def start_api_server():
    """Start the FastAPI server"""
    print("🚀 Starting API server...")
    try:
        # Start API server in background
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "unified_api:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
        return process
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        return None

def start_frontend():
    """Start the Streamlit frontend"""
    print("🎨 Starting Streamlit frontend...")
    try:
        # Start Streamlit in background
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", 
            "unified_frontend.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
        return process
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def wait_for_api(timeout=30):
    """Wait for API to be ready"""
    import requests
    
    print("⏳ Waiting for API to be ready...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ API is ready!")
                return True
        except:
            pass
        time.sleep(2)
    
    print("❌ API failed to start within timeout")
    return False

def open_browser():
    """Open browser tabs for API and frontend"""
    time.sleep(3)  # Wait a bit for services to fully start
    
    print("🌐 Opening browser...")
    try:
        # Open API documentation
        webbrowser.open("http://localhost:8000/docs")
        time.sleep(1)
        # Open Streamlit frontend
        webbrowser.open("http://localhost:8501")
    except Exception as e:
        print(f"⚠️ Could not open browser automatically: {e}")
        print("Please manually open:")
        print("   - API Documentation: http://localhost:8000/docs")
        print("   - Frontend Application: http://localhost:8501")

def main():
    """Main function to orchestrate the system startup"""
    print("=" * 60)
    print("🌱 Agricultural AI System Launcher")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("unified_api.py"):
        print("❌ Please run this script from the Backend directory")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ System check failed. Please ensure all required files are present.")
        sys.exit(1)
    
    # Install requirements if needed
    if os.path.exists("requirements.txt"):
        try:
            import fastapi, streamlit, tensorflow
            print("✅ Required packages already installed!")
        except ImportError:
            if not install_requirements():
                sys.exit(1)
    
    print("\n🚀 Starting system components...")
    
    # Start API server
    api_process = start_api_server()
    if not api_process:
        sys.exit(1)
    
    # Wait for API to be ready
    if not wait_for_api():
        api_process.terminate()
        sys.exit(1)
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        api_process.terminate()
        sys.exit(1)
    
    # Open browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    print("\n" + "=" * 60)
    print("✅ System started successfully!")
    print("=" * 60)
    print("🔗 Access URLs:")
    print("   📊 API Documentation: http://localhost:8000/docs")
    print("   🎨 Frontend Application: http://localhost:8501")
    print("   ❤️ API Health Check: http://localhost:8000/health")
    print("   📋 Model Information: http://localhost:8000/models/info")
    print("=" * 60)
    print("📝 Available API Endpoints:")
    print("   🌿 Plant Disease: POST /predict/plant-disease")
    print("   🌾 Paddy Disease: POST /predict/paddy-disease")
    print("   🐛 Pest Classification: POST /predict/pest")
    print("   🔀 Unified (Placeholder): POST /predict/unified")
    print("=" * 60)
    print("⚠️  Press Ctrl+C to stop all services")
    print("=" * 60)
    
    try:
        # Keep the main process alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down system...")
        
        # Terminate processes
        if api_process:
            api_process.terminate()
            print("✅ API server stopped")
        
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend stopped")
        
        print("👋 System shutdown complete!")

if __name__ == "__main__":
    main()