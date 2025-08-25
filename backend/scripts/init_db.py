#!/usr/bin/env python3
"""
Database initialization script for Blackletter GDPR Processor.
Creates all necessary tables in the database.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add backend to path so we can import our modules
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from app.db.session import Base
from app.models.job import Job

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db():
    """Initialize the database by creating all tables."""
    try:
        # Create engine
        logger.info("Creating database engine...")
        engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
        
        # Create all tables
        logger.info("Creating tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Database initialization completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False
    finally:
        # Dispose engine
        if 'engine' in locals():
            await engine.dispose()

if __name__ == "__main__":
    logger.info("Starting database initialization...")
    success = asyncio.run(init_db())
    sys.exit(0 if success else 1)