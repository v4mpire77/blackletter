#!/usr/bin/env python3
"""
Comprehensive End-to-End Test Suite for Blackletter System
Tests all critical components and user workflows
"""
import asyncio
import httpx
import json
import os
import time
from pathlib import Path
from typing import Dict, Any

class E2ETestSuite:
    def __init__(self):
        self.frontend_url = "http://localhost:3000"
        self.backend_url = "http://localhost:8000"
        self.test_results = []
        
    def log_test(self, test_name: str, status: str, details: str = ""):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        
        # Print immediate feedback
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {status}")
        if details:
            print(f"   {details}")
    
    async def test_service_health(self) -> bool:
        """Test 1: Verify all services are healthy"""
        print("\n Testing Service Health...")
        
        all_healthy = True
        
        # Test backend health
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.backend_url}/health", timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    self.log_test("Backend Health Check", "PASS", f"Version: {data.get('version', 'unknown')}")
                else:
                    self.log_test("Backend Health Check", "FAIL", f"Status: {response.status_code}")
                    all_healthy = False
        except Exception as e:
            self.log_test("Backend Health Check", "FAIL", str(e))
            all_healthy = False
        
        # Test frontend health
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.frontend_url}/health", timeout=10.0)
                if response.status_code == 200:
                    self.log_test("Frontend Health Check", "PASS")
                else:
                    self.log_test("Frontend Health Check", "FAIL", f"Status: {response.status_code}")
                    all_healthy = False
        except Exception as e:
            self.log_test("Frontend Health Check", "FAIL", str(e))
            all_healthy = False
        
        # Test database connectivity via backend
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.backend_url}/api/v1/jobs/", timeout=10.0)
                if response.status_code == 200:
                    self.log_test("Database Connectivity", "PASS", "Jobs endpoint accessible")
                else:
                    self.log_test("Database Connectivity", "FAIL", f"Status: {response.status_code}")
                    all_healthy = False
        except Exception as e:
            self.log_test("Database Connectivity", "FAIL", str(e))
            all_healthy = False
        
        return all_healthy
    
    async def test_api_endpoints(self) -> bool:
        """Test 2: Verify critical API endpoints"""
        print("\n Testing API Endpoints...")
        
        endpoints = [
            ("/health", "Health Check"),
            ("/docs", "API Documentation"),
            ("/api/v1/compliance", "Compliance API"),
        ]
        
        all_passed = True
        
        for endpoint, name in endpoints:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{self.backend_url}{endpoint}", timeout=10.0)
                    if response.status_code == 200:
                        self.log_test(f"API Endpoint - {name}", "PASS")
                    else:
                        self.log_test(f"API Endpoint - {name}", "FAIL", f"Status: {response.status_code}")
                        all_passed = False
            except Exception as e:
                self.log_test(f"API Endpoint - {name}", "FAIL", str(e))
                all_passed = False
        
        return all_passed
    
    async def test_frontend_pages(self) -> bool:
        """Test 3: Verify frontend pages load"""
        print("\n Testing Frontend Pages...")
        
        pages = [
            ("/", "Home Page"),
            ("/dashboard", "Dashboard"),
            ("/upload", "Upload Page"),
        ]
        
        all_passed = True
        
        for page, name in pages:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{self.frontend_url}{page}", timeout=10.0)
                    if response.status_code == 200:
                        self.log_test(f"Frontend - {name}", "PASS")
                    else:
                        self.log_test(f"Frontend - {name}", "FAIL", f"Status: {response.status_code}")
                        all_passed = False
            except Exception as e:
                self.log_test(f"Frontend - {name}", "FAIL", str(e))
                all_passed = False
        
        return all_passed
    
    async def test_file_upload_workflow(self) -> bool:
        """Test 4: Test document upload workflow"""
        print("\n Testing File Upload Workflow...")
        
        # Create a test file
        test_content = """
        DATA PROCESSING AGREEMENT
        
        This agreement outlines the data processing obligations between parties.
        Personal data will be processed in accordance with GDPR requirements.
        The processor shall implement appropriate technical and organizational measures.
        """
        
        try:
            # Create test file
            test_file_path = Path("test_contract.txt")
            test_file_path.write_text(test_content)
            
            # Test file upload
            async with httpx.AsyncClient() as client:
                with open(test_file_path, "rb") as f:
                    files = {"file": ("test_contract.txt", f, "text/plain")}
                    response = await client.post(
                        f"{self.backend_url}/api/v1/analyze",
                        files=files,
                        timeout=30.0
                    )
                
                if response.status_code == 200:
                    job_data = response.json()
                    self.log_test("File Upload", "PASS", f"Job ID: {job_data.get('job_id', 'N/A')}")
                    return True
                else:
                    self.log_test("File Upload", "FAIL", f"Status: {response.status_code}")
                    return False
            
        except Exception as e:
            self.log_test("File Upload", "FAIL", str(e))
            return False
        finally:
            # Cleanup
            if test_file_path.exists():
                test_file_path.unlink()
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run complete end-to-end test suite"""
        print(" Starting Comprehensive End-to-End Test Suite")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run all tests
        tests = [
            ("Service Health", self.test_service_health()),
            ("API Endpoints", self.test_api_endpoints()),
            ("Frontend Pages", self.test_frontend_pages()),
            ("File Upload Workflow", self.test_file_upload_workflow()),
        ]
        
        results = {}
        for test_name, test_coro in tests:
            try:
                results[test_name] = await test_coro
            except Exception as e:
                print(f"Error running {test_name}: {e}")
                results[test_name] = False
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Calculate overall results
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        warning_tests = len([r for r in self.test_results if r["status"] == "WARN"])
        
        # Print summary
        print("\n" + "=" * 60)
        print(" TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️  Warnings: {warning_tests}")
        print(f"⏱️  Duration: {duration:.2f} seconds")
        
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        print(f" Success Rate: {success_rate:.1f}%")
        
        # Overall status
        if failed_tests == 0:
            print("\n ALL TESTS PASSED! System is ready for user testing.")
            overall_status = "READY"
        elif failed_tests <= 2 and success_rate >= 80:
            print("\n⚠️  MOSTLY READY - Minor issues detected but system functional.")
            overall_status = "MOSTLY_READY"
        else:
            print("\n CRITICAL ISSUES - System not ready for user testing.")
            overall_status = "NOT_READY"
        
        # Save detailed results
        report = {
            "overall_status": overall_status,
            "success_rate": success_rate,
            "duration": duration,
            "summary": {
                "total": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "warnings": warning_tests
            },
            "detailed_results": self.test_results,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Save report to file
        with open("e2e_test_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n Detailed report saved to: e2e_test_report.json")
        
        return report

async def main():
    """Main execution function"""
    test_suite = E2ETestSuite()
    report = await test_suite.run_all_tests()
    
    # Exit with appropriate code
    if report["overall_status"] == "READY":
        exit(0)
    elif report["overall_status"] == "MOSTLY_READY":
        exit(1)
    else:
        exit(2)

if __name__ == "__main__":
    asyncio.run(main())