#!/bin/bash
# start-blackletter.sh - Script to start all Blackletter GDPR Processor services

echo "🚀 Starting Blackletter GDPR Processor..."

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Start Docker services
echo "🐳 Starting Docker containers..."
docker-compose -f docker-compose.final.yml up -d

# Wait a moment for services to initialize
echo "⏱️  Waiting for services to start..."
sleep 10

# Check service status
echo "🔍 Checking service status..."
docker-compose -f docker-compose.final.yml ps

echo "✅ Core services started successfully!"
echo ""
echo "To complete the setup:"
echo "1. Start the frontend: cd frontend && npm run dev"
echo "2. Access the application:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"