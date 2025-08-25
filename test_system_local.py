#!/usr/bin/env python3
"""
Test script for Blackletter GDPR Processor (Local Testing Version).
Verifies that the core components are working correctly without external dependencies.
"""

import asyncio
import httpx
import os
import sys
from pathlib import Path

async def test_system_local():
    """Test the Blackletter system with minimal dependencies."""
    print("Testing Blackletter GDPR Processor (Local Version)...")
    
    # Create a simple test file
    test_content = """
    DATA PROCESSING AGREEMENT
    
    This agreement outlines the data processing obligations between parties.
    Personal data will be processed in accordance with GDPR requirements.
    The processor shall implement appropriate technical and organizational measures.
    """
    
    test_file_path = Path("test_contract.txt")
    test_file_path.write_text(test_content)
    
    try:
        # Test 1: Check if we can import the main backend modules
        print("\nTest 1: Checking backend module imports...")
        try:
            # Try to import key modules
            from backend.main import app
            from backend.models import Document, AnalysisResult
            from backend.utils import analyze_contract
            print("Backend modules imported successfully")
        except Exception as e:
            print(f"Backend module import test: {e}")
        
        # Test 2: Check if we can run the analysis function directly
        print("\nTest 2: Testing contract analysis function...")
        try:
            # Add backend to path
            sys.path.append("backend")
            from utils import analyze_contract
            result = analyze_contract(test_content)
            print("Contract analysis function works")
            print(f"   Sample result: {result.get('compliance_issues', [{}])[0] if result.get('compliance_issues') else 'No issues found'}")
            print(f"   Compliance score: {result.get('summary', {}).get('compliance_score', 0) * 100:.1f}%")
        except Exception as e:
            print(f"Contract analysis test: {e}")
        
        # Test 3: Check frontend build
        print("\nTest 3: Checking frontend build...")
        try:
            # Check if the frontend build directory exists
            build_dir = Path("frontend/.next")
            if build_dir.exists():
                print("Frontend is built")
            else:
                print("Frontend is not built yet")
        except Exception as e:
            print(f"Frontend build check: {e}")
            
        # Test 4: Check if required environment variables are set
        print("\nTest 4: Checking environment variables...")
        required_vars = ["OPENAI_API_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if not missing_vars:
            print("All required environment variables are set")
        else:
            print(f"Missing environment variables: {missing_vars}")
            print("   Note: For full LLM functionality, you'll need to set OPENAI_API_KEY")
            
        # Test 5: Check file processing
        print("\nTest 5: Testing file processing...")
        try:
            # Simulate file processing
            with open(test_file_path, "r") as f:
                content = f.read()
                print(f"File reading works, content length: {len(content)} characters")
        except Exception as e:
            print(f"File processing test failed: {e}")
            
    finally:
        # Cleanup
        if test_file_path.exists():
            test_file_path.unlink()
    
    print("\nLocal tests completed!")
    print("\nTo test the full system:")
    print("1. Install Redis and PostgreSQL, or use Docker")
    print("2. Set up environment variables in backend/.env")
    print("3. Run the backend: uvicorn backend.main:app --reload")
    print("4. Run the frontend: cd frontend && npm run dev")
    print("5. Visit http://localhost:3000 in your browser")

if __name__ == "__main__":
    asyncio.run(test_system_local())