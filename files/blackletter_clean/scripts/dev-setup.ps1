# scripts/dev-setup.ps1 - Development Environment Setup
param(
    [switch]$SkipPython = $false,
    [switch]$SkipNode = $false,
    [switch]$Force = $false
)

$ErrorActionPreference = "Stop"

Write-Host "Blackletter Systems - Development Setup" -ForegroundColor Green
Write-Host "Context Engineering Framework Compliant" -ForegroundColor Cyan

# Check admin privileges
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Warning "Running without admin privileges. Some operations may fail."
}

# Set execution policy
try {
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    Write-Host "PowerShell execution policy set to RemoteSigned" -ForegroundColor Green
} catch {
    Write-Warning "Could not set execution policy: $($_.Exception.Message)"
}

# Create .env from .env.example if missing
if (-not (Test-Path ".env") -or $Force) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "Created .env from .env.example" -ForegroundColor Green
        Write-Host "IMPORTANT: Edit .env with your actual Supabase credentials!" -ForegroundColor Yellow
    } else {
        Write-Error ".env.example not found. Cannot create .env file."
    }
} else {
    Write-Host ".env file already exists (use -Force to overwrite)" -ForegroundColor Yellow
}

# Python Setup (3.11+)
if (-not $SkipPython) {
    Write-Host "`nSetting up Python environment..." -ForegroundColor Cyan
    
    # Check Python version
    try {
        $pythonOutput = python --version 2>&1
        if ($pythonOutput -match "Python 3\.1[1-9]") {
            Write-Host "Python version OK: $pythonOutput" -ForegroundColor Green
        } else {
            Write-Error "Python 3.11+ required. Found: $pythonOutput"
        }
    } catch {
        Write-Error "Python not found. Please install Python 3.11+ from python.org"
    }
    
    # Create virtual environment in backend
    if (Test-Path "backend") {
        Push-Location "backend"
        
        if (Test-Path "venv") {
            Write-Host "Virtual environment already exists" -ForegroundColor Yellow
        } else {
            python -m venv venv
            Write-Host "Created Python virtual environment" -ForegroundColor Green
        }
        
        # Activate and install dependencies
        if (Test-Path "venv/Scripts/Activate.ps1") {
            & "./venv/Scripts/Activate.ps1"
            python -m pip install --upgrade pip
            
            if (Test-Path "requirements.txt") {
                pip install -r requirements.txt
                Write-Host "Installed Python dependencies" -ForegroundColor Green
            } else {
                Write-Warning "requirements.txt not found in backend/"
            }
        }
        
        Pop-Location
    } else {
        Write-Warning "backend/ directory not found"
    }
}

# Node.js Setup
if (-not $SkipNode) {
    Write-Host "`nSetting up Node.js environment..." -ForegroundColor Cyan
    
    # Check Node version
    try {
        $nodeVersion = node --version 2>&1
        if ($nodeVersion -match "v[0-9]+\.[0-9]+\.[0-9]+") {
            Write-Host "Node.js version: $nodeVersion" -ForegroundColor Green
        } else {
            Write-Error "Node.js not found or invalid version"
        }
    } catch {
        Write-Error "Node.js not found. Please install Node.js LTS from nodejs.org"
    }
    
    # Install frontend dependencies
    if (Test-Path "frontend") {
        Push-Location "frontend"
        
        if (Test-Path "package.json") {
            npm install
            Write-Host "Installed Node.js dependencies" -ForegroundColor Green
        } else {
            Write-Warning "package.json not found in frontend/"
        }
        
        Pop-Location
    } else {
        Write-Warning "frontend/ directory not found"
    }
}

# Create upload directory
if (-not (Test-Path "uploads")) {
    New-Item -ItemType Directory -Path "uploads" -Force | Out-Null
    Write-Host "Created uploads directory" -ForegroundColor Green
}

# Validate Docker
Write-Host "`nChecking Docker..." -ForegroundColor Cyan
try {
    $dockerVersion = docker --version 2>&1
    Write-Host "Docker: $dockerVersion" -ForegroundColor Green
    
    $composeVersion = docker-compose --version 2>&1
    Write-Host "Docker Compose: $composeVersion" -ForegroundColor Green
} catch {
    Write-Warning "Docker not found. Install Docker Desktop for full development experience."
}

Write-Host "`nDevelopment setup complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env with your Supabase credentials" -ForegroundColor White
Write-Host "2. Run: .\scripts\docker-up.ps1" -ForegroundColor White
Write-Host "3. Run: .\scripts\test-backend.ps1" -ForegroundColor White
Write-Host "4. Run: .\tools\context_engineering.ps1 -Action test" -ForegroundColor White