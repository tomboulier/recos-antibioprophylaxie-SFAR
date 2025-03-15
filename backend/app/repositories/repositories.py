"""
Repository implementations for domain entities.

This module provides concrete repository implementations for all domain entities,
extending the base repository with specific operations when needed.
"""

import logging
from typing import List, Optional, Union

from sqlalchemy.orm import Session

from app.models.models import Antibiotic, Category, Procedure, Recommendation
from app.repositories.base_repository import BaseRepository
from app.schemas import schemas

# Get logger
logger = logging.getLogger(__name__)


class CategoryRepository(BaseRepository[Category, schemas.CategoryCreate, schemas.CategoryUpdate]):
    """Repository for Category entity."""

    def __init__(self):
        """Initialize with Category model."""
        super().__init__(Category)
    
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
        return db.query(Category).filter(Category.name == name).first()


class ProcedureRepository(BaseRepository[Procedure, schemas.ProcedureCreate, schemas.ProcedureUpdate]):
    """Repository for Procedure entity."""

    def __init__(self):
        """Initialize with Procedure model."""
        super().__init__(Procedure)
    
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
        return db.query(Procedure).filter(Procedure.name == name).first()
    
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
        return (
            db.query(Procedure)
            .join(Procedure.categories)
            .filter(Category.id == category_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create_with_categories(
        self, db: Session, *, obj_in: schemas.ProcedureCreate
    ) -> Procedure:
        """
        Create a procedure with category associations.
        
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
        """
        # Extract category IDs
        category_ids = obj_in.category_ids
        
        # Create procedure object without category_ids
        obj_in_data = obj_in.model_dump(exclude={"category_ids"})
        db_obj = Procedure(**obj_in_data)
        
        # Add categories
        if category_ids:
            categories = db.query(Category).filter(Category.id.in_(category_ids)).all()
            db_obj.categories = categories
        
        # Save to database
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        logger.info(f"Created procedure {db_obj.name} with ID {db_obj.id} and {len(db_obj.categories)} categories")
        return db_obj
    
    def update_with_categories(
        self, db: Session, *, db_obj: Procedure, obj_in: Union[schemas.ProcedureUpdate, dict]
    ) -> Procedure:
        """
        Update a procedure including its category associations.
        
        Parameters
        ----------
        db : Session
            Database session
        db_obj : Procedure
            Existing procedure to update
        obj_in : Union[schemas.ProcedureUpdate, dict]
            Schema or dict with update data
            
        Returns
        -------
        Procedure
            The updated procedure
        """
        # Handle dict or schema
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        # Handle categories separately
        category_ids = update_data.pop("category_ids", None)
        
        # Update procedure fields
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        
        # Update categories if provided
        if category_ids is not None:
            categories = db.query(Category).filter(Category.id.in_(category_ids)).all()
            db_obj.categories = categories
        
        # Save to database
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        logger.info(f"Updated procedure {db_obj.name} with ID {db_obj.id}")
        return db_obj


class AntibioticRepository(BaseRepository[Antibiotic, schemas.AntibioticCreate, schemas.AntibioticUpdate]):
    """Repository for Antibiotic entity."""

    def __init__(self):
        """Initialize with Antibiotic model."""
        super().__init__(Antibiotic)
    
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
        return db.query(Antibiotic).filter(Antibiotic.name == name).first()


class RecommendationRepository(BaseRepository[Recommendation, schemas.RecommendationCreate, schemas.RecommendationUpdate]):
    """Repository for Recommendation entity."""

    def __init__(self):
        """Initialize with Recommendation model."""
        super().__init__(Recommendation)
    
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
        return db.query(Recommendation).filter(Recommendation.procedure_id == procedure_id).all()
    
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
        return (
            db.query(Recommendation)
            .filter(Recommendation.procedure_id == procedure_id, Recommendation.alternative == True)
            .all()
        )
