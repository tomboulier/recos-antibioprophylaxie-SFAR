"""
Adaptateurs pour convertir entre modèles ORM et schémas Pydantic.

Ce module fournit des fonctions pour faciliter la conversion entre les modèles
SQLAlchemy et les schémas Pydantic, en particulier pour gérer les problèmes
de sérialisation dans les versions récentes.
"""

import logging
from typing import Any, Dict, List, Type, TypeVar

from pydantic import BaseModel

from app.models.models import Procedure


# Configuration du logger
logger = logging.getLogger(__name__)

# Types génériques pour l'inférence de type
T = TypeVar('T', bound=BaseModel)
M = TypeVar('M')


def model_to_dict(obj: Any) -> Dict[str, Any]:
    """
    Convertit un modèle SQLAlchemy en dictionnaire.
    
    Paramètres
    ----------
    obj : Any
        Objet SQLAlchemy à convertir
        
    Retourne
    --------
    Dict[str, Any]
        Dictionnaire des attributs de l'objet
    """
    data = {}
    for c in obj.__table__.columns:
        attr_name = c.name
        data[attr_name] = getattr(obj, attr_name)
    
    return data


def convert_orm_to_schema(orm_obj: Any, schema_class: Type[T]) -> T:
    """
    Convertit un objet ORM SQLAlchemy en un modèle Pydantic.
    
    Paramètres
    ----------
    orm_obj : Any
        Objet ORM à convertir
    schema_class : Type[T]
        Classe du schéma Pydantic cible
        
    Retourne
    --------
    T
        Instance du schéma Pydantic
    """
    obj_dict = model_to_dict(orm_obj)
    
    # Gestion des relations
    if hasattr(orm_obj, 'categories') and hasattr(schema_class, 'categories'):
        obj_dict['categories'] = [model_to_dict(cat) for cat in orm_obj.categories]
    
    if hasattr(orm_obj, 'recommendations') and hasattr(schema_class, 'recommendations'):
        obj_dict['recommendations'] = [model_to_dict(rec) for rec in orm_obj.recommendations]
    
    if hasattr(orm_obj, 'procedure') and hasattr(schema_class, 'procedure'):
        obj_dict['procedure'] = model_to_dict(orm_obj.procedure)
    
    if hasattr(orm_obj, 'antibiotic') and hasattr(schema_class, 'antibiotic'):
        obj_dict['antibiotic'] = model_to_dict(orm_obj.antibiotic)
    
    # Conversion des noms d'attributs pour la correspondance avec les schémas Pydantic
    if isinstance(orm_obj, Procedure):
        if 'name' in obj_dict:
            obj_dict['name'] = obj_dict['name']
        if 'risk_factors' in obj_dict:
            obj_dict['risk_factors'] = obj_dict['risk_factors']
    
    return schema_class(**obj_dict)


def convert_list_orm_to_schema(orm_list: List[Any], schema_class: Type[T]) -> List[T]:
    """
    Convertit une liste d'objets ORM en liste de modèles Pydantic.
    
    Paramètres
    ----------
    orm_list : List[Any]
        Liste d'objets ORM à convertir
    schema_class : Type[T]
        Classe du schéma Pydantic cible
        
    Retourne
    --------
    List[T]
        Liste d'instances du schéma Pydantic
    """
    return [convert_orm_to_schema(item, schema_class) for item in orm_list]
