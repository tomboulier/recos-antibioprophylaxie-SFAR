"""
API dependencies module.

This module provides FastAPI dependency injection functions that can be used
across different API endpoints.
"""

import logging
from typing import Generator

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.services import (
    AntibioticService,
    CategoryService,
    ProcedureService,
    RecommendationService,
)

# Get logger
logger = logging.getLogger(__name__)


def get_category_service() -> CategoryService:
    """
    Get CategoryService instance for dependency injection.
    
    Returns
    -------
    CategoryService
        Service for category operations
    """
    return CategoryService()


def get_procedure_service() -> ProcedureService:
    """
    Get ProcedureService instance for dependency injection.
    
    Returns
    -------
    ProcedureService
        Service for procedure operations
    """
    return ProcedureService()


def get_antibiotic_service() -> AntibioticService:
    """
    Get AntibioticService instance for dependency injection.
    
    Returns
    -------
    AntibioticService
        Service for antibiotic operations
    """
    return AntibioticService()


def get_recommendation_service() -> RecommendationService:
    """
    Get RecommendationService instance for dependency injection.
    
    Returns
    -------
    RecommendationService
        Service for recommendation operations
    """
    return RecommendationService()
