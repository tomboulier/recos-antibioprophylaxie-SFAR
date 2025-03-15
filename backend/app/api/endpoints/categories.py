"""
API endpoints for category management.

This module defines the API routes for creating, reading, updating, and deleting
surgical categories.
"""

import logging
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_category_service
from app.core.database import get_db
from app.schemas import schemas
from app.services.services import CategoryService

# Get logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


@router.get("/", response_model=List[schemas.Category])
def read_categories(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category_service: CategoryService = Depends(get_category_service),
) -> Any:
    """
    Retrieve all categories.
    
    Parameters
    ----------
    db : Session
        Database session
    skip : int, optional
        Number of records to skip, by default 0
    limit : int, optional
        Maximum number of records to return, by default 100
    category_service : CategoryService
        Category service instance
        
    Returns
    -------
    List[schemas.Category]
        List of categories
    """
    categories = category_service.get_multi(db, skip=skip, limit=limit)
    return categories


@router.get("/{id}", response_model=schemas.Category)
def read_category(
    *,
    db: Session = Depends(get_db),
    id: int,
    category_service: CategoryService = Depends(get_category_service),
) -> Any:
    """
    Get a specific category by ID.
    
    Parameters
    ----------
    db : Session
        Database session
    id : int
        Category ID
    category_service : CategoryService
        Category service instance
        
    Returns
    -------
    schemas.Category
        The requested category
        
    Raises
    ------
    HTTPException
        If the category is not found
    """
    category = category_service.get(db=db, id=id)
    return category


@router.post("/", response_model=schemas.Category, status_code=status.HTTP_201_CREATED)
def create_category(
    *,
    db: Session = Depends(get_db),
    category_in: schemas.CategoryCreate,
    category_service: CategoryService = Depends(get_category_service),
) -> Any:
    """
    Create a new category.
    
    Parameters
    ----------
    db : Session
        Database session
    category_in : schemas.CategoryCreate
        Category data
    category_service : CategoryService
        Category service instance
        
    Returns
    -------
    schemas.Category
        The created category
        
    Raises
    ------
    HTTPException
        If a category with the same name already exists
    """
    category = category_service.create(db=db, obj_in=category_in)
    return category


@router.put("/{id}", response_model=schemas.Category)
def update_category(
    *,
    db: Session = Depends(get_db),
    id: int,
    category_in: schemas.CategoryUpdate,
    category_service: CategoryService = Depends(get_category_service),
) -> Any:
    """
    Update a category.
    
    Parameters
    ----------
    db : Session
        Database session
    id : int
        Category ID
    category_in : schemas.CategoryUpdate
        Category update data
    category_service : CategoryService
        Category service instance
        
    Returns
    -------
    schemas.Category
        The updated category
        
    Raises
    ------
    HTTPException
        If the category is not found
    """
    category = category_service.update(db=db, id=id, obj_in=category_in)
    return category


@router.delete("/{id}", response_model=schemas.Category)
def delete_category(
    *,
    db: Session = Depends(get_db),
    id: int,
    category_service: CategoryService = Depends(get_category_service),
) -> Any:
    """
    Delete a category.
    
    Parameters
    ----------
    db : Session
        Database session
    id : int
        Category ID
    category_service : CategoryService
        Category service instance
        
    Returns
    -------
    schemas.Category
        The deleted category
        
    Raises
    ------
    HTTPException
        If the category is not found
    """
    category = category_service.remove(db=db, id=id)
    return category
