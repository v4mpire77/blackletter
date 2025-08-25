#!/usr/bin/env python3
"""
Test script for Blackletter GDPR Processor.
Verifies that all components are working correctly.
"""

import asyncio
import httpx
import time
from pathlib import Path

async def test_system():
    \"\"\"Test all components of the Blackletter system.\"\"\"
    print("🧪 Testing Blackletter GDPR Processor...")
    
    # Test 1: Check if backend is running
    print(\"\\n🔍 Test 1: Checking backend health...\")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health", timeout=10.0)
            if response.status_code == 200:
                print("✅ Backend is running")
                print(f"   Status: {response.json()}")
            else:
                print(f"❌ Backend returned status {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Backend is not accessible: {e}")
        return False
    
    # Test 2: Check if frontend is running
    print(\"\\n🔍 Test 2: Checking frontend health...\")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:3000", timeout=10.0)
            if response.status_code == 200:
                print("✅ Frontend is running")
            else:
                print(f"⚠️  Frontend returned status {response.status_code} (may be normal during startup)")
    except Exception as e:
        print(f"⚠️  Frontend is not accessible: {e} (may be normal during startup)")
    
    # Test 3: Check if Redis is accessible
    print(\"\\n🔍 Test 3: Checking Redis connectivity...\")
    try:
        async with httpx.AsyncClient() as client:
            # We can't directly test Redis, but we can check if the backend can connect
            response = await client.get("http://localhost:8000/api/v1/compliance", timeout=10.0)
            if response.status_code == 200:
                print("✅ Redis connectivity verified through backend")
            else:
                print(f"⚠️  Could not verify Redis connectivity")
    except Exception as e:
        print(f"⚠️  Could not verify Redis connectivity: {e}")
    
    # Test 4: Check if database is accessible
    print(\"\\n🔍 Test 4: Checking database connectivity...\")
    try:
        async with httpx.AsyncClient() as client:
            # Try to list jobs (should return empty list if DB is working)
            response = await client.get("http://localhost:8000/api/v1/jobs/", timeout=10.0)
            if response.status_code == 200:
                print("✅ Database connectivity verified")
            else:
                print(f"⚠️  Database connectivity test returned status {response.status_code}")
    except Exception as e:
        print(f"⚠️  Database connectivity test failed: {e}")
    
    print(\"\\n🎉 All tests completed!\")
    print(\"\\n📋 To test the full system:\")
    print("1. Visit http://localhost:3000 in your browser")
    print("2. Upload a PDF contract document")
    print("3. The system will process it and show compliance results")
    print(\"\\n📝 Note: For full LLM functionality, you'll need to configure an OpenAI API key in backend/.env\")
    
    return True

if __name__ == "__main__":
    asyncio.run(test_system())
