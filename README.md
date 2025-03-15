# Application de Recommandations d'Antibioprophylaxie SFAR

Une application web et mobile pour aider les anesthésistes à trouver la bonne antibioprophylaxie selon les recommandations de la Société Française d'Anesthésie et de Réanimation (SFAR).

## Présentation

Cette application a pour objectif de faciliter l'accès et la consultation des recommandations officielles de la SFAR concernant l'antibioprophylaxie en chirurgie et médecine interventionnelle. Elle permet aux anesthésistes et autres professionnels de santé de trouver rapidement les protocoles d'antibioprophylaxie adaptés à chaque type d'intervention chirurgicale.

## Architecture

Le projet suit les principes de la Clean Architecture (Architecture Hexagonale) et du Domain-Driven Design :

- **Domaine** : Le cœur métier de l'application, contenant les entités et règles métier sans dépendances extérieures
- **Application** : Les cas d'utilisation orchestrant les opérations métier
- **Infrastructure** : Les adaptateurs techniques pour la persistance et l'API
- **Présentation** : L'interface utilisateur

### Technologies utilisées

- **Backend** : Python avec FastAPI
- **Frontend** : Vue.js avec Tailwind CSS
- **Base de données** : SQLite (développement) / PostgreSQL (production)
- **Documentation** : MkDocs Material
- **Gestion des dépendances** : uv + pyproject.toml

## Structure du projet

```
antibioprophylaxie-sfar/
├── backend/                 # Backend Python avec FastAPI
│   ├── domaine/             # Cœur métier (en français)
│   ├── application/         # Cas d'utilisation
│   ├── infrastructure/      # Adaptateurs techniques
│   └── presentation/        # Interface API
├── frontend/                # Frontend Vue.js avec Tailwind CSS
│   ├── public/              # Assets statiques (logos, favicon)
│   ├── src/                 # Sources de l'application
│   │   ├── assets/          # Ressources (CSS, images)
│   │   ├── components/      # Composants Vue.js 
│   │   └── App.vue          # Composant racine
│   ├── index.html           # Point d'entrée HTML
│   └── vite.config.js       # Configuration de Vite
└── docs/                    # Documentation
```

## Prérequis

- Python 3.10 ou supérieur
- [uv](https://github.com/astral-sh/uv) (gestionnaire de paquets Python ultra-rapide)
- Node.js 18 ou supérieur (pour le frontend)

## Installation

### Backend

1. Cloner le dépôt et se placer dans le répertoire du projet :

```bash
git clone <url-du-depot>
cd antibioprophylaxie-sfar
```

2. Créer et activer un environnement virtuel avec uv :

```bash
uv venv
source .venv/bin/activate  # sous Linux/macOS
# ou
.venv\Scripts\activate  # sous Windows
```

3. Installer les dépendances du backend :

```bash
cd backend
uv pip install -e ".[dev,test]"
```

4. Configurer la base de données :

```bash
# Instructions à venir
```

5. Lancer le serveur de développement :

```bash
uvicorn infrastructure.api.main:app --reload
```

### Frontend

1. Se placer dans le répertoire du frontend :

```bash
cd frontend
```

2. Installer les dépendances :

```bash
npm install
```

3. Lancer le serveur de développement :

```bash
npm run dev
```

L'application sera disponible à l'adresse http://localhost:5173/

## Tests

Le projet utilise pytest pour les tests unitaires et d'intégration :

```bash
# Exécuter tous les tests
cd backend
pytest

# Exécuter les tests avec rapport de couverture
pytest --cov=domaine,application,infrastructure

# Exécuter un fichier de test spécifique
pytest tests/domaine/test_entites.py
```

## Conventions de code

Le projet suit plusieurs conventions de qualité de code :

- **Formatage** : Black
- **Linting** : Flake8
- **Type hints** : vérification avec MyPy
- **Documentation** : Docstrings au format numpydoc
- **Tests** : Pytest
- **Commits** : Convention Conventional Commits

Vous pouvez exécuter les outils de qualité de code avec les commandes suivantes :

```bash
# Formatage automatique
black .

# Vérification du formatage
black --check .

# Linting
flake8

# Vérification des types
mypy .
```

## Licence

Ce projet est développé à des fins éducatives et de recherche.

## Références

- Recommandations Formalisées d'Experts - SFAR
