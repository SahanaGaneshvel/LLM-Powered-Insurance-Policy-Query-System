#!/usr/bin/env python3
"""
Test script to verify Vercel deployment configuration
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    try:
        import pydantic
        print("✅ Pydantic imported successfully")
    except ImportError as e:
        print(f"❌ Pydantic import failed: {e}")
        return False
    
    try:
        import groq
        print("✅ Groq imported successfully")
    except ImportError as e:
        print(f"❌ Groq import failed: {e}")
        return False
    
    try:
        import pinecone
        print("✅ Pinecone imported successfully")
    except ImportError as e:
        print(f"❌ Pinecone import failed: {e}")
        return False
    
    return True

def test_app_import():
    """Test that the main app can be imported."""
    try:
        from app import app
        print("✅ Main app imported successfully")
        return True
    except Exception as e:
        print(f"❌ Main app import failed: {e}")
        return False

def test_api_import():
    """Test that the API entry point can be imported."""
    try:
        from api.index import handler
        print("✅ API entry point imported successfully")
        return True
    except Exception as e:
        print(f"❌ API entry point import failed: {e}")
        return False

def test_environment():
    """Test environment variable validation."""
    from utils import validate_environment
    
    missing_vars = validate_environment()
    if missing_vars:
        print(f"⚠️  Missing environment variables: {missing_vars}")
        print("   These will need to be set in Vercel dashboard")
    else:
        print("✅ All required environment variables are set")
    
    return True

def test_file_structure():
    """Test that all required files exist."""
    required_files = [
        "app.py",
        "api/index.py",
        "vercel.json",
        "requirements.txt",
        "runtime.txt"
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    return True

def main():
    """Run all tests."""
    print("🧪 Testing Vercel deployment configuration...\n")
    
    tests = [
        ("File Structure", test_file_structure),
        ("Package Imports", test_imports),
        ("App Import", test_app_import),
        ("API Import", test_api_import),
        ("Environment", test_environment)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"📋 Testing {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} passed\n")
            else:
                print(f"❌ {test_name} failed\n")
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}\n")
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your project is ready for Vercel deployment.")
        return True
    else:
        print("⚠️  Some tests failed. Please fix the issues before deploying.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 