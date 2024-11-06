# alembic/env.py
import sys, os
from pathlib import Path
from logging.config import fileConfig

# from sqlalchemy import engine_from_config
import sqlalchemy
from sqlalchemy import pool
from alembic import context


# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
fileConfig(config.config_file_name)

# Set target metadata
from config import Utils
target_metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(Utils.DATABASE_URL)


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Override the SQLAlchemy URL with the one from our config
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # include_schemas=True  # Add this if using schemas
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()