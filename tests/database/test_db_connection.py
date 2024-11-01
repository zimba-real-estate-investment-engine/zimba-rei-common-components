
import pytest , logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from test_config import TestConfig
# from test_db import create_test_database

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Setup test database before running tests"""
    create_test_database()

@pytest.fixture(scope="session")
def engine():
    """Create the SQLAlchemy engine"""
    db_url = TestConfig.get_test_db_url()
    engine = create_engine(
        db_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10
    )
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def session_factory(engine):
    """Create a new session factory"""
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal

@pytest.fixture(scope="function")
def db_session(session_factory):
    """Create a new database session for a test"""
    session = session_factory()
    try:
        yield session
    finally:
        session.close()

def create_test_database():
    """Create test database if it doesn't exist"""
    # Connect to MySQL server without specifying database
    engine = create_engine(
        f"mysql+pymysql://{TestConfig.DB_USER}:{TestConfig.DB_PASSWORD}"
        f"@{TestConfig.DB_HOST}:{TestConfig.DB_PORT}"
    )
    
    try:
        with engine.connect() as conn:
            # Create database if it doesn't exist
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {TestConfig.DB_NAME}"))
            logger.info(f"Test database '{TestConfig.DB_NAME}' is ready")
    except Exception as e:
        logger.error(f"Error creating test database: {e}")
        raise
    finally:
        engine.dispose()

# test_connection.py
def test_database_connection(db_session):
    """Verify that we can connect to the test database"""
    try:
        result = db_session.execute(text("SELECT 1")).scalar()
        assert result == 1
        print("Successfully connected to test database!")
    except Exception as e:
        pytest.fail(f"Failed to connect to test database: {e}")