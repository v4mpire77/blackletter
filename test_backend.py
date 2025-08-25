#!/usr/bin/env python3
"""
Simple test script to verify Blackletter backend API is working.
"""

import httpx
import asyncio

async def test_backend():
    """Test the backend API endpoints."""
    print("🧪 Testing Blackletter Backend API...")
    
    # Test 1: Health check
    print("\n🔍 Test 1: Health check")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health", timeout=10.0)
            if response.status_code == 200:
                print("✅ Health check passed")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ Health check failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test 2: Root endpoint
    print("\n🔍 Test 2: Root endpoint")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/", timeout=10.0)
            if response.status_code == 200:
                print("✅ Root endpoint working")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ Root endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
    
    # Test 3: Compliance check
    print("\n🔍 Test 3: Compliance endpoint")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/api/v1/compliance", timeout=10.0)
            if response.status_code == 200:
                print("✅ Compliance endpoint working")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ Compliance endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Compliance endpoint failed: {e}")
    
    print("\n📋 Backend API test completed!")
    print("To test the full system, you'll need to:")
    print("1. Start the backend server: uvicorn main:app --reload")
    print("2. Start the frontend: npm run dev")
    print("3. Start Redis server")
    print("4. Set up PostgreSQL database")
    print("5. Visit http://localhost:3000 in your browser")

if __name__ == "__main__":
    asyncio.run(test_backend())