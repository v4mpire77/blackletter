# Blackletter GDPR Processor - Complete Setup Guide

This guide will help you set up and run the complete Blackletter GDPR Processor system with all components.

## Prerequisites

Before running the setup, ensure you have the following installed:

1. **Docker** - [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. **Docker Compose** - Usually included with Docker Desktop
3. **Python 3.8+** (for running test scripts)
4. **Git** (if you need to clone the repository)

## Quick Start

### Windows Users

1. **Run the PowerShell setup script:**
   ```powershell
   .\setup.ps1
   ```

2. **Wait for services to start** (about 1-2 minutes)

3. **Access the system:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Linux/macOS Users

1. **Make the setup script executable:**
   ```bash
   chmod +x setup.sh
   ```

2. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

3. **Wait for services to start** (about 1-2 minutes)

4. **Access the system:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Manual Setup (Alternative)

If you prefer to set up manually:

1. **Create environment files:**
   ```bash
   # Backend
   cp .env.example backend/.env
   # Edit backend/.env to add your OpenAI API key if needed
   
   # Frontend
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > frontend/.env.local
   ```

2. **Start all services:**
   ```bash
   docker-compose -f docker-compose.clean.yml up -d
   ```

3. **Wait 1-2 minutes for services to initialize**

## Testing the System

### Automated Test

Run the test script to verify all components are working:

```bash
python test_system.py
```

### Manual Test

1. **Visit the frontend:** http://localhost:3000
2. **Upload a contract document** (PDF, DOCX, or TXT)
3. **Watch the processing status**
4. **View the compliance report** when processing completes

## System Components

The complete system includes:

1. **Frontend** (Next.js/React) - Port 3000
2. **Backend API** (FastAPI) - Port 8000
3. **Database** (PostgreSQL via Supabase) - Port 54322
4. **Redis** (for job queue) - Port 6379
5. **Celery Workers** (for background processing)
6. **Authentication Service** (Supabase GoTrue) - Port 9999

## Configuration

### Backend Environment Variables

Edit `backend/.env` to configure:

- `OPENAI_API_KEY` - For LLM analysis features
- `SECRET_KEY` - Change for production deployments
- Database and Redis connection settings (usually don't need changes)

### Frontend Environment Variables

Edit `frontend/.env.local` to configure:

- `NEXT_PUBLIC_API_URL` - API endpoint (default is fine for local setup)

## Troubleshooting

### Services Not Starting

1. **Check Docker logs:**
   ```bash
   docker-compose -f docker-compose.clean.yml logs
   ```

2. **Check individual service logs:**
   ```bash
   docker-compose -f docker-compose.final.yml logs backend
   docker-compose -f docker-compose.final.yml logs frontend
   ```

### Database Issues

1. **Ensure PostgreSQL is accessible:**
   ```bash
   docker-compose -f docker-compose.final.yml ps
   ```

2. **Restart the database service if needed:**
   ```bash
   docker-compose -f docker-compose.final.yml restart postgres-db
   ```

### Common Issues

1. **Port conflicts:** Make sure ports 3000, 8000, 54322, 6379, 9999 are free
2. **Insufficient resources:** Docker Desktop may need more memory (4GB+ recommended)
3. **Windows file permissions:** Run PowerShell as Administrator if needed

## Stopping the System

To stop all services:

```bash
docker-compose -f docker-compose.final.yml down
```

To stop services but keep data volumes:

```bash
docker-compose -f docker-compose.final.yml down
```

To stop services and remove data volumes (complete reset):

```bash
docker-compose -f docker-compose.final.yml down -v
```

## Development

### Backend Development

The backend will automatically reload when you make code changes.

### Frontend Development

The frontend will automatically rebuild when you make code changes.

### Adding New Features

1. Make your code changes
2. The services will automatically reload (thanks to Docker volumes)
3. Test your changes through the frontend or API

## Production Deployment

For production deployment, you should:

1. **Change all default passwords and secrets**
2. **Use a proper SSL certificate**
3. **Configure proper domain names**
4. **Set up backups for the database**
5. **Monitor resource usage**
6. **Set up proper logging and monitoring**

See `DEPLOYMENT.md` for detailed production deployment instructions.