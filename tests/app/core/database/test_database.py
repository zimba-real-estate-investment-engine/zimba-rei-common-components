# tests/test_database.py

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.engine.cursor import CursorResult
from app.core.database import get_db, SessionLocal, engine, Base


def test_database_connection():
    # Test that we can create a session and query the migrations
    with SessionLocal() as db:
        assert isinstance(db, Session)  # Check session instance
        # Example: Check if tables exist by querying metadata
        # assert engine.dialect.has_table(engine, "subscriptions")  # Assuming subscription table exists


def test_select_on_db():
    with SessionLocal() as db:
        result = db.execute(select(1))
        assert result.rowcount > 0
        assert isinstance(result, CursorResult)
        assert not result.closed


def test_get_db_dependency():
    # Ensure that get_db yields a session and closes it properly
    db_gen = get_db()
    db = next(db_gen)
    assert isinstance(db, Session)  # Check if it's a session
    db_gen.close()  # Close the generator to simulate request end
