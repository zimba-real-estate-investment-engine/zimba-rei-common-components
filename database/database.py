# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from typing import Generator
from config import Utils

# Create database engine
DATABASE_URL: str = Utils.DATABASE_URL
engine: Engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Enables automatic reconnection
    pool_recycle=3600,   # Recycle connections after 1 hour
    echo=False           # Set to True for SQL query logging
)

# Create sessionmaker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Dependency to get DB session
def get_db() -> Generator[Session, None, None]:
    """
    Create a new database session and ensure it is closed after use.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()