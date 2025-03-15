"""
Entité représentant un antibiotique.

Ce module définit la classe Antibiotique qui modélise les antibiotiques
utilisés dans les recommandations d'antibioprophylaxie de la SFAR.
"""
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

from domaine.entites.entite_base import EntiteBase


@dataclass
class Antibiotique(EntiteBase):
    """
    Antibiotique utilisé dans les recommandations SFAR.
    
    Cette classe représente un antibiotique pouvant être utilisé 
    en antibioprophylaxie selon les recommandations SFAR.
    
    Attributs
    ---------
    nom : str
        Nom commercial de l'antibiotique
    nom_generique : Optional[str]
        Nom générique ou DCI (Dénomination Commune Internationale)
    description : Optional[str]
        Description de l'antibiotique
    posologie_standard : Optional[str]
        Informations générales sur la posologie standard
    contre_indications : Optional[str]
        Contre-indications notables
    """
    
    # Champs obligatoires en premier
    nom: str
    # Champs optionnels ensuite
    nom_generique: Optional[str] = None
    description: Optional[str] = None
    posologie_standard: Optional[str] = None
    contre_indications: Optional[str] = None
    # Redéfinition des champs hérités avec leurs valeurs par défaut
    id: Optional[int] = None
    date_creation: datetime = field(default_factory=datetime.utcnow)
    date_modification: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validation après initialisation."""
        if not self.nom:
            raise ValueError("Le nom de l'antibiotique ne peut pas être vide")
