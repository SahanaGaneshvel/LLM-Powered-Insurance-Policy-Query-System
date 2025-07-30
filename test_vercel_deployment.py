#!/usr/bin/env python3
"""
Test script to verify Vercel deployment imports
"""

def test_imports():
    """Test that all imports work correctly."""
    try:
        print("Testing imports...")
        
        # Test Vercel-compatible imports
        from embedding_service_vercel import EmbeddingServiceVercel
        from groq_service_vercel import GroqServiceVercel
        from document_parser import DocumentParser
        from utils import PerformanceMonitor, CacheManager
        
        print("✅ All Vercel-compatible imports successful")
        
        # Test service initialization
        embedding_service = EmbeddingServiceVercel()
        groq_service = GroqServiceVercel()
        document_parser = DocumentParser()
        performance_monitor = PerformanceMonitor()
        cache_manager = CacheManager()
        
        print("✅ All services initialized successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("🎉 All tests passed! Ready for Vercel deployment.")
    else:
        print("❌ Tests failed. Check imports.") 