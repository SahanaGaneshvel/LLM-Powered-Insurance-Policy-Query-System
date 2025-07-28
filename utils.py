#!/usr/bin/env python3
"""
Utility functions and classes for the LLM-Powered Intelligent Query–Retrieval System
"""

import os
import time
import asyncio
from typing import Dict, Any, List, Optional
from collections import defaultdict, deque
from loguru import logger
import redis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PerformanceMonitor:
    """Monitor and track system performance."""
    
    def __init__(self, max_requests: int = 1000):
        """Initialize performance monitor."""
        self.request_times = deque(maxlen=max_requests)
        self.request_count = 0
        self.error_count = 0
        self.start_time = time.time()
    
    def start_timer(self) -> float:
        """Start a performance timer."""
        return time.time()
    
    def end_timer(self, start_time: float) -> float:
        """End a performance timer and return duration."""
        duration = time.time() - start_time
        self.request_times.append(duration)
        return duration
    
    def record_request(self, duration: float):
        """Record a request duration."""
        self.request_count += 1
        self.request_times.append(duration)
    
    def record_error(self):
        """Record an error."""
        self.error_count += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        if not self.request_times:
            return {
                "total_requests": 0,
                "avg_response_time": 0,
                "min_response_time": 0,
                "max_response_time": 0,
                "error_rate": 0,
                "uptime": time.time() - self.start_time
            }
        
        times = list(self.request_times)
        return {
            "total_requests": self.request_count,
            "avg_response_time": sum(times) / len(times),
            "min_response_time": min(times),
            "max_response_time": max(times),
            "error_rate": self.error_count / max(self.request_count, 1),
            "uptime": time.time() - self.start_time
        }

class CacheManager:
    """Manage caching for improved performance."""
    
    def __init__(self):
        """Initialize cache manager."""
        self.memory_cache = {}
        self.cache_ttl = int(os.getenv("CACHE_TTL", 3600))
        
        # Initialize Redis if available
        self.redis_client = None
        redis_url = os.getenv("REDIS_URL")
        if redis_url:
            try:
                self.redis_client = redis.from_url(redis_url)
                self.redis_client.ping()
                logger.info("Redis cache initialized")
            except Exception as e:
                logger.warning(f"Redis not available: {e}")
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        # Try Redis first
        if self.redis_client:
            try:
                value = self.redis_client.get(key)
                if value:
                    return value.decode('utf-8')
            except Exception as e:
                logger.warning(f"Redis get error: {e}")
        
        # Fallback to memory cache
        if key in self.memory_cache:
            value, timestamp = self.memory_cache[key]
            if time.time() - timestamp < self.cache_ttl:
                return value
            else:
                del self.memory_cache[key]
        
        return None
    
    def set(self, key: str, value: Any, ttl: int = None):
        """Set value in cache."""
        ttl = ttl or self.cache_ttl
        
        # Try Redis first
        if self.redis_client:
            try:
                self.redis_client.setex(key, ttl, str(value))
                return
            except Exception as e:
                logger.warning(f"Redis set error: {e}")
        
        # Fallback to memory cache
        self.memory_cache[key] = (value, time.time())
    
    def clear(self):
        """Clear all cache."""
        if self.redis_client:
            try:
                self.redis_client.flushdb()
            except Exception as e:
                logger.warning(f"Redis clear error: {e}")
        
        self.memory_cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        memory_size = len(self.memory_cache)
        
        redis_size = 0
        if self.redis_client:
            try:
                redis_size = self.redis_client.dbsize()
            except Exception:
                pass
        
        return {
            "memory_cache_size": memory_size,
            "redis_cache_size": redis_size,
            "total_size": memory_size + redis_size
        }

def validate_environment() -> List[str]:
    """Validate required environment variables."""
    required_vars = [
        "GROQ_API_KEY",
        "PINECONE_API_KEY", 
        "PINECONE_ENVIRONMENT"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {missing_vars}")
    
    return missing_vars

def setup_logging():
    """Setup logging configuration."""
    logger.remove()
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="7 days",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"
    )
    logger.add(
        lambda msg: print(msg, end=""),
        level="INFO",
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

def optimize_parameters(current_latency: float, target_latency: float = 2.5) -> Dict[str, Any]:
    """Dynamically optimize system parameters based on performance."""
    if current_latency <= target_latency:
        return {
            "chunk_size": int(os.getenv("MAX_CHUNK_SIZE", 1000)),
            "top_k": int(os.getenv("TOP_K_RESULTS", 5)),
            "batch_size": int(os.getenv("BATCH_SIZE", 10))
        }
    
    # Reduce parameters to improve speed
    current_chunk_size = int(os.getenv("MAX_CHUNK_SIZE", 1000))
    current_top_k = int(os.getenv("TOP_K_RESULTS", 5))
    current_batch_size = int(os.getenv("BATCH_SIZE", 10))
    
    # Calculate reduction factor
    reduction_factor = current_latency / target_latency
    
    return {
        "chunk_size": max(500, int(current_chunk_size / reduction_factor)),
        "top_k": max(3, int(current_top_k / reduction_factor)),
        "batch_size": max(5, int(current_batch_size / reduction_factor))
    }

def batch_process(items: List[Any], batch_size: int) -> List[List[Any]]:
    """Split items into batches for processing."""
    return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]

async def parallel_process(func, items: List[Any], max_concurrent: int = 5) -> List[Any]:
    """Process items in parallel with concurrency limit."""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_item(item):
        async with semaphore:
            return await func(item)
    
    tasks = [process_item(item) for item in items]
    return await asyncio.gather(*tasks)

# Global instances
performance_monitor = PerformanceMonitor()
cache_manager = CacheManager() 