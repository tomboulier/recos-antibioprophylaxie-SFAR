"""
API endpoints for antibiotic management.

This module defines the API routes for creating, reading, updating, and deleting
antibiotics.
"""

import logging
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_antibiotic_service
from app.core.database import get_db
from app.schemas import schemas
from app.services.services import AntibioticService

# Get logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


@router.get("/", response_model=List[schemas.Antibiotic])
def read_antibiotics(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    antibiotic_service: AntibioticService = Depends(get_antibiotic_service),
) -> Any:
    """
    Retrieve all antibiotics.
    
    Parameters
    ----------
    db : Session
        Database session
    skip : int, optional
        Number of records to skip, by default 0
    limit : int, optional
        Maximum number of records to return, by default 100
    antibiotic_service : AntibioticService
        Antibiotic service instance
        
    Returns
    -------
    List[schemas.Antibiotic]
        List of antibiotics
    """
    antibiotics = antibiotic_service.get_multi(db, skip=skip, limit=limit)
    return antibiotics


@router.get("/{id}", response_model=schemas.Antibiotic)
def read_antibiotic(
    *,
    db: Session = Depends(get_db),
    id: int,
    antibiotic_service: AntibioticService = Depends(get_antibiotic_service),
) -> Any:
    """
    Get a specific antibiotic by ID.
    
    Parameters
    ----------
    db : Session
        Database session
    id : int
        Antibiotic ID
    antibiotic_service : AntibioticService
        Antibiotic service instance
        
    Returns
    -------
    schemas.Antibiotic
        The requested antibiotic
        
    Raises
    ------
    HTTPException
        If the antibiotic is not found
    """
    antibiotic = antibiotic_service.get(db=db, id=id)
    return antibiotic


@router.post("/", response_model=schemas.Antibiotic, status_code=status.HTTP_201_CREATED)
def create_antibiotic(
    *,
    db: Session = Depends(get_db),
    antibiotic_in: schemas.AntibioticCreate,
    antibiotic_service: AntibioticService = Depends(get_antibiotic_service),
) -> Any:
    """
    Create a new antibiotic.
    
    Parameters
    ----------
    db : Session
        Database session
    antibiotic_in : schemas.AntibioticCreate
        Antibiotic data
    antibiotic_service : AntibioticService
        Antibiotic service instance
        
    Returns
    -------
    schemas.Antibiotic
        The created antibiotic
        
    Raises
    ------
    HTTPException
        If an antibiotic with the same name already exists
    """
    antibiotic = antibiotic_service.create(db=db, obj_in=antibiotic_in)
    return antibiotic


@router.put("/{id}", response_model=schemas.Antibiotic)
def update_antibiotic(
    *,
    db: Session = Depends(get_db),
    id: int,
    antibiotic_in: schemas.AntibioticUpdate,
    antibiotic_service: AntibioticService = Depends(get_antibiotic_service),
) -> Any:
    """
    Update an antibiotic.
    
    Parameters
    ----------
    db : Session
        Database session
    id : int
        Antibiotic ID
    antibiotic_in : schemas.AntibioticUpdate
        Antibiotic update data
    antibiotic_service : AntibioticService
        Antibiotic service instance
        
    Returns
    -------
    schemas.Antibiotic
        The updated antibiotic
        
    Raises
    ------
    HTTPException
        If the antibiotic is not found
    """
    antibiotic = antibiotic_service.update(db=db, id=id, obj_in=antibiotic_in)
    return antibiotic


@router.delete("/{id}", response_model=schemas.Antibiotic)
def delete_antibiotic(
    *,
    db: Session = Depends(get_db),
    id: int,
    antibiotic_service: AntibioticService = Depends(get_antibiotic_service),
) -> Any:
    """
    Delete an antibiotic.
    
    Parameters
    ----------
    db : Session
        Database session
    id : int
        Antibiotic ID
    antibiotic_service : AntibioticService
        Antibiotic service instance
        
    Returns
    -------
    schemas.Antibiotic
        The deleted antibiotic
        
    Raises
    ------
    HTTPException
        If the antibiotic is not found
    """
    antibiotic = antibiotic_service.remove(db=db, id=id)
    return antibiotic
