# app/database.py
"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL from environment variable
# IMPORTANT: Use .env file for database configuration
# Create .env file in backend/ directory with DATABASE_URL=mysql+pymysql://username:password@host:port/database_name
DATABASE_URL = os.getenv("DATABASE_URL")

# If DATABASE_URL is not set in .env file, raise an error
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please create a .env file in the backend/ directory with DATABASE_URL. "
        "Example: DATABASE_URL=mysql+pymysql://root:root@localhost:3307/wam_db"
    )

# HARDCODED FALLBACK (COMMENTED OUT - USE .env FILE INSTEAD)
# Uncomment below only if you need a hardcoded fallback (not recommended for production)
# DATABASE_URL = "mysql+pymysql://root:root@localhost:3307/wam_db"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


def get_db() -> Generator:
    """
    Dependency function to get database session.
    Yields a database session and closes it after use.
    
    Usage:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_url():
    """
    Get database URL for use in scripts.
    """
    return DATABASE_URL


def init_db():
    """
    Initialize database tables.
    Creates all tables defined in models.
    """
    Base.metadata.create_all(bind=engine)
