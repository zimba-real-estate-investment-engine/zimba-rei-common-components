# tests/test_database.py

from sqlalchemy.orm import Session
from app.core.database import get_db, SessionLocal, engine, Base
from app.models.user import User  # Assuming there's a User model for demonstration


def test_database_connection():
    # Test that we can create a session and query the database
    with SessionLocal() as db:
        assert isinstance(db, Session)  # Check session instance
        # Example: Check if tables exist by querying metadata
        assert engine.dialect.has_table(engine, "users")  # Assuming User table exists


def test_get_db_dependency():
    # Ensure that get_db yields a session and closes it properly
    db_gen = get_db()
    db = next(db_gen)
    assert isinstance(db, Session)  # Check if it's a session
    db_gen.close()  # Close the generator to simulate request end
