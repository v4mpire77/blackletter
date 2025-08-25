#!/bin/bash
# start-production.sh - Production startup script for Blackletter GDPR Processor

echo "🚀 Starting Blackletter GDPR Processor..."

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "🐳 Using Docker deployment..."
    
    # Check if docker-compose file exists
    if [ -f "docker-compose.final.yml" ]; then
        echo "📋 Starting services with docker-compose..."
        docker-compose -f docker-compose.final.yml up -d
        
        echo "⏱️  Waiting for services to start..."
        sleep 30
        
        echo "🔍 Checking service status..."
        docker-compose -f docker-compose.final.yml ps
        
        echo "✅ Services started successfully!"
        echo "   Frontend: http://localhost:3000"
        echo "   Backend: http://localhost:8000"
        echo "   API Docs: http://localhost:8000/docs"
        
    else
        echo "❌ docker-compose.final.yml not found!"
        exit 1
    fi
    
else
    echo "⚠️  Docker not found. Please install Docker to run the system."
    echo "   Alternatively, follow the manual installation guide in PRODUCTION_DEPLOYMENT_GUIDE.md"
    exit 1
fi