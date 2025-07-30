#!/usr/bin/env python3
"""
API Routes for the LLM-Powered Intelligent Query–Retrieval System
"""

import asyncio
import aiohttp
from datetime import datetime
from typing import List, Dict, Any
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from loguru import logger

from document_parser import DocumentParser
from embedding_service_vercel import EmbeddingServiceVercel
from groq_service import GroqService
from utils import PerformanceMonitor, CacheManager

# Initialize services
document_parser = DocumentParser()
embedding_service = EmbeddingServiceVercel()
groq_service = GroqService()

# Performance monitoring
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

class SingleQueryRequest(BaseModel):
    document_url: str
    question: str

class SingleQueryResponse(BaseModel):
    answer: str
    explanation: str
    processing_time: float

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
        
        # Step 4: Format responses (answers are already in the correct format)
        
        # Step 5: Submit to webhook (async, don't wait for response)
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

async def process_single_query(
    request: SingleQueryRequest,
    token: str = Depends(get_current_user)
):
    """Process a single query for testing."""
    start_time = performance_monitor.start_timer()
    
    try:
        # Process document
        document_chunks = await document_parser.process_document_from_url(request.document_url)
        if not document_chunks:
            raise HTTPException(status_code=400, detail="Failed to process document")
        
        # Index document
        await embedding_service.index_documents(document_chunks)
        
        # Parse query
        parsed_query = await groq_service.parse_query(request.question)
        
        # Search for relevant clauses
        similar_clauses = await embedding_service.search_similar(request.question, top_k=3)
        
        if not similar_clauses:
            answer = "No relevant information found."
            explanation = "The document does not contain information related to this query."
        else:
            # Evaluate best clause
            best_clause = similar_clauses[0]["text"]
            evaluation = await groq_service.evaluate_clause(request.question, best_clause)
            
            if evaluation.get("answer", "").lower() == "yes":
                answer = evaluation.get("direct_answer", "Relevant information found.")
                explanation = evaluation.get("explanation", "Clause contains relevant information.")
            else:
                answer = "No specific answer found."
                explanation = "Document contains some relevant information but no direct answer."
        
        processing_time = performance_monitor.end_timer(start_time)
        
        return SingleQueryResponse(
            answer=answer,
            explanation=explanation,
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing single query: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

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