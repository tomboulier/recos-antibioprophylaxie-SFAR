"""
API endpoints for procedure management.

This module defines the API routes for creating, reading, updating, and deleting
surgical procedures.
"""

import logging
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_procedure_service
from app.core.database import get_db
from app.schemas import schemas
from app.services.services import ProcedureService

# Get logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


@router.get("/", response_model=List[schemas.ProcedureWithCategories])
def read_procedures(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category_id: int = Query(None, description="Filter by category ID"),
    procedure_service: ProcedureService = Depends(get_procedure_service),
) -> Any:
    """
    Retrieve procedures with optional category filtering.
    
    Parameters
    ----------
    db : Session
        Database session
    skip : int, optional
        Number of records to skip, by default 0
    limit : int, optional
        Maximum number of records to return, by default 100
    category_id : int, optional
        Category ID to filter by, by default None
    procedure_service : ProcedureService
        Procedure service instance
        
    Returns
    -------
    List[schemas.ProcedureWithCategories]
        List of procedures with their categories
    """
    if category_id is not None:
        procedures = procedure_service.get_by_category(
            db, category_id=category_id, skip=skip, limit=limit
        )
    else:
        procedures = procedure_service.get_multi(db, skip=skip, limit=limit)
    
    return procedures


@router.get("/{id}", response_model=schemas.ProcedureWithCategories)
def read_procedure(
    *,
    db: Session = Depends(get_db),
    id: int,
    procedure_service: ProcedureService = Depends(get_procedure_service),
) -> Any:
    """
    Get a specific procedure by ID.
    
    Parameters
    ----------
    db : Session
        Database session
    id : int
        Procedure ID
    procedure_service : ProcedureService
        Procedure service instance
        
    Returns
    -------
    schemas.ProcedureWithCategories
        The requested procedure with its categories
        
    Raises
    ------
    HTTPException
        If the procedure is not found
    """
    procedure = procedure_service.get(db=db, id=id)
    return procedure


@router.post("/", response_model=schemas.ProcedureWithCategories, status_code=status.HTTP_201_CREATED)
def create_procedure(
    *,
    db: Session = Depends(get_db),
    procedure_in: schemas.ProcedureCreate,
    procedure_service: ProcedureService = Depends(get_procedure_service),
) -> Any:
    """
    Create a new procedure.
    
    Parameters
    ----------
    db : Session
        Database session
    procedure_in : schemas.ProcedureCreate
        Procedure data including category IDs
    procedure_service : ProcedureService
        Procedure service instance
        
    Returns
    -------
    schemas.ProcedureWithCategories
        The created procedure with its categories
        
    Raises
    ------
    HTTPException
        If a procedure with the same name already exists
        If any of the specified categories don't exist
    """
    procedure = procedure_service.create(db=db, obj_in=procedure_in)
    return procedure


@router.put("/{id}", response_model=schemas.ProcedureWithCategories)
def update_procedure(
    *,
    db: Session = Depends(get_db),
    id: int,
    procedure_in: schemas.ProcedureUpdate,
    procedure_service: ProcedureService = Depends(get_procedure_service),
) -> Any:
    """
    Update a procedure.
    
    Parameters
    ----------
    db : Session
        Database session
    id : int
        Procedure ID
    procedure_in : schemas.ProcedureUpdate
        Procedure update data
    procedure_service : ProcedureService
        Procedure service instance
        
    Returns
    -------
    schemas.ProcedureWithCategories
        The updated procedure with its categories
        
    Raises
    ------
    HTTPException
        If the procedure is not found
    """
    procedure = procedure_service.update(db=db, id=id, obj_in=procedure_in)
    return procedure


@router.delete("/{id}", response_model=schemas.ProcedureWithCategories)
def delete_procedure(
    *,
    db: Session = Depends(get_db),
    id: int,
    procedure_service: ProcedureService = Depends(get_procedure_service),
) -> Any:
    """
    Delete a procedure.
    
    Parameters
    ----------
    db : Session
        Database session
    id : int
        Procedure ID
    procedure_service : ProcedureService
        Procedure service instance
        
    Returns
    -------
    schemas.ProcedureWithCategories
        The deleted procedure with its categories
        
    Raises
    ------
    HTTPException
        If the procedure is not found
    """
    procedure = procedure_service.remove(db=db, id=id)
    return procedure


@router.get("/search/by-name", response_model=List[schemas.ProcedureWithCategories])
def search_procedures_by_name(
    *,
    db: Session = Depends(get_db),
    name: str = Query(..., min_length=3, description="Search term (minimum 3 characters)"),
    skip: int = 0,
    limit: int = 100,
    procedure_service: ProcedureService = Depends(get_procedure_service),
) -> Any:
    """
    Search procedures by name.
    
    Parameters
    ----------
    db : Session
        Database session
    name : str
        Search term (minimum 3 characters)
    skip : int, optional
        Number of records to skip, by default 0
    limit : int, optional
        Maximum number of records to return, by default 100
    procedure_service : ProcedureService
        Procedure service instance
        
    Returns
    -------
    List[schemas.ProcedureWithCategories]
        List of procedures matching the search term
    """
    # In a real implementation, you would add a specific search method to the service
    # For now, we'll use a simple filter on the name field
    procedures = procedure_service.get_multi(db=db, skip=skip, limit=limit)
    return [p for p in procedures if name.lower() in p.name.lower()]
