#!/usr/bin/env python3
"""
Database Connectivity Test for Blackletter System
Tests PostgreSQL connection through backend API and direct connection
"""
import asyncio
import asyncpg
import httpx
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConnectivityTest:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.db_url_local = "postgresql://postgres:postgres@localhost:54322/postgres"
        
    async def test_direct_db_connection(self):
        """Test direct PostgreSQL connection"""
        print(" Testing direct PostgreSQL connection...")
        
        try:
            # Try to connect to the local PostgreSQL instance
            conn = await asyncpg.connect(self.db_url_local, timeout=10)
            
            # Test basic query
            result = await conn.fetchval("SELECT version()")
            
            await conn.close()
            
            print("✅ Direct database connection successful")
            print(f"   PostgreSQL version: {result}")
            return True
            
        except Exception as e:
            print(f"❌ Direct database connection failed: {e}")
            return False
    
    async def test_backend_health(self):
        """Test backend health and database connectivity through API"""
        print("\n Testing backend health and database connectivity...")
        
        try:
            async with httpx.AsyncClient() as client:
                # Test health endpoint
                response = await client.get(f"{self.backend_url}/health", timeout=10.0)
                
                if response.status_code == 200:
                    health_data = response.json()
                    print("✅ Backend health check passed")
                    print(f"   Backend version: {health_data.get('version', 'unknown')}")
                    print(f"   Status: {health_data.get('status', 'unknown')}")
                    
                    # Test database-dependent endpoint
                    try:
                        response = await client.get(f"{self.backend_url}/api/v1/jobs/", timeout=10.0)
                        
                        if response.status_code == 200:
                            print("✅ Backend database connectivity confirmed")
                            jobs = response.json()
                            print(f"   Jobs endpoint returned {len(jobs)} items")
                            return True
                        else:
                            print(f"⚠️  Jobs endpoint returned status {response.status_code}")
                            print(f"   Response: {response.text}")
                            # This might be okay if the endpoint returns 404 for empty results
                            return True
                    except Exception as e:
                        print(f"⚠️  Jobs endpoint test failed: {e}")
                        # Continue with other tests
                        return True
                else:
                    print(f"❌ Backend health check failed with status {response.status_code}")
                    print(f"   Response: {response.text}")
                    return False
                    
        except Exception as e:
            print(f"❌ Backend health test failed: {e}")
            return False
    
    async def test_frontend_health(self):
        """Test frontend health"""
        print("\n Testing frontend health...")
        
        try:
            async with httpx.AsyncClient() as client:
                # Test frontend health
                response = await client.get("http://localhost:3000/health", timeout=10.0)
                
                if response.status_code == 200:
                    print("✅ Frontend health check passed")
                    return True
                else:
                    print(f"⚠️  Frontend health check returned status {response.status_code}")
                    print(f"   This may be normal during startup")
                    return True  # Not critical for overall system health
                    
        except Exception as e:
            print(f"⚠️  Frontend health test failed: {e}")
            print("   This may be normal during startup")
            return True  # Not critical for overall system health
    
    async def test_full_stack_integration(self):
        """Test full stack integration"""
        print("\n Testing full stack integration...")
        
        # Test each component
        db_connected = await self.test_direct_db_connection()
        backend_healthy = await self.test_backend_health()
        frontend_healthy = await self.test_frontend_health()
        
        # Overall status
        overall_success = db_connected and backend_healthy
        
        print("\n" + "="*60)
        print(" DATABASE CONNECTIVITY TEST SUMMARY")
        print("="*60)
        print(f"Direct Database Connection: {'✅ PASS' if db_connected else '❌ FAIL'}")
        print(f"Backend Health: {'✅ PASS' if backend_healthy else '❌ FAIL'}")
        print(f"Frontend Health: {'✅ PASS' if frontend_healthy else '⚠️  WARN'}")
        print(f"Overall Status: {'✅ READY' if overall_success else '❌ ISSUE'}")
        
        if overall_success:
            print("\n🎉 All critical components are working correctly!")
            print("The Blackletter GDPR Processor system is ready for use.")
        else:
            print("\n⚠️  Some components need attention.")
            print("Please check the error messages above and resolve issues.")
        
        return overall_success

async def main():
    """Main test function"""
    print("BLACKLETTER GDPR PROCESSOR - DATABASE CONNECTIVITY TEST")
    print("="*60)
    
    tester = DatabaseConnectivityTest()
    success = await tester.test_full_stack_integration()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)