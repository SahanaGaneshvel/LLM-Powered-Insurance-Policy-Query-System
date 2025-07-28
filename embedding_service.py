#!/usr/bin/env python3
"""
Embedding Service using Groq and Pinecone
"""

import os
import asyncio
from typing import List, Dict, Any, Optional
from loguru import logger
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingService:
    """Service for managing embeddings and vector search."""
    
    def __init__(self):
        """Initialize embedding service."""
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
        
        # Initialize embedding model
        try:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            self.embedding_model = None
        
        # Initialize Pinecone
        if self.pinecone_api_key and self.pinecone_environment:
            try:
                self.pc = Pinecone(api_key=self.pinecone_api_key)
                self.index_name = "hackrx-index"
                self._ensure_index_exists()
                logger.info("EmbeddingService initialized successfully")
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
                    dimension=384,  # Sentence transformer dimension
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'  # Adjust based on your environment
                    )
                )
                logger.info(f"Index {self.index_name} created successfully")
            else:
                logger.info(f"Index {self.index_name} already exists")
        except Exception as e:
            logger.error(f"Error ensuring index exists: {e}")
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts."""
        if not self.embedding_model:
            logger.error("Embedding model not available")
            return []
        
        try:
            embeddings = self.embedding_model.encode(texts)
            return embeddings.tolist()
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
                        "text": doc["text"][:1000],  # Limit metadata size
                        "chunk_id": i,
                        "source": doc.get("source", "unknown")
                    }
                }
                vectors.append(vector)
            
            # Upsert to Pinecone
            index = self.pc.Index(self.index_name)
            index.upsert(vectors=vectors)
            
            logger.info(f"Indexed {len(vectors)} document chunks")
            return True
            
        except Exception as e:
            logger.error(f"Error indexing documents: {e}")
            return False
    
    async def search_similar(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        if not self.pc or not self.embedding_model:
            logger.error("Pinecone or embedding model not available")
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])
            
            # Search in Pinecone
            index = self.pc.Index(self.index_name)
            results = index.query(
                vector=query_embedding[0].tolist(),
                top_k=top_k,
                include_metadata=True
            )
            
            # Format results
            similar_docs = []
            for match in results.matches:
                similar_docs.append({
                    "text": match.metadata.get("text", ""),
                    "score": match.score,
                    "id": match.id
                })
            
            logger.info(f"Found {len(similar_docs)} similar documents")
            return similar_docs
            
        except Exception as e:
            logger.error(f"Error searching similar documents: {e}")
            return []
    
    async def clear_index(self) -> bool:
        """Clear all vectors from the index."""
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
                "index_fullness": stats.index_fullness
            }
        except Exception as e:
            logger.error(f"Error getting index stats: {e}")
            return {"error": str(e)} 