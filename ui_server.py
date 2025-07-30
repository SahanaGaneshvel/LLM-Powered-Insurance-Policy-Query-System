#!/usr/bin/env python3
"""
Simple UI Server for Insurance Policy Query System
"""

import os
import asyncio
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from loguru import logger
import aiohttp
from datetime import datetime

# Import your existing services
from document_parser import DocumentParser
from embedding_service_vercel import EmbeddingServiceVercel
from groq_service_vercel import GroqServiceVercel
from utils import PerformanceMonitor, CacheManager

# Initialize FastAPI app
app = FastAPI(
    title="Insurance Policy Query System UI",
    description="Web interface for the LLM-Powered Insurance Policy Query System",
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

# Initialize services
document_parser = DocumentParser()
embedding_service = EmbeddingServiceVercel()
groq_service = GroqServiceVercel()
performance_monitor = PerformanceMonitor()
cache_manager = CacheManager()

# Security
security = HTTPBearer()

# Pydantic models
class HackrxRequest(BaseModel):
    documents: str
    questions: List[str]

class HackrxResponse(BaseModel):
    answers: List[str]

# Authentication
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Validate API key."""
    api_key = credentials.credentials
    expected_key = "4a7809a665f2f39b1f2fa7c7073518e6baa4ebe9309eea30dae92adba5772d8c"
    
    if api_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return api_key

async def submit_to_webhook(results: List[str]) -> bool:
    """Submit results to webhook endpoint."""
    try:
        webhook_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "answers": results
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://webhook-endpoint.com/api/v1/hackrx/run",
                json=webhook_data,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "LLM-Powered-Insurance-System/1.0"
                },
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    logger.info("Webhook submission successful")
                    return True
                else:
                    logger.warning(f"Webhook submission failed: {response.status}")
                    return False
    except Exception as e:
        logger.error(f"Webhook submission error: {e}")
        return False

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    """Serve the main UI."""
    return FileResponse("ui.html")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Insurance Policy Query System UI",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/hackrx/run", response_model=HackrxResponse)
async def hackrx_run(
    request: HackrxRequest,
    token: str = Depends(get_current_user)
):
    """Main endpoint for processing insurance policy queries."""
    start_time = performance_monitor.start_timer()
    
    try:
        # Step 1: Parse and index document
        logger.info(f"Processing document from URL: {request.documents}")
        document_chunks = await document_parser.process_document_from_url(request.documents)
        
        if not document_chunks:
            raise HTTPException(status_code=400, detail="Failed to process document")
        
        # Step 2: Index document chunks
        logger.info(f"Indexing {len(document_chunks)} document chunks")
        indexing_success = await embedding_service.index_documents(document_chunks)
        
        if not indexing_success:
            raise HTTPException(status_code=500, detail="Failed to index document")
        
        # Step 3: Process each question
        answers = []
        for question in request.questions:
            # Parse query
            parsed_query = await groq_service.parse_query(question)
            
            # Search for relevant clauses
            similar_clauses = await embedding_service.search_similar(question, top_k=5)
            
            if not similar_clauses:
                answer = "No relevant information found in the document."
            else:
                # Get relevant texts
                relevant_texts = [clause["text"] for clause in similar_clauses]
                
                # Generate detailed answer
                answer = await groq_service.generate_detailed_answer(question, relevant_texts)
            
            answers.append(answer)
        
        # Step 4: Submit to webhook (async, don't wait for response)
        webhook_task = asyncio.create_task(submit_to_webhook(answers))
        
        # Record performance
        processing_time = performance_monitor.end_timer(start_time)
        performance_monitor.record_request(processing_time)
        
        logger.info(f"Processed {len(request.questions)} questions in {processing_time:.2f}s")
        
        # Return results in required format
        return HackrxResponse(answers=answers)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/stats")
async def get_stats():
    """Get system statistics."""
    try:
        index_stats = embedding_service.get_index_stats()
        performance_stats = performance_monitor.get_stats()
        
        return {
            "index_stats": index_stats,
            "performance_stats": performance_stats,
            "cache_stats": cache_manager.get_stats()
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving statistics")

@app.delete("/api/v1/clear-index")
async def clear_index(token: str = Depends(get_current_user)):
    """Clear the vector index."""
    try:
        success = await embedding_service.clear_index()
        if success:
            return {"message": "Index cleared successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to clear index")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error clearing index: {e}")
        raise HTTPException(status_code=500, detail="Error clearing index")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Insurance Policy Query System UI Server...")
    print("📱 Open your browser and go to: http://localhost:8080")
    print("🔧 API endpoint: http://localhost:8080/hackrx/run")
    print("📊 Health check: http://localhost:8080/health")
    print("=" * 60)
    
    uvicorn.run(
        "ui_server:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    ) 