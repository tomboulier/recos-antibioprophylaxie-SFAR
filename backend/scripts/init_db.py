#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script d'initialisation de la base de données avec des données de test.

Ce script permet de créer des données de test pour la base de données
utilisée par l'API d'antibioprophylaxie SFAR.
"""

import logging
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.models import Antibiotic, Category, Procedure, Recommendation

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_categories(db: Session) -> Dict[str, int]:
    """
    Crée des catégories chirurgicales de test.

    Paramètres
    ----------
    db : Session
        Session de base de données SQLAlchemy

    Retourne
    --------
    Dict[str, int]
        Dictionnaire associant les noms des catégories à leurs identifiants
    """
    categories = [
        Category(name="Neurochirurgie", description="Chirurgie du système nerveux central et périphérique"),
        Category(name="Chirurgie digestive", description="Chirurgie de l'appareil digestif"),
        Category(name="Chirurgie orthopédique", description="Chirurgie de l'appareil locomoteur"),
        Category(name="Chirurgie cardiovasculaire", description="Chirurgie cardiaque et vasculaire"),
        Category(name="Chirurgie thoracique", description="Chirurgie du thorax"),
    ]

    db.add_all(categories)
    db.commit()

    # Récupérer les IDs des catégories créées
    for category in categories:
        db.refresh(category)

    logger.info(f"Créé {len(categories)} catégories chirurgicales")
    return {category.name: category.id for category in categories}


def create_antibiotics(db: Session) -> Dict[str, int]:
    """
    Crée des antibiotiques de test.

    Paramètres
    ----------
    db : Session
        Session de base de données SQLAlchemy

    Retourne
    --------
    Dict[str, int]
        Dictionnaire associant les noms des antibiotiques à leurs identifiants
    """
    antibiotics = [
        Antibiotic(
            name="Céfazoline",
            generic_name="Céfazoline",
            description="Céphalosporine de première génération",
            dosage_info="2g IV (4g si >120kg)",
            contraindications="Allergie aux bêta-lactamines",
        ),
        Antibiotic(
            name="Clindamycine",
            generic_name="Clindamycine",
            description="Antibiotique de la famille des lincosamides",
            dosage_info="600-900mg IV",
            contraindications="Antécédents de colite pseudomembraneuse",
        ),
        Antibiotic(
            name="Vancomycine",
            generic_name="Vancomycine",
            description="Glycopeptide actif sur les bactéries à Gram positif",
            dosage_info="15mg/kg IV (max 2g)",
            contraindications="Insuffisance rénale sévère",
        ),
    ]

    db.add_all(antibiotics)
    db.commit()

    # Récupérer les IDs des antibiotiques créés
    for antibiotic in antibiotics:
        db.refresh(antibiotic)

    logger.info(f"Créé {len(antibiotics)} antibiotiques")
    return {antibiotic.name: antibiotic.id for antibiotic in antibiotics}


def create_procedures(
    db: Session, category_ids: Dict[str, int]
) -> Dict[str, int]:
    """
    Crée des procédures chirurgicales de test.

    Paramètres
    ----------
    db : Session
        Session de base de données SQLAlchemy
    category_ids : Dict[str, int]
        Dictionnaire associant les noms des catégories à leurs identifiants

    Retourne
    --------
    Dict[str, int]
        Dictionnaire associant les noms des procédures à leurs identifiants
    """
    # Récupérer les objets Category pour les associations many-to-many
    neuro_category = db.query(Category).get(category_ids["Neurochirurgie"])
    digestive_category = db.query(Category).get(category_ids["Chirurgie digestive"])
    ortho_category = db.query(Category).get(category_ids["Chirurgie orthopédique"])
    cardio_category = db.query(Category).get(category_ids["Chirurgie cardiovasculaire"])
    thoracic_category = db.query(Category).get(category_ids["Chirurgie thoracique"])

    procedures = [
        Procedure(
            name="Dérivation ventriculaire externe (DVE)",
            description="Mise en place d'un cathéter dans un ventricule cérébral pour drainage du LCR",
            risk_factors="Infection, hémorragie intracérébrale",
            categories=[neuro_category],
        ),
        Procedure(
            name="Dérivation lombaire externe (DLE)",
            description="Mise en place d'un cathéter dans l'espace sous-arachnoïdien lombaire pour drainage du LCR",
            risk_factors="Infection, céphalées post-ponction, engagement cérébral",
            categories=[neuro_category],
        ),
        Procedure(
            name="Dérivation ventriculo-péritonéale (DVP)",
            description="Système de shunt permanent entre ventricule cérébral et cavité péritonéale",
            risk_factors="Infection, obstruction, hyperdrainage",
            categories=[neuro_category],
        ),
        Procedure(
            name="Appendicectomie",
            description="Ablation chirurgicale de l'appendice",
            risk_factors="Infection du site opératoire, abcès intra-abdominal",
            categories=[digestive_category],
        ),
        Procedure(
            name="Prothèse totale de hanche",
            description="Remplacement articulaire de la hanche",
            risk_factors="Infection prothétique, luxation, fracture périprothétique",
            categories=[ortho_category],
        ),
        Procedure(
            name="Pontage aorto-coronarien",
            description="Création d'un pontage vasculaire pour contourner une obstruction coronarienne",
            risk_factors="Infection sternale, médiastinite",
            categories=[cardio_category],
        ),
        Procedure(
            name="Lobectomie pulmonaire",
            description="Exérèse d'un lobe pulmonaire",
            risk_factors="Infection pulmonaire, fistule bronchique",
            categories=[thoracic_category],
        ),
    ]

    db.add_all(procedures)
    db.commit()

    # Récupérer les IDs des procédures créées
    for procedure in procedures:
        db.refresh(procedure)

    logger.info(f"Créé {len(procedures)} procédures chirurgicales")
    return {procedure.name: procedure.id for procedure in procedures}


def create_recommendations(
    db: Session, procedure_ids: Dict[str, int], antibiotic_ids: Dict[str, int]
) -> None:
    """
    Crée des recommandations d'antibioprophylaxie de test.

    Paramètres
    ----------
    db : Session
        Session de base de données SQLAlchemy
    procedure_ids : Dict[str, int]
        Dictionnaire associant les noms des procédures à leurs identifiants
    antibiotic_ids : Dict[str, int]
        Dictionnaire associant les noms des antibiotiques à leurs identifiants
    """
    recommendations = [
        Recommendation(
            procedure_id=procedure_ids["Dérivation ventriculaire externe (DVE)"],
            antibiotic_id=antibiotic_ids["Céfazoline"],
            dosage="2g IV (4g si >120kg)",
            timing="30 minutes avant l'incision",
            duration="Dose unique préopératoire",
            alternative=False,
            evidence_level="Grade I",
            notes="Réinjection per-opératoire (1g) si durée >4h",
        ),
        Recommendation(
            procedure_id=procedure_ids["Dérivation ventriculaire externe (DVE)"],
            antibiotic_id=antibiotic_ids["Vancomycine"],
            dosage="15mg/kg IV (max 2g)",
            timing="120 minutes avant l'incision",
            duration="Dose unique préopératoire",
            alternative=True,
            evidence_level="Grade I",
            notes="En cas d'allergie aux bêta-lactamines ou de colonisation connue à SARM",
        ),
        Recommendation(
            procedure_id=procedure_ids["Prothèse totale de hanche"],
            antibiotic_id=antibiotic_ids["Céfazoline"],
            dosage="2g IV (4g si >120kg)",
            timing="30 minutes avant l'incision",
            duration="24h maximum",
            alternative=False,
            evidence_level="Grade I",
            notes="Réinjection per-opératoire (1g) si durée >4h ou saignement >1.5L",
        ),
        Recommendation(
            procedure_id=procedure_ids["Appendicectomie"],
            antibiotic_id=antibiotic_ids["Céfazoline"],
            dosage="2g IV (4g si >120kg)",
            timing="30 minutes avant l'incision",
            duration="Dose unique préopératoire",
            alternative=False,
            evidence_level="Grade I",
            notes="En cas d'appendicite non compliquée",
        ),
    ]

    db.add_all(recommendations)
    db.commit()

    logger.info(f"Créé {len(recommendations)} recommandations d'antibioprophylaxie")


def init_db() -> None:
    """
    Initialise la base de données avec des données de test.
    """
    db = SessionLocal()
    try:
        # Vérifier si la base de données est déjà initialisée
        existing_categories = db.query(Category).count()
        if existing_categories > 0:
            logger.info("La base de données contient déjà des données")
            return

        # Créer les données de test
        logger.info("Initialisation de la base de données avec des données de test...")
        category_ids = create_categories(db)
        antibiotic_ids = create_antibiotics(db)
        procedure_ids = create_procedures(db, category_ids)
        create_recommendations(db, procedure_ids, antibiotic_ids)
        
        logger.info("Initialisation de la base de données terminée avec succès")
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
