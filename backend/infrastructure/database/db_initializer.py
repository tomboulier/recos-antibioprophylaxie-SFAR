"""
Module d'initialisation de la base de données pour Docker.
Ce script sera exécuté au démarrage du conteneur Docker pour s'assurer
que la base de données est correctement initialisée.
"""
import os
import sys
import logging
from pathlib import Path

# Configurer le logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ajouter le répertoire racine au PATH pour permettre les imports
backend_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(backend_dir))

# Importer après avoir ajouté le répertoire au PATH
from infrastructure.persistance.database import Base, engine
from app.models.models import Procedure, Category, Antibiotic, Recommendation
from scripts.init_db import init_db

def main():
    """
    Initialise la base de données si elle n'existe pas déjà.
    """
    try:
        # Vérifier si un fichier de base de données existe déjà
        db_path = os.environ.get("DATABASE_URL", "").replace("sqlite:///", "")
        
        # Si pas de DB_URL, utiliser un chemin par défaut
        if not db_path:
            db_path = str(backend_dir / "antibio.db")
            os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
            logger.info(f"Utilisation de la base de données par défaut: {db_path}")
        
        # Créer les tables si elles n'existent pas
        logger.info("Création des tables de la base de données...")
        Base.metadata.create_all(bind=engine)
        
        # Vérifier si la base de données contient déjà des données
        from sqlalchemy.orm import Session
        with Session(engine) as session:
            procedure_count = session.query(Procedure).count()
            
            if procedure_count == 0:
                logger.info("Base de données vide, initialisation des données...")
                # Initialiser avec les données de test/développement
                init_db()
                logger.info("Base de données initialisée avec succès!")
            else:
                logger.info(f"Base de données déjà initialisée ({procedure_count} procédures trouvées)")
                
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation de la base de données: {e}")
        raise

if __name__ == "__main__":
    main()
