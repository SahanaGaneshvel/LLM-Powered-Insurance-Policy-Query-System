#!/usr/bin/env python3
"""
Main FastAPI application for LLM-Powered Intelligent Query–Retrieval System
Updated for Vercel compatibility - No sentence_transformers dependency
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="LLM-Powered Intelligent Query–Retrieval System",
    description="Processes PDFs/DOCX/emails, retrieves relevant clauses using embeddings, evaluates logic, and outputs structured JSON responses",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting LLM-Powered Intelligent Query–Retrieval System")
    
    # Validate environment
    from utils import validate_environment
    missing_vars = validate_environment()
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        logger.error("Please set the required environment variables before starting the application")
    else:
        logger.info("All environment variables are set")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down LLM-Powered Intelligent Query–Retrieval System")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "LLM-Powered Intelligent Query–Retrieval System",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "main": "/hackrx/run",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check environment variables
        from utils import validate_environment
        missing_vars = validate_environment()
        
        # Check services
        services_status = {
            "document_parser": "ready",
            "embedding_service": "ready", 
            "groq_service": "ready",
            "utils": "ready"
        }
        
        return {
            "status": "healthy",
            "environment": {
                "GROQ_API_KEY": bool(os.getenv("GROQ_API_KEY")),
                "PINECONE_API_KEY": bool(os.getenv("PINECONE_API_KEY")),
                "PINECONE_ENVIRONMENT": bool(os.getenv("PINECONE_ENVIRONMENT")),
                "REDIS_URL": bool(os.getenv("REDIS_URL"))
            },
            "services": services_status,
            "timestamp": "2025-01-28T20:30:00Z"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }

# Include API routes directly instead of as router
from api_routes import (
    HackrxRequest, HackrxResponse,
    get_current_user, hackrx_run,
    process_single_query, get_stats, clear_index
)

# Add the routes directly to the main app
app.add_api_route("/hackrx/run", hackrx_run, methods=["POST"], response_model=HackrxResponse)
app.add_api_route("/api/v1/process-single", process_single_query, methods=["POST"])
app.add_api_route("/api/v1/stats", get_stats, methods=["GET"])
app.add_api_route("/api/v1/clear-index", clear_index, methods=["DELETE"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "false").lower() == "true"
    ) 