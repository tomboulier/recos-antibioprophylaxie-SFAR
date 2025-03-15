"""
Base service implementation.

This module provides a generic base service that implements business logic
for all entities, following the Service pattern and Clean Architecture principles.
"""

import logging
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models.base import Base
from app.repositories.base_repository import BaseRepository

# Define generic types for models, schemas and repositories
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)

# Get logger
logger = logging.getLogger(__name__)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType, RepositoryType]):
    """
    Base class for all services, implementing business logic for CRUD operations.
    
    This class acts as a facade over repositories, adding business rules and validation.
    
    Parameters
    ----------
    repository : RepositoryType
        The repository instance this service operates with
    """

    def __init__(self, repository: RepositoryType):
        """
        Initialize service with a repository.
        
        Parameters
        ----------
        repository : RepositoryType
            The repository instance this service operates with
        """
        self.repository = repository
    
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Get a single record by ID with business validation.
        
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
            
        Raises
        ------
        HTTPException
            If the record is not found
        """
        obj = self.repository.get(db=db, id=id)
        if obj is None:
            entity_name = self.repository.model.__name__
            logger.warning(f"{entity_name} with ID {id} not found")
            raise HTTPException(status_code=404, detail=f"{entity_name} not found")
        return obj
    
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
        return self.repository.get_multi(db=db, skip=skip, limit=limit)
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record with business validation.
        
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
        # Apply any business rules or validation here before creating
        self._validate_create(db, obj_in)
        return self.repository.create(db=db, obj_in=obj_in)
    
    def update(
        self, db: Session, *, id: Any, obj_in: UpdateSchemaType
    ) -> ModelType:
        """
        Update a record with business validation.
        
        Parameters
        ----------
        db : Session
            Database session
        id : Any
            ID of the record to update
        obj_in : UpdateSchemaType
            Schema with update data
            
        Returns
        -------
        ModelType
            The updated record
            
        Raises
        ------
        HTTPException
            If the record is not found
        """
        db_obj = self.get(db=db, id=id)  # This will raise 404 if not found
        self._validate_update(db, db_obj, obj_in)
        return self.repository.update(db=db, db_obj=db_obj, obj_in=obj_in)
    
    def remove(self, db: Session, *, id: Any) -> ModelType:
        """
        Delete a record by ID with business validation.
        
        Parameters
        ----------
        db : Session
            Database session
        id : Any
            ID of the record to delete
            
        Returns
        -------
        ModelType
            The deleted record
            
        Raises
        ------
        HTTPException
            If the record is not found
        """
        db_obj = self.get(db=db, id=id)  # This will raise 404 if not found
        self._validate_remove(db, db_obj)
        return self.repository.remove(db=db, id=id)
    
    def _validate_create(self, db: Session, obj_in: CreateSchemaType) -> None:
        """
        Validate create operation by business rules.
        
        Override this method to implement specific business validations.
        
        Parameters
        ----------
        db : Session
            Database session
        obj_in : CreateSchemaType
            Data to validate
            
        Raises
        ------
        HTTPException
            If validation fails
        """
        pass
    
    def _validate_update(self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType) -> None:
        """
        Validate update operation by business rules.
        
        Override this method to implement specific business validations.
        
        Parameters
        ----------
        db : Session
            Database session
        db_obj : ModelType
            Existing object to be updated
        obj_in : UpdateSchemaType
            Update data to validate
            
        Raises
        ------
        HTTPException
            If validation fails
        """
        pass
    
    def _validate_remove(self, db: Session, db_obj: ModelType) -> None:
        """
        Validate remove operation by business rules.
        
        Override this method to implement specific business validations.
        
        Parameters
        ----------
        db : Session
            Database session
        db_obj : ModelType
            Object to be removed
            
        Raises
        ------
        HTTPException
            If validation fails
        """
        pass
