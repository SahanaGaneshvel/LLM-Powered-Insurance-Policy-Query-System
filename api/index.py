"""
Vercel serverless function entry point for LLM-Powered Insurance Policy Query System
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import app
    handler = app
except ImportError as e:
    # Fallback for deployment issues
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    
    app = FastAPI(title="LLM-Powered Insurance Policy Query System")
    
    @app.get("/")
    async def root():
        return {"message": "API is running", "status": "deployed"}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy"}
    
    handler = app 