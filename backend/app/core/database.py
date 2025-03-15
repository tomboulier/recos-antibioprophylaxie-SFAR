"""
Database connection handling.

This module provides functionality for database session management
and connection pooling using SQLAlchemy.
"""

import logging
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

# Get logger
logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# Create SQLAlchemy engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before usage
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {},
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """
    Get database session.

    Creates a new database session for dependency injection in FastAPI.

    Yields
    ------
    Generator
        SQLAlchemy session

    Examples
    --------
    >>> from fastapi import Depends
    >>> from app.core.database import get_db
    >>>
    >>> @app.get("/items/")
    >>> def read_items(db: Session = Depends(get_db)):
    >>>     return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
        logger.debug("Database session created successfully")
    except Exception as e:
        logger.error(f"Error during database session usage: {e}")
        raise
    finally:
        db.close()
        logger.debug("Database session closed")
