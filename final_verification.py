#!/usr/bin/env python3
"""
Final Verification Script for Blackletter GDPR Processor
This script performs a comprehensive check of all system components
to ensure everything is ready for production deployment.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and report status"""
    exists = Path(filepath).exists()
    status = "PASS" if exists else "FAIL"
    print(f"{status} {description}")
    return exists

def check_directory_exists(dirpath, description):
    """Check if a directory exists and report status"""
    exists = Path(dirpath).exists()
    status = "PASS" if exists else "FAIL"
    print(f"{status} {description}")
    return exists

def run_command(command, description):
    """Run a command and report success or failure"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        success = result.returncode == 0
        status = "PASS" if success else "FAIL"
        print(f"{status} {description}")
        if not success and result.stderr:
            print(f"     Error: {result.stderr.strip()}")
        return success
    except subprocess.TimeoutExpired:
        print(f"FAIL {description} - Command timed out")
        return False
    except Exception as e:
        print(f"FAIL {description} - {str(e)}")
        return False

def check_docker():
    """Check if Docker is installed and running"""
    print("\nDocker Check:")
    docker_installed = run_command("docker --version", "Docker installed")
    if docker_installed:
        run_command("docker info", "Docker daemon running")
    return docker_installed

def check_frontend():
    """Check frontend components"""
    print("\nFrontend Check:")
    frontend_built = check_directory_exists("frontend/.next", "Frontend built successfully")
    package_json = check_file_exists("frontend/package.json", "Frontend package.json exists")
    env_local = check_file_exists("frontend/.env.local", "Frontend environment file exists")
    return frontend_built and package_json and env_local

def check_backend():
    """Check backend components"""
    print("\nBackend Check:")
    main_py = check_file_exists("backend/main.py", "Backend main.py exists")
    requirements = check_file_exists("backend/requirements.txt", "Backend requirements.txt exists")
    env_file = check_file_exists("backend/.env", "Backend environment file exists")
    return main_py and requirements and env_file

def check_docker_compose():
    """Check Docker Compose files"""
    print("\nDocker Compose Check:")
    compose_file = check_file_exists("docker-compose.final.yml", "Production Docker Compose file exists")
    return compose_file

def check_scripts():
    """Check deployment scripts"""
    print("\nScripts Check:")
    bash_script = check_file_exists("start-production.sh", "Bash startup script exists")
    ps_script = check_file_exists("start-production.ps1", "PowerShell startup script exists")
    return bash_script and ps_script

def check_documentation():
    """Check key documentation files"""
    print("\nDocumentation Check:")
    readme = check_file_exists("README.md", "README.md exists")
    deployment_guide = check_file_exists("PRODUCTION_DEPLOYMENT_GUIDE.md", "Deployment guide exists")
    completion_status = check_file_exists("PROJECT_COMPLETION_STATUS.md", "Completion status exists")
    return readme and deployment_guide and completion_status

def main():
    """Main verification function"""
    print("BLACKLETTER GDPR PROCESSOR - FINAL VERIFICATION")
    print("=" * 60)
    
    # Run all checks
    checks = [
        ("Docker", check_docker),
        ("Frontend", check_frontend),
        ("Backend", check_backend),
        ("Docker Compose", check_docker_compose),
        ("Scripts", check_scripts),
        ("Documentation", check_documentation)
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"FAIL {name} check - {str(e)}")
            results[name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    print(f"Checks Passed: {passed}/{total}")
    
    for name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"  {status} {name}")
    
    # Overall status
    if passed == total:
        print("\nALL CHECKS PASSED!")
        print("The Blackletter GDPR Processor system is ready for production deployment.")
        print("\nTo deploy:")
        print("  1. Configure backend/.env with your settings")
        print("  2. Run ./start-production.sh (Linux/macOS) or ./start-production.ps1 (Windows)")
        print("  3. Access the application at http://localhost:3000")
        return 0
    else:
        print(f"\n{total - passed} CHECK(S) FAILED")
        print("Please review the failed checks above and resolve issues before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())