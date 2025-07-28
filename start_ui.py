#!/usr/bin/env python3
"""
Startup script for the Insurance Policy Query System UI
"""

import sys
import os
from pathlib import Path

def check_ui_files():
    """Check if UI files exist."""
    print("🔍 Checking UI files...")
    
    required_files = ["ui.html", "ui_server.py"]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - missing")
            return False
    
    return True

def main():
    """Main startup function."""
    print("🏥 Insurance Policy Query System UI")
    print("=" * 50)
    
    # Check UI files
    if not check_ui_files():
        print("\n❌ Missing UI files. Please ensure ui.html and ui_server.py exist.")
        return False
    
    print("\n✅ All UI files found!")
    print("\n🚀 Starting UI Server...")
    print("=" * 50)
    
    try:
        # Import and run the UI server
        from ui_server import app
        import uvicorn
        
        print("📱 UI Server starting on http://localhost:8080")
        print("🔧 API endpoint: http://localhost:8080/hackrx/run")
        print("📊 Health check: http://localhost:8080/health")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        uvicorn.run(
            "ui_server:app",
            host="0.0.0.0",
            port=8080,
            reload=True,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"\n❌ Failed to start UI server: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 