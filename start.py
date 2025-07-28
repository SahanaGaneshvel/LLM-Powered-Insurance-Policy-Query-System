#!/usr/bin/env python3
"""
Startup script for LLM-Powered Intelligent Query–Retrieval System
"""

import sys
import os
import subprocess
from dotenv import load_dotenv

def check_python_version():
    """Check if Python version is compatible."""
    print("🔍 Python Version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not supported. Please use Python 3.8+")
        return False

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Dependencies...")
    
    required_packages = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("pinecone", "pinecone"),
        ("groq", "groq"),
        ("pymupdf", "fitz"),
        ("python-docx", "docx"),
        ("aiohttp", "aiohttp"),
        ("tiktoken", "tiktoken"),
        ("loguru", "loguru"),
        ("sentence-transformers", "sentence_transformers")
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - missing")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies installed")
    return True

def check_environment():
    """Check environment variables."""
    print("🔍 Environment Variables...")
    
    load_dotenv()
    
    required_vars = [
        "GROQ_API_KEY",
        "PINECONE_API_KEY",
        "PINECONE_ENVIRONMENT"
    ]
    
    missing_vars = []
    
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var}")
        else:
            print(f"❌ {var} - not set")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️  Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("Please set these in your .env file or environment")
        print("The app will still start but may not function properly")
        return True  # Allow startup even without API keys for testing
    else:
        print("✅ All required environment variables set")
        return True

def check_api_connections():
    """Check API connections."""
    print("🔍 API Connections...")
    
    # Check Groq API
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        print("✅ Groq API key set")
    else:
        print("⚠️  Groq API key not set")
    
    # Check Pinecone
    pinecone_key = os.getenv("PINECONE_API_KEY")
    pinecone_env = os.getenv("PINECONE_ENVIRONMENT")
    
    if pinecone_key and pinecone_env:
        print("✅ Pinecone configuration complete")
    else:
        print("⚠️  Pinecone configuration incomplete")
    
    return True

def create_directories():
    """Create necessary directories."""
    print("🔍 Creating directories...")
    
    directories = ["logs", "cache", "temp"]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ {directory}/")
        except Exception as e:
            print(f"❌ Failed to create {directory}/: {e}")
            return False
    
    return True

def main():
    """Main startup function."""
    print("🔧 LLM-Powered Intelligent Query–Retrieval System Startup")
    print("=" * 60)
    
    # Run all checks
    checks = [
        check_python_version(),
        check_dependencies(),
        check_environment(),
        check_api_connections(),
        create_directories()
    ]
    
    if all(checks):
        print("✅ All checks passed! Starting server...")
        print("=" * 60)
        
        # Start the server
        try:
            subprocess.run([sys.executable, "app.py"], check=True)
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to start server: {e}")
            return False
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 