# Blackletter GDPR Processor - Quick Start Guide

This guide will help you set up and run the Blackletter GDPR Processor system on your local machine.

## Prerequisites

1. **Python 3.8+** with pip
2. **Node.js 16+** with npm
3. **PostgreSQL** database
4. **Redis** server
5. **Docker** (optional, for containerized deployment)

## Quick Setup (Direct Installation)

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create backend/.env file with your configuration
cp .env.example .env
# Edit .env with your settings (database, Redis, API keys, etc.)

# Initialize the database
python scripts/init_db.py

# Run the backend server
uvicorn main:app --reload
```

The backend will be available at http://localhost:8000

### 2. Frontend Setup

In a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create frontend/.env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run the frontend development server
npm run dev
```

The frontend will be available at http://localhost:3000

### 3. Redis Setup

Install and start Redis server:

- **Windows**: Download from https://redis.io/download/
- **macOS**: `brew install redis && brew services start redis`
- **Linux**: `sudo apt install redis-server && sudo systemctl start redis`

### 4. PostgreSQL Setup

Install and start PostgreSQL:

- **Windows**: Download from https://www.postgresql.org/download/windows/
- **macOS**: `brew install postgresql && brew services start postgresql`
- **Linux**: `sudo apt install postgresql && sudo systemctl start postgresql`

Create a database for the application:
```sql
CREATE DATABASE blackletter;
CREATE USER blackletter WITH PASSWORD 'blackletter';
GRANT ALL PRIVILEGES ON DATABASE blackletter TO blackletter;
```

## Testing the System

1. Visit http://localhost:3000 in your browser
2. Upload a contract document (PDF, DOCX, or TXT)
3. The system will process it and show compliance results

## Docker Setup (Alternative)

If you prefer to use Docker:

1. Install Docker Desktop
2. Run the setup script:
   ```bash
   # Windows
   .\setup.ps1
   
   # macOS/Linux
   ./setup.sh
   ```

3. Access the system at:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## API Documentation

Once the backend is running, you can access the API documentation at:
http://localhost:8000/docs

## Troubleshooting

### Common Issues

1. **Port conflicts**: Make sure ports 3000, 8000, 5432, and 6379 are free
2. **Database connection errors**: Check your database credentials in .env
3. **Redis connection errors**: Ensure Redis is running
4. **Missing dependencies**: Run `pip install -r requirements.txt` again

### Dependency Issues

If you encounter dependency conflicts:

1. Update pip: `pip install --upgrade pip`
2. Clear pip cache: `pip cache purge`
3. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

For frontend issues:
1. Delete node_modules: `rm -rf node_modules`
2. Delete package-lock.json: `rm package-lock.json`
3. Reinstall: `npm install`

## Next Steps

1. Configure your OpenAI API key in the backend .env file for LLM features
2. Customize the GDPR compliance rules in the rules/ directory
3. Add authentication and user management
4. Set up monitoring and logging
5. Configure production deployment settings