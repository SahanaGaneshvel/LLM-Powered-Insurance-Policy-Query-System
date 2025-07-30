#!/usr/bin/env python3
"""
Vercel-Compatible Embedding Service using simple text processing
"""

import os
import asyncio
import hashlib
from typing import List, Dict, Any, Optional
from loguru import logger
from pinecone import Pinecone, ServerlessSpec
import numpy as np

class EmbeddingServiceVercel:
    """Simplified embedding service for Vercel deployment."""
    
    def __init__(self):
        """Initialize embedding service."""
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
        
        # Simple text processing for Vercel compatibility
        logger.info("Using simplified embedding service for Vercel")
        
        # Initialize Pinecone
        if self.pinecone_api_key and self.pinecone_environment:
            try:
                self.pc = Pinecone(api_key=self.pinecone_api_key)
                self.index_name = "hackrx-index"
                self._ensure_index_exists()
                logger.info("EmbeddingServiceVercel initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Pinecone: {e}")
                self.pc = None
        else:
            logger.warning("Pinecone credentials not provided")
            self.pc = None
    
    def _ensure_index_exists(self):
        """Ensure Pinecone index exists."""
        try:
            # Check if index exists
            existing_indexes = [index.name for index in self.pc.list_indexes()]
            
            if self.index_name not in existing_indexes:
                logger.info(f"Creating index: {self.index_name}")
                # Create index with serverless spec
                self.pc.create_index(
                    name=self.index_name,
                    dimension=128,  # Smaller dimension for simple embeddings
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'
                    )
                )
                logger.info(f"Index {self.index_name} created successfully")
            else:
                logger.info(f"Index {self.index_name} already exists")
        except Exception as e:
            logger.error(f"Error ensuring index exists: {e}")
    
    def _simple_text_to_vector(self, text: str) -> List[float]:
        """Convert text to simple vector using hash-based approach."""
        # Simple hash-based embedding for Vercel compatibility
        text_hash = hashlib.md5(text.encode()).hexdigest()
        
        # Convert hash to 128-dimensional vector
        vector = []
        for i in range(0, len(text_hash), 2):
            if len(vector) >= 128:
                break
            hex_pair = text_hash[i:i+2]
            vector.append(float(int(hex_pair, 16)) / 255.0)
        
        # Pad to 128 dimensions if needed
        while len(vector) < 128:
            vector.append(0.0)
        
        return vector[:128]
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate simple embeddings for texts."""
        try:
            embeddings = []
            for text in texts:
                embedding = self._simple_text_to_vector(text)
                embeddings.append(embedding)
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return []
    
    async def index_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """Index documents in Pinecone."""
        if not self.pc:
            logger.error("Pinecone not initialized")
            return False
        
        try:
            # Generate embeddings
            texts = [doc["text"] for doc in documents]
            embeddings = self.get_embeddings(texts)
            
            if not embeddings:
                logger.error("No embeddings generated")
                return False
            
            # Prepare vectors for Pinecone
            vectors = []
            for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
                vector = {
                    "id": f"doc_{i}_{hash(doc['text'][:100])}",
                    "values": embedding,
                    "metadata": {
                        "text": doc["text"][:1000],  # Limit text length
                        "source": doc.get("source", "unknown"),
                        "timestamp": doc.get("timestamp", "")
                    }
                }
                vectors.append(vector)
            
            # Upsert to Pinecone
            index = self.pc.Index(self.index_name)
            index.upsert(vectors=vectors)
            
            logger.info(f"Indexed {len(vectors)} documents")
            return True
            
        except Exception as e:
            logger.error(f"Error indexing documents: {e}")
            return False
    
    async def search_similar(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        if not self.pc:
            logger.error("Pinecone not initialized")
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.get_embeddings([query])
            if not query_embedding:
                return []
            
            # Search in Pinecone
            index = self.pc.Index(self.index_name)
            results = index.query(
                vector=query_embedding[0],
                top_k=top_k,
                include_metadata=True
            )
            
            # Format results
            documents = []
            for match in results.matches:
                doc = {
                    "id": match.id,
                    "score": match.score,
                    "text": match.metadata.get("text", ""),
                    "source": match.metadata.get("source", ""),
                    "timestamp": match.metadata.get("timestamp", "")
                }
                documents.append(doc)
            
            return documents
            
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []
    
    async def clear_index(self) -> bool:
        """Clear all documents from index."""
        if not self.pc:
            logger.error("Pinecone not initialized")
            return False
        
        try:
            index = self.pc.Index(self.index_name)
            index.delete(delete_all=True)
            logger.info("Index cleared successfully")
            return True
        except Exception as e:
            logger.error(f"Error clearing index: {e}")
            return False
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get index statistics."""
        if not self.pc:
            return {"error": "Pinecone not initialized"}
        
        try:
            index = self.pc.Index(self.index_name)
            stats = index.describe_index_stats()
            return {
                "total_vector_count": stats.total_vector_count,
                "dimension": stats.dimension,
                "index_fullness": stats.index_fullness,
                "namespaces": stats.namespaces
            }
        except Exception as e:
            logger.error(f"Error getting index stats: {e}")
            return {"error": str(e)} 