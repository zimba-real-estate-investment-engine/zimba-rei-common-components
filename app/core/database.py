from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from urllib.parse import quote_plus

# Database configuration
DB_USER = os.getenv('DB_USER', 'rei_app_rds_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'thepassword')  # Consider moving this to environment variable
DB_HOST = os.getenv('DB_HOST', 'zimba-rei-micro.cz2qemaeifj0.us-east-2.rds.amazonaws.com')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'zimba_rei_micro')

# Create the SQLAlchemy database URL
# We use quote_plus to properly encode the password
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Enables automatic reconnection
    pool_size=5,  # Maximum number of connections to keep persistently
    max_overflow=10  # Maximum number of connections that can be created beyond pool_size
)

# SessionLocal class will be used to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Test the connection
def test_connection():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        print("Successfully connected to the database!")
        return True
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    test_connection()
