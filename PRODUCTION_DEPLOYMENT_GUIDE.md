# Blackletter GDPR Processor - Production Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the Blackletter GDPR Processor system to a production environment. The system can be deployed using Docker containers for simplified management and scalability.

## Prerequisites

Before deploying, ensure you have:

1. **Server/VM** with at least:
   - 4GB RAM (8GB recommended)
   - 2 CPU cores
   - 20GB storage space
   - Ubuntu 20.04+ or CentOS 8+ (recommended)

2. **Domain name** (optional but recommended for production)

3. **SSL certificate** (recommended for production)

## Installation Options

### Option 1: Docker Deployment (Recommended)

#### Step 1: Install Docker and Docker Compose

```bash
# Update package index
sudo apt-get update

# Install Docker
sudo apt-get install docker.io -y

# Install Docker Compose
sudo apt-get install docker-compose -y

# Add current user to docker group
sudo usermod -aG docker $USER

# Restart shell or logout/login to apply group changes
```

#### Step 2: Download the Application

```bash
# Clone the repository
git clone <repository-url>
cd blackletter

# Or download the latest release
wget <release-url>
tar -xzf blackletter.tar.gz
cd blackletter
```

#### Step 3: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example backend/.env

# Edit the environment file with your configuration
nano backend/.env
```

Required environment variables:
```bash
# Secret key for JWT signing (generate a secure random string)
SECRET_KEY=your-very-secure-secret-key-here

# Database configuration (if using external PostgreSQL)
DATABASE_URL=postgresql://user:password@host:port/database

# Redis configuration (if using external Redis)
REDIS_URL=redis://host:port/0

# Optional: OpenAI API key for LLM features
OPENAI_API_KEY=your-openai-api-key-here
```

#### Step 4: Start the Application

```bash
# Start all services
docker-compose -f docker-compose.final.yml up -d

# Check if services are running
docker-compose -f docker-compose.final.yml ps

# View logs (optional)
docker-compose -f docker-compose.final.yml logs -f
```

#### Step 5: Verify Installation

```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend (may take a minute to build)
curl http://localhost:3000/health
```

### Option 2: Manual Installation

#### Step 1: Install System Dependencies

```bash
# Update package index
sudo apt-get update

# Install system dependencies
sudo apt-get install python3 python3-pip postgresql postgresql-contrib redis-server nodejs npm -y
```

#### Step 2: Set Up PostgreSQL Database

```bash
# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql << EOF
CREATE DATABASE blackletter;
CREATE USER blackletter_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE blackletter TO blackletter_user;
\q
EOF
```

#### Step 3: Set Up Redis

```bash
# Start Redis service
sudo systemctl start redis
sudo systemctl enable redis
```

#### Step 4: Install Backend Dependencies

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

#### Step 5: Install Frontend Dependencies

```bash
# Navigate to frontend directory
cd ../frontend

# Install Node.js dependencies
npm install

# Build the frontend
npm run build
```

#### Step 6: Configure Environment Variables

Create `backend/.env` with your configuration:
```bash
SECRET_KEY=your-very-secure-secret-key-here
DATABASE_URL=postgresql://blackletter_user:secure_password@localhost:5432/blackletter
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=your-openai-api-key-here  # Optional
```

#### Step 7: Start Services

In separate terminals:

```bash
# Terminal 1: Start backend
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 2: Start Celery workers
cd backend
source venv/bin/activate
celery -A workers.celery_app worker --loglevel=info

# Terminal 3: Start frontend
cd frontend
npm run start
```

## Production Configuration

### Reverse Proxy (Nginx)

For production deployments, use Nginx as a reverse proxy:

```bash
# Install Nginx
sudo apt-get install nginx -y

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/blackletter
```

Nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/blackletter /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Test automatic renewal
sudo certbot renew --dry-run
```

## Monitoring and Maintenance

### Health Checks

Monitor these endpoints:
- Backend health: `http://your-domain.com/api/health`
- Frontend health: `http://your-domain.com/health`

### Log Monitoring

```bash
# Docker logs
docker-compose -f docker-compose.final.yml logs -f

# Manual installation logs
# Check system journal for service logs
journalctl -u blackletter-backend -f
```

### Backup Procedures

```bash
# Database backup
pg_dump -U blackletter_user -h localhost blackletter > backup.sql

# File backup
tar -czf blackletter-backup.tar.gz /path/to/blackletter
```

## Scaling for Production

### Horizontal Scaling

To handle more users, you can scale the worker processes:

```bash
# Scale Celery workers
docker-compose -f docker-compose.final.yml up -d --scale celery=3
```

### Vertical Scaling

Increase resources allocated to containers:
```yaml
# In docker-compose.final.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
```

## Security Considerations

1. **Environment Variables**: Never commit secrets to version control
2. **Firewall**: Restrict access to only necessary ports
3. **Updates**: Regularly update Docker images and dependencies
4. **Backups**: Implement regular backup procedures
5. **Monitoring**: Set up alerts for system issues

## Troubleshooting

### Common Issues

1. **Services not starting**:
   ```bash
   # Check logs
   docker-compose -f docker-compose.final.yml logs
   
   # Restart services
   docker-compose -f docker-compose.final.yml restart
   ```

2. **Database connection issues**:
   ```bash
   # Check database connectivity
   pg_isready -U blackletter_user -d blackletter -h localhost
   ```

3. **Frontend build failures**:
   ```bash
   # Rebuild frontend
   cd frontend && npm run build
   ```

### Getting Help

If you encounter issues:
1. Check the logs for error messages
2. Verify all environment variables are set correctly
3. Ensure all required services are running
4. Refer to the documentation in the repository

## Conclusion

The Blackletter GDPR Processor system is now deployed and ready for production use. The system will automatically process uploaded contracts for GDPR compliance and provide detailed analysis results.

For any questions or support, please refer to the project documentation or contact the development team.