"""
Service implementations for domain entities.

This module provides concrete service implementations for all domain entities,
implementing business logic and validation rules.
"""

import logging
from typing import List, Optional, Union

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import Antibiotic, Category, Procedure, Recommendation
from app.repositories.repositories import (
    AntibioticRepository,
    CategoryRepository,
    ProcedureRepository,
    RecommendationRepository,
)
from app.schemas import schemas
from app.services.base_service import BaseService

# Get logger
logger = logging.getLogger(__name__)


class CategoryService(BaseService[Category, schemas.CategoryCreate, schemas.CategoryUpdate, CategoryRepository]):
    """Service for Category entity business logic."""

    def __init__(self, repository: Optional[CategoryRepository] = None):
        """
        Initialize with Category repository.
        
        Parameters
        ----------
        repository : Optional[CategoryRepository], optional
            Category repository instance, by default None
        """
        super().__init__(repository or CategoryRepository())
    
    def get_by_name(self, db: Session, *, name: str) -> Optional[Category]:
        """
        Get a category by its name.
        
        Parameters
        ----------
        db : Session
            Database session
        name : str
            Category name to search for
            
        Returns
        -------
        Optional[Category]
            The category if found, None otherwise
        """
        return self.repository.get_by_name(db=db, name=name)
    
    def _validate_create(self, db: Session, obj_in: schemas.CategoryCreate) -> None:
        """
        Validate category creation by business rules.
        
        Parameters
        ----------
        db : Session
            Database session
        obj_in : schemas.CategoryCreate
            Category data to validate
            
        Raises
        ------
        HTTPException
            If a category with the same name already exists
        """
        # Check if category with the same name already exists
        existing = self.get_by_name(db=db, name=obj_in.name)
        if existing:
            logger.warning(f"Attempted to create duplicate category with name '{obj_in.name}'")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with name '{obj_in.name}' already exists",
            )


class ProcedureService(BaseService[Procedure, schemas.ProcedureCreate, schemas.ProcedureUpdate, ProcedureRepository]):
    """Service for Procedure entity business logic."""

    def __init__(self, repository: Optional[ProcedureRepository] = None):
        """
        Initialize with Procedure repository.
        
        Parameters
        ----------
        repository : Optional[ProcedureRepository], optional
            Procedure repository instance, by default None
        """
        super().__init__(repository or ProcedureRepository())
    
    def get_by_name(self, db: Session, *, name: str) -> Optional[Procedure]:
        """
        Get a procedure by its name.
        
        Parameters
        ----------
        db : Session
            Database session
        name : str
            Procedure name to search for
            
        Returns
        -------
        Optional[Procedure]
            The procedure if found, None otherwise
        """
        return self.repository.get_by_name(db=db, name=name)
    
    def get_by_category(self, db: Session, *, category_id: int, skip: int = 0, limit: int = 100) -> List[Procedure]:
        """
        Get procedures by category ID.
        
        Parameters
        ----------
        db : Session
            Database session
        category_id : int
            Category ID to filter by
        skip : int, optional
            Number of records to skip, by default 0
        limit : int, optional
            Maximum number of records to return, by default 100
            
        Returns
        -------
        List[Procedure]
            List of procedures in the specified category
        """
        return self.repository.get_by_category(db=db, category_id=category_id, skip=skip, limit=limit)
    
    def create(self, db: Session, *, obj_in: schemas.ProcedureCreate) -> Procedure:
        """
        Create a new procedure with categories.
        
        Parameters
        ----------
        db : Session
            Database session
        obj_in : schemas.ProcedureCreate
            Schema with procedure data including category IDs
            
        Returns
        -------
        Procedure
            The created procedure
            
        Raises
        ------
        HTTPException
            If validation fails
        """
        self._validate_create(db, obj_in)
        return self.repository.create_with_categories(db=db, obj_in=obj_in)
    
    def update(
        self, db: Session, *, id: int, obj_in: Union[schemas.ProcedureUpdate, dict]
    ) -> Procedure:
        """
        Update a procedure including its category associations.
        
        Parameters
        ----------
        db : Session
            Database session
        id : int
            ID of the procedure to update
        obj_in : Union[schemas.ProcedureUpdate, dict]
            Schema or dict with update data
            
        Returns
        -------
        Procedure
            The updated procedure
            
        Raises
        ------
        HTTPException
            If the procedure is not found or validation fails
        """
        db_obj = self.get(db=db, id=id)  # This will raise 404 if not found
        self._validate_update(db, db_obj, obj_in)
        return self.repository.update_with_categories(db=db, db_obj=db_obj, obj_in=obj_in)
    
    def _validate_create(self, db: Session, obj_in: schemas.ProcedureCreate) -> None:
        """
        Validate procedure creation by business rules.
        
        Parameters
        ----------
        db : Session
            Database session
        obj_in : schemas.ProcedureCreate
            Procedure data to validate
            
        Raises
        ------
        HTTPException
            If a procedure with the same name already exists
            If specified categories don't exist
        """
        # Check if procedure with the same name already exists
        existing = self.get_by_name(db=db, name=obj_in.name)
        if existing:
            logger.warning(f"Attempted to create duplicate procedure with name '{obj_in.name}'")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Procedure with name '{obj_in.name}' already exists",
            )
        
        # Check if all specified categories exist
        category_repo = CategoryRepository()
        for category_id in obj_in.category_ids:
            if not category_repo.get(db=db, id=category_id):
                logger.warning(f"Attempted to use non-existent category ID {category_id}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Category with ID {category_id} does not exist",
                )


class AntibioticService(BaseService[Antibiotic, schemas.AntibioticCreate, schemas.AntibioticUpdate, AntibioticRepository]):
    """Service for Antibiotic entity business logic."""

    def __init__(self, repository: Optional[AntibioticRepository] = None):
        """
        Initialize with Antibiotic repository.
        
        Parameters
        ----------
        repository : Optional[AntibioticRepository], optional
            Antibiotic repository instance, by default None
        """
        super().__init__(repository or AntibioticRepository())
    
    def get_by_name(self, db: Session, *, name: str) -> Optional[Antibiotic]:
        """
        Get an antibiotic by its name.
        
        Parameters
        ----------
        db : Session
            Database session
        name : str
            Antibiotic name to search for
            
        Returns
        -------
        Optional[Antibiotic]
            The antibiotic if found, None otherwise
        """
        return self.repository.get_by_name(db=db, name=name)
    
    def _validate_create(self, db: Session, obj_in: schemas.AntibioticCreate) -> None:
        """
        Validate antibiotic creation by business rules.
        
        Parameters
        ----------
        db : Session
            Database session
        obj_in : schemas.AntibioticCreate
            Antibiotic data to validate
            
        Raises
        ------
        HTTPException
            If an antibiotic with the same name already exists
        """
        # Check if antibiotic with the same name already exists
        existing = self.get_by_name(db=db, name=obj_in.name)
        if existing:
            logger.warning(f"Attempted to create duplicate antibiotic with name '{obj_in.name}'")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Antibiotic with name '{obj_in.name}' already exists",
            )


class RecommendationService(BaseService[Recommendation, schemas.RecommendationCreate, schemas.RecommendationUpdate, RecommendationRepository]):
    """Service for Recommendation entity business logic."""

    def __init__(self, repository: Optional[RecommendationRepository] = None):
        """
        Initialize with Recommendation repository.
        
        Parameters
        ----------
        repository : Optional[RecommendationRepository], optional
            Recommendation repository instance, by default None
        """
        super().__init__(repository or RecommendationRepository())
    
    def get_by_procedure(self, db: Session, *, procedure_id: int) -> List[Recommendation]:
        """
        Get all recommendations for a specific procedure.
        
        Parameters
        ----------
        db : Session
            Database session
        procedure_id : int
            Procedure ID to filter by
            
        Returns
        -------
        List[Recommendation]
            List of recommendations for the procedure
        """
        return self.repository.get_by_procedure(db=db, procedure_id=procedure_id)
    
    def get_alternatives_for_procedure(self, db: Session, *, procedure_id: int) -> List[Recommendation]:
        """
        Get alternative recommendations for a specific procedure.
        
        These are typically used for patients with allergies.
        
        Parameters
        ----------
        db : Session
            Database session
        procedure_id : int
            Procedure ID to filter by
            
        Returns
        -------
        List[Recommendation]
            List of alternative recommendations for the procedure
        """
        return self.repository.get_alternatives_for_procedure(db=db, procedure_id=procedure_id)
    
    def _validate_create(self, db: Session, obj_in: schemas.RecommendationCreate) -> None:
        """
        Validate recommendation creation by business rules.
        
        Parameters
        ----------
        db : Session
            Database session
        obj_in : schemas.RecommendationCreate
            Recommendation data to validate
            
        Raises
        ------
        HTTPException
            If the procedure or antibiotic does not exist
        """
        # Check if procedure exists
        procedure_repo = ProcedureRepository()
        if not procedure_repo.get(db=db, id=obj_in.procedure_id):
            logger.warning(f"Attempted to create recommendation for non-existent procedure ID {obj_in.procedure_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Procedure with ID {obj_in.procedure_id} does not exist",
            )
        
        # Check if antibiotic exists
        antibiotic_repo = AntibioticRepository()
        if not antibiotic_repo.get(db=db, id=obj_in.antibiotic_id):
            logger.warning(f"Attempted to create recommendation with non-existent antibiotic ID {obj_in.antibiotic_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Antibiotic with ID {obj_in.antibiotic_id} does not exist",
            )
