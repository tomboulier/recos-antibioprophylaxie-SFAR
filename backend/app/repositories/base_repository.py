"""
Base repository implementation.

This module provides a generic base repository that implements common CRUD operations
for all entities, following the Repository pattern.
"""

import logging
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models.base import Base

# Define generic types for models and schemas
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

# Get logger
logger = logging.getLogger(__name__)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for all repositories, implementing CRUD operations.
    
    Parameters
    ----------
    model : Type[ModelType]
        The SQLAlchemy model class this repository operates on
    """

    def __init__(self, model: Type[ModelType]):
        """
        Initialize repository with a model.
        
        Parameters
        ----------
        model : Type[ModelType]
            The SQLAlchemy model class this repository operates on
        """
        self.model = model
    
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Get a single record by ID.
        
        Parameters
        ----------
        db : Session
            Database session
        id : Any
            ID of the record to get
            
        Returns
        -------
        Optional[ModelType]
            The record if found, None otherwise
        """
        result = db.query(self.model).filter(self.model.id == id).first()
        if result is None:
            logger.debug(f"No {self.model.__name__} found with id {id}")
        return result
    
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Get multiple records with pagination.
        
        Parameters
        ----------
        db : Session
            Database session
        skip : int, optional
            Number of records to skip, by default 0
        limit : int, optional
            Maximum number of records to return, by default 100
            
        Returns
        -------
        List[ModelType]
            List of records
        """
        result = db.query(self.model).offset(skip).limit(limit).all()
        logger.debug(f"Retrieved {len(result)} {self.model.__name__} records")
        return result
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.
        
        Parameters
        ----------
        db : Session
            Database session
        obj_in : CreateSchemaType
            Schema with data to create
            
        Returns
        -------
        ModelType
            The created record
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        logger.info(f"Created new {self.model.__name__} with ID {db_obj.id}")
        return db_obj
    
    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        """
        Update a record.
        
        Parameters
        ----------
        db : Session
            Database session
        db_obj : ModelType
            Existing database object to update
        obj_in : UpdateSchemaType
            Schema with update data
            
        Returns
        -------
        ModelType
            The updated record
        """
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        logger.info(f"Updated {self.model.__name__} with ID {db_obj.id}")
        return db_obj
    
    def remove(self, db: Session, *, id: Any) -> Optional[ModelType]:
        """
        Delete a record by ID.
        
        Parameters
        ----------
        db : Session
            Database session
        id : Any
            ID of the record to delete
            
        Returns
        -------
        Optional[ModelType]
            The deleted record if found, None otherwise
        """
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
            logger.info(f"Deleted {self.model.__name__} with ID {id}")
            return obj
        
        logger.warning(f"Attempted to delete non-existent {self.model.__name__} with ID {id}")
        return None
