"""
Domain models for the antibioprophylaxis recommendation system.

This module defines the SQLAlchemy ORM models that represent the domain
entities of the antibioprophylaxis recommendation system.
"""

from typing import List, Optional

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


# Association table for many-to-many relationship between Category and Procedure
category_procedure = Table(
    "category_procedure",
    Base.metadata,
    Column("category_id", Integer, ForeignKey("category.id"), primary_key=True),
    Column("procedure_id", Integer, ForeignKey("procedure.id"), primary_key=True),
)


class Category(Base):
    """
    Surgical category model.
    
    Represents a category of surgical procedures (e.g., cardiology, orthopedics).
    
    Attributes
    ----------
    name : str
        Name of the surgical category
    description : str
        Description of the category
    procedures : List[Procedure]
        List of procedures in this category
    """
    
    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    procedures: Mapped[List["Procedure"]] = relationship(
        secondary=category_procedure, back_populates="categories"
    )
    
    def __repr__(self) -> str:
        """String representation of the category."""
        return f"<Category {self.name}>"


class Procedure(Base):
    """
    Surgical procedure model.
    
    Represents a specific surgical procedure that requires antibioprophylaxis.
    
    Attributes
    ----------
    name : str
        Name of the surgical procedure
    description : str
        Description of the procedure
    risk_factors : str
        Risk factors associated with the procedure
    categories : List[Category]
        Categories this procedure belongs to
    recommendations : List[Recommendation]
        Antibioprophylaxis recommendations for this procedure
    """
    
    name: Mapped[str] = mapped_column(String(200), index=True, nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    risk_factors: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    categories: Mapped[List["Category"]] = relationship(
        secondary=category_procedure, back_populates="procedures"
    )
    recommendations: Mapped[List["Recommendation"]] = relationship(
        back_populates="procedure", cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        """String representation of the procedure."""
        return f"<Procedure {self.name}>"


class Antibiotic(Base):
    """
    Antibiotic model.
    
    Represents an antibiotic that can be used for prophylaxis.
    
    Attributes
    ----------
    name : str
        Name of the antibiotic
    generic_name : str
        Generic name of the antibiotic
    description : str
        Description of the antibiotic
    dosage_info : str
        General dosage information
    contraindications : str
        Contraindications for the antibiotic
    recommendations : List[Recommendation]
        Recommendations that include this antibiotic
    """
    
    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False, unique=True)
    generic_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    dosage_info: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    contraindications: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    recommendations: Mapped[List["Recommendation"]] = relationship(back_populates="antibiotic")
    
    def __repr__(self) -> str:
        """String representation of the antibiotic."""
        return f"<Antibiotic {self.name}>"


class Recommendation(Base):
    """
    Antibioprophylaxis recommendation model.
    
    Represents a specific recommendation for antibioprophylaxis for a procedure.
    
    Attributes
    ----------
    procedure_id : int
        ID of the procedure this recommendation applies to
    antibiotic_id : int
        ID of the recommended antibiotic
    dosage : str
        Recommended dosage
    timing : str
        Timing of administration (e.g., "30-60 minutes before incision")
    duration : str
        Duration of prophylaxis
    alternative : bool
        Whether this is an alternative recommendation (for allergies, etc.)
    special_populations : str
        Special considerations for specific patient populations
    evidence_level : str
        Level of evidence for this recommendation
    notes : str
        Additional notes or warnings
    """
    
    procedure_id: Mapped[int] = mapped_column(Integer, ForeignKey("procedure.id"), nullable=False)
    antibiotic_id: Mapped[int] = mapped_column(Integer, ForeignKey("antibiotic.id"), nullable=False)
    dosage: Mapped[str] = mapped_column(String(200), nullable=False)
    timing: Mapped[str] = mapped_column(String(200), nullable=False)
    duration: Mapped[str] = mapped_column(String(200), nullable=False)
    alternative: Mapped[bool] = mapped_column(Boolean, default=False)
    special_populations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    evidence_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    procedure: Mapped["Procedure"] = relationship(back_populates="recommendations")
    antibiotic: Mapped["Antibiotic"] = relationship(back_populates="recommendations")
    
    def __repr__(self) -> str:
        """String representation of the recommendation."""
        return f"<Recommendation {self.id} for {self.procedure.name} using {self.antibiotic.name}>"
