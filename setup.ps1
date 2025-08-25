# setup.ps1 - Complete setup script for Blackletter GDPR Processor on Windows

Write-Host "🚀 Setting up Blackletter GDPR Processor..." -ForegroundColor Green

# Check if Docker is installed
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if docker-compose is installed
try {
    $composeVersion = docker-compose --version
    Write-Host "✅ docker-compose found: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ docker-compose is not installed. Please install Docker Desktop (includes docker-compose)." -ForegroundColor Red
    exit 1
}

# Create necessary directories
Write-Host "📁 Creating directories..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path "backend/uploads" -Force | Out-Null
New-Item -ItemType Directory -Path "backend/reports" -Force | Out-Null
New-Item -ItemType Directory -Path "data" -Force | Out-Null

Write-Host "🔧 Setting up environment files..." -ForegroundColor Cyan

# Check if backend/.env exists, if not create it
if (-not (Test-Path "backend/.env")) {
    Write-Host "Creating backend/.env from example..." -ForegroundColor Yellow
    Copy-Item ".env.example" "backend/.env"
    Write-Host "⚠️  Please update backend/.env with your actual values, especially:" -ForegroundColor Yellow
    Write-Host "   - OPENAI_API_KEY (if using LLM features)" -ForegroundColor Yellow
    Write-Host "   - SECRET_KEY (change the default for production)" -ForegroundColor Yellow
}

# Check if frontend/.env.local exists, if not create it
if (-not (Test-Path "frontend/.env.local")) {
    Write-Host "Creating frontend/.env.local..." -ForegroundColor Yellow
    "NEXT_PUBLIC_API_URL=http://localhost:8000" | Out-File -FilePath "frontend/.env.local" -Encoding UTF8
}

Write-Host "🐳 Starting services with docker-compose..." -ForegroundColor Cyan
docker-compose -f docker-compose.final.yml up -d

Write-Host "⏱️  Waiting for services to start..." -ForegroundColor Cyan
Start-Sleep -Seconds 15

# Check if services are running
Write-Host "🔍 Checking service status..." -ForegroundColor Cyan
docker-compose -f docker-compose.final.yml ps

Write-Host "📋 Services started:" -ForegroundColor Green
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "   Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "   Backend Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "   Redis: localhost:6379" -ForegroundColor White
Write-Host "   Database: localhost:54322" -ForegroundColor White

Write-Host "🎉 Setup complete!" -ForegroundColor Green
Write-Host "" -ForegroundColor White
Write-Host "To test the system:" -ForegroundColor White
Write-Host "1. Visit http://localhost:3000 in your browser" -ForegroundColor White
Write-Host "2. Upload a contract document" -ForegroundColor White
Write-Host "3. The system will process it and show compliance results" -ForegroundColor White
Write-Host "" -ForegroundColor White
Write-Host "To stop the services later, run: docker-compose -f docker-compose.clean.yml down" -ForegroundColor White