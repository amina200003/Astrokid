#!/usr/bin/env python3
"""
AstroKid Launcher Script
This script checks dependencies and launches the AstroKid Streamlit application.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'google-generativeai',
        'duckduckgo-search',
        'python-dotenv',
        'requests',
        'beautifulsoup4'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Installing missing packages...")
        
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please run:")
            print(f"   pip install {' '.join(missing_packages)}")
            return False
    
    return True

def check_api_key():
    """Check if API key is configured"""
    env_file = Path('api.env')
    
    if not env_file.exists():
        print("❌ api.env file not found!")
        print("📝 Please create api.env file with your Gemini API key:")
        print("   GEMINI_API_KEY=your_api_key_here")
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
        if 'GEMINI_API_KEY=' not in content or 'your_api_key_here' in content:
            print("❌ Please set your Gemini API key in api.env file")
            return False
    
    print("✅ API key configured")
    return True

def main():
    """Main launcher function"""
    print("🚀 AstroKid Launcher")
    print("=" * 30)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check API key
    if not check_api_key():
        return
    
    print("\n🎯 Starting AstroKid...")
    print("🌐 The app will open in your browser at http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("-" * 30)
    
    try:
        # Run the Streamlit app
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'astrokid_app.py'])
    except KeyboardInterrupt:
        print("\n👋 AstroKid stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error running AstroKid: {e}")

if __name__ == "__main__":
    main()
