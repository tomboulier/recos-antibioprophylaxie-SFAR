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

### Option 1 : Installation locale

- Python 3.10 ou supérieur
- [uv](https://github.com/astral-sh/uv) (gestionnaire de paquets Python ultra-rapide)
- Node.js 18 ou supérieur (pour le frontend)

### Option 2 : Utilisation de Docker (recommandé)

- Docker
- Docker Compose

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

4. Lancer le serveur de développement :

```bash
# Depuis le répertoire backend
python -m uvicorn infrastructure.api.main:app --reload --host 0.0.0.0 --port 8000
```

Le serveur API sera accessible à l'adresse http://localhost:8000/
La documentation interactive de l'API sera disponible à http://localhost:8000/docs

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

## Utilisation avec Docker (recommandé)

Le projet est configuré pour fonctionner avec Docker et Docker Compose, ce qui simplifie considérablement le déploiement et le développement.

1. S'assurer que Docker et Docker Compose sont installés sur votre machine

2. Construire et démarrer les conteneurs :

```bash
# À la racine du projet
docker-compose up -d --build
```

Cette commande va :
- Construire les images Docker pour le backend et le frontend
- Démarrer les conteneurs en mode détaché (background)
- Configurer le réseau entre les services

3. Accéder aux applications :

- Frontend : http://localhost:5173/
- Backend API : http://localhost:8000/
- Documentation API : http://localhost:8000/docs

4. Suivre les logs :

```bash
# Logs du backend
docker-compose logs -f backend

# Logs du frontend
docker-compose logs -f frontend

# Tous les logs
docker-compose logs -f
```

5. Arrêter les conteneurs :

```bash
docker-compose down
```

### Avantages de l'approche Docker

- Environnement de développement cohérent et reproductible
- Pas besoin d'installer Python, Node.js ou d'autres dépendances localement
- Démarrage en une seule commande des deux services (backend et frontend)
- Volume bind mounts pour permettre la modification des fichiers en temps réel sans reconstruire les images
- Facilité de déploiement sur d'autres environnements

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

## Communication Frontend-Backend

Le frontend et le backend communiquent via une API REST :

### Configuration

Le frontend est configuré pour communiquer avec le backend à l'adresse `http://localhost:8000` par défaut. Cette configuration peut être modifiée dans le fichier `.env.local` en ajoutant :

```
VITE_API_BASE_URL=http://votre-url-api
```

### Endpoints API utilisés

Le frontend interagit principalement avec les endpoints suivants :

- `GET /procedures/search/by-name?name={terme}` - Recherche d'interventions par nom
- `GET /procedures/{id}` - Récupération des détails d'une intervention spécifique

### Cycle de développement

Pour travailler sur l'application :

1. Démarrer le backend (terminal 1) :
   ```bash
   cd backend
   source .venv/bin/activate
   python -m uvicorn infrastructure.api.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Démarrer le frontend (terminal 2) :
   ```bash
   cd frontend
   npm run dev
   ```

3. Ouvrir votre navigateur à http://localhost:5173/

### CORS et sécurité

En développement, le backend est configuré pour accepter les requêtes de n'importe quelle origine (CORS). En production, cette configuration devra être restreinte aux domaines spécifiques hébergeant le frontend.

## Licence

Ce projet est développé à des fins éducatives et de recherche.

## Références

- Recommandations Formalisées d'Experts - SFAR
