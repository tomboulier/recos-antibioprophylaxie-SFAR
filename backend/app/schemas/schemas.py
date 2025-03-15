"""
API schema definitions using Pydantic models.

This module defines the Pydantic models used for request/response validation
and serialization in the API.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# Base schemas with shared attributes
class CategoryBase(BaseModel):
    """Base schema for Category."""
    
    name: str = Field(..., description="Category name", example="Orthopédie")
    description: Optional[str] = Field(None, description="Category description")


class CategoryCreate(CategoryBase):
    """Schema for creating a new Category."""
    
    pass


class CategoryUpdate(CategoryBase):
    """Schema for updating a Category."""
    
    name: Optional[str] = Field(None, description="Category name")


class CategoryInDB(CategoryBase):
    """Schema for Category stored in database."""
    
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic config."""
        
        from_attributes = True


class Category(CategoryInDB):
    """Schema for Category returned by API."""
    
    pass


# Procedure schemas
class ProcedureBase(BaseModel):
    """Base schema for Procedure."""
    
    name: str = Field(..., description="Procedure name", example="Chirurgie de la hanche")
    description: Optional[str] = Field(None, description="Procedure description")
    risk_factors: Optional[str] = Field(None, description="Risk factors for this procedure")


class ProcedureCreate(ProcedureBase):
    """Schema for creating a new Procedure."""
    
    category_ids: List[int] = Field(..., description="IDs of categories this procedure belongs to")


class ProcedureUpdate(ProcedureBase):
    """Schema for updating a Procedure."""
    
    name: Optional[str] = Field(None, description="Procedure name")
    category_ids: Optional[List[int]] = Field(None, description="IDs of categories")


class ProcedureInDB(ProcedureBase):
    """Schema for Procedure stored in database."""
    
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic config."""
        
        from_attributes = True


class ProcedureWithCategories(ProcedureInDB):
    """Schema for Procedure with its categories, returned by API."""
    
    categories: List[Category] = Field([], description="Categories this procedure belongs to")


# Antibiotic schemas
class AntibioticBase(BaseModel):
    """Base schema for Antibiotic."""
    
    name: str = Field(..., description="Antibiotic name", example="Céfazoline")
    generic_name: Optional[str] = Field(None, description="Generic name")
    description: Optional[str] = Field(None, description="Description of the antibiotic")
    dosage_info: Optional[str] = Field(None, description="General dosage information")
    contraindications: Optional[str] = Field(None, description="Contraindications")


class AntibioticCreate(AntibioticBase):
    """Schema for creating a new Antibiotic."""
    
    pass


class AntibioticUpdate(AntibioticBase):
    """Schema for updating an Antibiotic."""
    
    name: Optional[str] = Field(None, description="Antibiotic name")


class AntibioticInDB(AntibioticBase):
    """Schema for Antibiotic stored in database."""
    
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic config."""
        
        from_attributes = True


class Antibiotic(AntibioticInDB):
    """Schema for Antibiotic returned by API."""
    
    pass


# Recommendation schemas
class RecommendationBase(BaseModel):
    """Base schema for Recommendation."""
    
    procedure_id: int = Field(..., description="ID of the procedure")
    antibiotic_id: int = Field(..., description="ID of the recommended antibiotic")
    dosage: str = Field(..., description="Recommended dosage", example="2g IV")
    timing: str = Field(..., description="Timing of administration", example="30-60 minutes before incision")
    duration: str = Field(..., description="Duration of prophylaxis", example="Dose unique")
    alternative: bool = Field(False, description="Whether this is an alternative recommendation")
    special_populations: Optional[str] = Field(None, description="Special considerations for specific patient populations")
    evidence_level: Optional[str] = Field(None, description="Level of evidence", example="Grade 1+")
    notes: Optional[str] = Field(None, description="Additional notes or warnings")


class RecommendationCreate(RecommendationBase):
    """Schema for creating a new Recommendation."""
    
    pass


class RecommendationUpdate(RecommendationBase):
    """Schema for updating a Recommendation."""
    
    procedure_id: Optional[int] = Field(None, description="ID of the procedure")
    antibiotic_id: Optional[int] = Field(None, description="ID of the recommended antibiotic")
    dosage: Optional[str] = Field(None, description="Recommended dosage")
    timing: Optional[str] = Field(None, description="Timing of administration")
    duration: Optional[str] = Field(None, description="Duration of prophylaxis")
    alternative: Optional[bool] = Field(None, description="Whether this is an alternative recommendation")


class RecommendationInDB(RecommendationBase):
    """Schema for Recommendation stored in database."""
    
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic config."""
        
        from_attributes = True


class RecommendationFull(RecommendationInDB):
    """Full Recommendation schema with related entities."""
    
    procedure: ProcedureInDB
    antibiotic: Antibiotic
    
    class Config:
        """Pydantic config."""
        
        from_attributes = True


# Search and filter schemas
class ProcedureFilter(BaseModel):
    """Schema for filtering procedures."""
    
    name: Optional[str] = Field(None, description="Filter by name (partial match)")
    category_id: Optional[int] = Field(None, description="Filter by category ID")


class RecommendationFilter(BaseModel):
    """Schema for filtering recommendations."""
    
    procedure_id: Optional[int] = Field(None, description="Filter by procedure ID")
    antibiotic_id: Optional[int] = Field(None, description="Filter by antibiotic ID")
    alternative: Optional[bool] = Field(None, description="Filter by alternative status")
