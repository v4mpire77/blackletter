# start-production.ps1 - Production startup script for Blackletter GDPR Processor

Write-Host "🚀 Starting Blackletter GDPR Processor..." -ForegroundColor Green

# Check if Docker is available
try {
    $dockerVersion = docker --version
    Write-Host "🐳 Using Docker deployment..." -ForegroundColor Cyan
    Write-Host "   $dockerVersion" -ForegroundColor Gray
    
    # Check if docker-compose file exists
    if (Test-Path "docker-compose.final.yml") {
        Write-Host "📋 Starting services with docker-compose..." -ForegroundColor Cyan
        docker-compose -f docker-compose.final.yml up -d
        
        Write-Host "⏱️  Waiting for services to start..." -ForegroundColor Yellow
        Start-Sleep -Seconds 30
        
        Write-Host "🔍 Checking service status..." -ForegroundColor Cyan
        docker-compose -f docker-compose.final.yml ps
        
        Write-Host "✅ Services started successfully!" -ForegroundColor Green
        Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
        Write-Host "   Backend: http://localhost:8000" -ForegroundColor White
        Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
        
    } else {
        Write-Host "❌ docker-compose.final.yml not found!" -ForegroundColor Red
        exit 1
    }
    
} catch {
    Write-Host "⚠️  Docker not found. Please install Docker Desktop to run the system." -ForegroundColor Yellow
    Write-Host "   Alternatively, follow the manual installation guide in PRODUCTION_DEPLOYMENT_GUIDE.md" -ForegroundColor Gray
    exit 1
}