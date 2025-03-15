"""
Base models for SQLAlchemy ORM.

This module defines the base models and utility functions for the ORM layer.
"""

from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """
    Base class for all SQLAlchemy models.
    
    Provides common columns (id) and methods for all models.
    """

    id: Any
    __name__: str
    
    # Common columns for all models
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Generate __tablename__ automatically based on class name
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate table name from class name.
        
        Returns
        -------
        str
            Table name in snake_case
        """
        return cls.__name__.lower()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model instance to dictionary.
        
        Returns
        -------
        Dict[str, Any]
            Dictionary representation of the model
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
