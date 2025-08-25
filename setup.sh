#!/usr/bin/env bash
# setup.sh - Complete setup script for Blackletter GDPR Processor

echo "🚀 Setting up Blackletter GDPR Processor..."

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

echo "✅ Docker and docker-compose found"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p backend/uploads
mkdir -p backend/reports
mkdir -p data

echo "🔧 Setting up environment files..."
# Check if backend/.env exists, if not create it
if [ ! -f "backend/.env" ]; then
    echo "Creating backend/.env from example..."
    cp .env.example backend/.env
    echo "⚠️  Please update backend/.env with your actual values, especially:"
    echo "   - OPENAI_API_KEY (if using LLM features)"
    echo "   - SECRET_KEY (change the default for production)"
fi

# Check if frontend/.env.local exists, if not create it
if [ ! -f "frontend/.env.local" ]; then
    echo "Creating frontend/.env.local..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > frontend/.env.local
fi

echo "🐳 Starting services with docker-compose..."
docker-compose -f docker-compose.final.yml up -d

echo "⏱️  Waiting for services to start..."
sleep 15

# Check if services are running
echo "🔍 Checking service status..."
docker-compose -f docker-compose.final.yml ps

echo "📋 Services started:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   Backend Docs: http://localhost:8000/docs"
echo "   Redis: localhost:6379"
echo "   Database: localhost:54322"

echo "🎉 Setup complete!"
echo ""
echo "To test the system:"
echo "1. Visit http://localhost:3000 in your browser"
echo "2. Upload a contract document"
echo "3. The system will process it and show compliance results"
echo ""
echo "To stop the services later, run: docker-compose -f docker-compose.clean.yml down"