# Blackletter GDPR Processor - Quick Start Guide

## Overview
Get the Blackletter GDPR Processor system up and running in minutes with this quick start guide.

## Prerequisites
- Docker and Docker Compose installed
- 4GB+ RAM recommended
- Git (optional, for cloning repository)

## Quick Deployment

### 1. Get the Code
```bash
# Clone the repository
git clone <repository-url>
cd blackletter

# Or download and extract the release archive
```

### 2. Configure Environment
```bash
# Copy environment template
cp .env.example backend/.env

# Edit backend/.env with your settings
# At minimum, set a secure SECRET_KEY
```

### 3. Start the System
```bash
# Using the provided script (recommended)
./start-production.sh        # Linux/macOS
./start-production.ps1       # Windows

# Or using Docker Compose directly
docker-compose -f docker-compose.final.yml up -d
```

### 4. Access the Application
1. Wait 30-60 seconds for services to start
2. Open browser to:
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

## First Use

### Upload a Contract
1. Click "Upload Contract" in the web interface
2. Select a PDF, TXT, or DOCX file (< 10MB)
3. Wait for processing to complete (typically 15-30 seconds)
4. Review GDPR compliance analysis results

### Review Results
1. Check the dashboard for compliance metrics
2. Review detailed findings in the results table
3. Export results if needed

## Common Tasks

### Stop the System
```bash
# Using Docker Compose
docker-compose -f docker-compose.final.yml down
```

### View Logs
```bash
# View all logs
docker-compose -f docker-compose.final.yml logs -f

# View specific service logs
docker-compose -f docker-compose.final.yml logs frontend
docker-compose -f docker-compose.final.yml logs backend
```

### Update the System
```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose -f docker-compose.final.yml up -d --build
```

## Next Steps

### Production Deployment
1. Configure domain name and SSL certificate
2. Set up monitoring and alerting
3. Implement backup procedures
4. Review security hardening options

### Advanced Configuration
1. Review `docker-compose.final.yml` for customization
2. Adjust environment variables in `backend/.env`
3. Configure external database/Redis if needed

## Getting Help

### Documentation
- README.md: Complete system overview
- PRODUCTION_DEPLOYMENT_GUIDE.md: Detailed deployment instructions
- API_DOCUMENTATION.md: API endpoint reference

### Support
For issues or questions, please:
1. Check the documentation
2. Review logs for error messages
3. Verify all prerequisites are met
4. Contact support team

---

*Blackletter GDPR Processor - Automated GDPR Article 28(3) Compliance Analysis*