#!/usr/bin/env python3
"""
Test script for the LLM-Powered Intelligent Query–Retrieval System

This script demonstrates how to use the system with example requests.
"""

import requests
import json
import time
import os
from typing import Dict, List, Any

# Configuration
BASE_URL = "http://localhost:8000"
BEARER_TOKEN = "4a7809a665f2f39b1f2fa7c7073518e6baa4ebe9309eea30dae92adba5772d8c"

def test_health_check():
    """Test the health check endpoint."""
    print("🔍 Testing health check...")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed")
            print(f"   Status: {data.get('status')}")
            print(f"   Services: {len(data.get('services', {}))} initialized")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint."""
    print("\n🏠 Testing root endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print("✅ Root endpoint working")
            print(f"   Version: {data.get('version')}")
            print(f"   Status: {data.get('status')}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False

def test_hackrx_endpoint():
    """Test the main hackrx endpoint with example data."""
    print("\n🚀 Testing hackrx endpoint...")
    
    # Example request data using the provided test document
    test_data = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?",
            "Does this policy cover maternity expenses, and what are the conditions?"
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/hackrx/run",
            headers=headers,
            json=test_data,
            timeout=10
        )
        processing_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Hackrx endpoint working")
            print(f"   Processing time: {processing_time:.2f} seconds")
            print(f"   Answers returned: {len(data.get('answers', []))}")
            
            # Display first answer as example
            if data.get('answers'):
                first_answer = data['answers'][0]
                print(f"   Example answer:")
                print(f"     {first_answer[:100]}...")
            
            return True
        else:
            print(f"❌ Hackrx endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Hackrx endpoint error: {e}")
        return False

def test_single_query():
    """Test processing a single query."""
    print("\n🔍 Testing single query processing...")
    
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Test with a simple query
    test_data = {
        "query": "Is knee surgery covered?",
        "document_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/api/v1/process-single",
            headers=headers,
            json=test_data,
            timeout=10
        )
        processing_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Single query processing working")
            print(f"   Processing time: {processing_time:.2f} seconds")
            print(f"   Clauses found: {data.get('clauses_found', 0)}")
            return True
        else:
            print(f"❌ Single query processing failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Single query processing error: {e}")
        return False

def test_stats_endpoint():
    """Test the stats endpoint."""
    print("\n📊 Testing stats endpoint...")
    
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/stats", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("✅ Stats endpoint working")
            print(f"   Index stats available: {bool(data.get('index_stats'))}")
            return True
        else:
            print(f"❌ Stats endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Stats endpoint error: {e}")
        return False

def test_authentication():
    """Test authentication with invalid token."""
    print("\n🔐 Testing authentication...")
    
    headers = {
        "Authorization": "Bearer invalid-token",
        "Content-Type": "application/json"
    }
    
    test_data = {
        "documents": "https://example.com/test.pdf",
        "questions": ["Test question"]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/hackrx/run",
            headers=headers,
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 401:
            print("✅ Authentication working correctly (rejected invalid token)")
            return True
        else:
            print(f"❌ Authentication test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Authentication test error: {e}")
        return False

def run_performance_test():
    """Run a basic performance test."""
    print("\n⚡ Running performance test...")
    
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    test_data = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment?",
            "What is the waiting period for pre-existing diseases?",
            "Does this policy cover maternity expenses?"
        ]
    }
    
    times = []
    for i in range(3):
        try:
            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/hackrx/run",
                headers=headers,
                json=test_data,
                timeout=10
            )
            processing_time = time.time() - start_time
            times.append(processing_time)
            
            if response.status_code == 200:
                print(f"   Test {i+1}: {processing_time:.2f}s")
            else:
                print(f"   Test {i+1}: Failed ({response.status_code})")
                
        except Exception as e:
            print(f"   Test {i+1}: Error - {e}")
    
    if times:
        avg_time = sum(times) / len(times)
        print(f"   Average processing time: {avg_time:.2f}s")
        
        if avg_time <= 3.0:
            print("✅ Performance target met (≤3s)")
        else:
            print("⚠️  Performance target exceeded (>3s)")

def main():
    """Run all tests."""
    print("🧪 LLM-Powered Intelligent Query–Retrieval System Test Suite")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not running. Please start the server first:")
            print("   python app.py")
            return
    except Exception:
        print("❌ Cannot connect to server. Please start the server first:")
        print("   python app.py")
        return
    
    # Run tests
    tests = [
        ("Health Check", test_health_check),
        ("Root Endpoint", test_root_endpoint),
        ("Authentication", test_authentication),
        ("Hackrx Endpoint", test_hackrx_endpoint),
        ("Single Query", test_single_query),
        ("Stats Endpoint", test_stats_endpoint),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    # Performance test
    run_performance_test()
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the logs for details.")
    
    print("\n📝 Next steps:")
    print("   1. Review the API documentation at http://localhost:8000/docs")
    print("   2. Test with your own documents and questions")
    print("   3. Monitor performance and adjust configuration as needed")

if __name__ == "__main__":
    main() 